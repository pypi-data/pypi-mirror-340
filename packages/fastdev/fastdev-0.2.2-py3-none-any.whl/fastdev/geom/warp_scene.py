# mypy: ignore-errors
# ruff: noqa: F821
import os
from functools import lru_cache
from typing import List, Optional, Union

import numpy as np
import torch
import trimesh
import warp as wp
from beartype import beartype
from jaxtyping import Float, Int

from fastdev.geom.warp_sdf_fns import query_sdf_in_scenes

Device = Optional[Union[str, torch.device]]  # from torch.types import Device  # make mypy happy


@beartype
class Scene:
    """Class to manage multiple scenes"""

    def __init__(self, num_scenes: int, device: Device = "cpu"):
        self.device = device
        self.num_scenes = num_scenes

        # common tensor arguments
        int_args = {"device": device, "dtype": torch.int32}
        float_args = {"device": device, "dtype": torch.float32}

        # mesh fields
        self._mesh_filenames: List[str] = []
        self._mesh_scene_indices: Int[torch.Tensor, "num_meshes"] = torch.empty((0,), **int_args)
        self._mesh_scales: Float[torch.Tensor, "num_meshes 3"] = torch.empty((0, 3), **float_args)
        self._mesh_poses: Float[torch.Tensor, "num_meshes 4 4"] = torch.empty((0, 4, 4), **float_args)
        self._wp_meshes: List[wp.Mesh] = []

        # box fields
        self._box_sizes: Float[torch.Tensor, "num_boxes 3"] = torch.empty((0, 3), **float_args)
        self._box_scene_indices: Int[torch.Tensor, "num_boxes"] = torch.empty((0,), **int_args)
        self._box_scales: Float[torch.Tensor, "num_boxes 3"] = torch.empty((0, 3), **float_args)
        self._box_poses: Float[torch.Tensor, "num_boxes 4 4"] = torch.empty((0, 4, 4), **float_args)

        # scene indices for built scenes
        self._is_built: bool = False
        self._scene_mesh_indices: Int[torch.Tensor, "num_scenes"] = torch.empty((0,), **int_args)
        self._scene_mesh_first_indices: Int[torch.Tensor, "num_scenes"] = torch.empty((0,), **int_args)
        self._scene_box_indices: Int[torch.Tensor, "num_scenes"] = torch.empty((0,), **int_args)
        self._scene_box_first_indices: Int[torch.Tensor, "num_scenes"] = torch.empty((0,), **int_args)

    def add_meshes_from_files(
        self,
        filenames: List[str],  # filenames can be repeated since meshes are cached by filename
        scene_indices: Int[torch.Tensor, "num_meshes"],
        scales: Optional[Float[torch.Tensor, "num_meshes 3"]] = None,
        poses: Optional[Float[torch.Tensor, "num_meshes 4 4"]] = None,
    ):
        filenames = [os.path.normpath(os.path.abspath(filename)) for filename in filenames]  # normalize paths
        self._mesh_filenames.extend(filenames)
        self._mesh_scene_indices = torch.cat([self._mesh_scene_indices, scene_indices.to(self.device)])
        if scales is None:
            scales = torch.ones((len(filenames), 3), device=self.device, dtype=torch.float32)
        self._mesh_scales = torch.cat([self._mesh_scales, scales.to(self.device)])
        if poses is None:
            poses = torch.eye(4, device=self.device, dtype=torch.float32).repeat(len(filenames), 1, 1)
        self._mesh_poses = torch.cat([self._mesh_poses, poses.to(self.device)])

    def add_boxes(
        self,
        sizes: Float[torch.Tensor, "num_boxes 3"],
        scene_indices: Int[torch.Tensor, "num_boxes"],
        scales: Optional[Float[torch.Tensor, "num_boxes"]] = None,
        poses: Optional[Float[torch.Tensor, "num_boxes 4 4"]] = None,
    ):
        self._box_sizes = torch.cat([self._box_sizes, sizes.to(self.device)])
        self._box_scene_indices = torch.cat([self._box_scene_indices, scene_indices.to(self.device)])
        if scales is None:
            scales = torch.ones((len(sizes), 3), device=self.device, dtype=torch.float32)
        self._box_scales = torch.cat([self._box_scales, scales.to(self.device)])
        if poses is None:
            poses = torch.eye(4, device=self.device, dtype=torch.float32).repeat(len(sizes), 1, 1)

    def add_spheres(self):
        raise NotImplementedError("Spheres are not implemented yet")

    def build(self) -> None:
        filename_to_wp_mesh = {f: self.load_warp_mesh_cached(f, self.device) for f in set(self._mesh_filenames)}
        self._wp_meshes = [filename_to_wp_mesh[f] for f in self._mesh_filenames]
        self._mesh_ids_wp = wp.array([m.id for m in self._wp_meshes], dtype=wp.uint64, device=self.device)

        mesh_indices_per_scene = [
            torch.nonzero(self._mesh_scene_indices == i, as_tuple=True)[0] for i in range(self.num_scenes)
        ]
        self._scene_mesh_indices = torch.cat(mesh_indices_per_scene, dim=0)
        mesh_counts_per_scene = torch.tensor(
            [indices.numel() for indices in mesh_indices_per_scene], device=self.device, dtype=torch.int32
        )
        self._scene_mesh_first_indices = torch.cat(
            [torch.zeros(1, device=self.device, dtype=torch.int32), torch.cumsum(mesh_counts_per_scene, dim=0)[:-1]],
            dim=0,
        )

        box_indices_per_scene = [
            torch.nonzero(self._box_scene_indices == i, as_tuple=True)[0] for i in range(self.num_scenes)
        ]
        self._scene_box_indices = torch.cat(box_indices_per_scene, dim=0)
        box_counts_per_scene = torch.tensor(
            [indices.numel() for indices in box_indices_per_scene], device=self.device, dtype=torch.int32
        )
        self._scene_box_first_indices = torch.cat(
            [torch.zeros(1, device=self.device, dtype=torch.int32), torch.cumsum(box_counts_per_scene, dim=0)[:-1]],
            dim=0,
        )

        self._is_built = True

    def query_signed_distances(
        self,
        query_points: Float[torch.Tensor, "num_points 3"],
        query_points_first_idx: Int[torch.Tensor, "num_scenes"],
        max_dist: float = 1e6,
    ) -> torch.Tensor:
        if not self._is_built:
            raise RuntimeError("Scene is not built. Call build() first.")
        wp.init()

        full_query_points_first_idx = torch.cat(
            [query_points_first_idx, torch.tensor([query_points.shape[0]], device=query_points.device)]
        )
        max_num_pts_per_scene = torch.diff(full_query_points_first_idx).max().item()

        sdf = torch.empty_like(query_points[..., 0], requires_grad=False)
        normals = torch.empty_like(query_points, requires_grad=False)
        clst_pts = torch.empty_like(query_points, requires_grad=False)

        wp.launch(
            kernel=query_sdf_in_scenes,
            dim=(max_num_pts_per_scene, self.num_scenes),
            inputs=[
                wp.from_torch(query_points.contiguous().view(-1, 3), dtype=wp.vec3, requires_grad=False),
                wp.from_torch(query_points_first_idx.contiguous().to(torch.int32), dtype=wp.int32, requires_grad=False),
                self._mesh_ids_wp,
                self._meshes_first_idx_wp,
                self._mesh_poses,
                self._mesh_scales,
                self._box_sizes,
                self._box_first_idx_wp,
                self._box_poses,
                self._box_scales,
                max_dist,
                wp.from_torch(sdf.view(-1), dtype=wp.float32),
                wp.from_torch(normals.view(-1, 3), dtype=wp.vec3),
                wp.from_torch(clst_pts.view(-1, 3), dtype=wp.vec3),
            ],
            device=wp.device_from_torch(query_points.device),
        )

    @property
    def num_meshes(self) -> int:
        return len(self._mesh_filenames)

    @property
    def num_boxes(self) -> int:
        return len(self._box_sizes)

    def __repr__(self) -> str:
        return f"Scene(num_scenes={self.num_scenes}, num_meshes={self.num_meshes}, num_boxes={self.num_boxes})"

    def __str__(self) -> str:
        return self.__repr__()

    @staticmethod
    @lru_cache(maxsize=1024)
    @beartype
    def load_warp_mesh_cached(mesh_path: str, device: Device = "cpu") -> wp.Mesh:
        mesh = trimesh.load(mesh_path, process=False, force="mesh")
        v, f = mesh.vertices.view(np.ndarray), mesh.faces.view(np.ndarray)  # type: ignore
        return wp.Mesh(
            points=wp.array(v, dtype=wp.vec3, device=device),
            indices=wp.array(np.ravel(f), dtype=int, device=device),
        )
