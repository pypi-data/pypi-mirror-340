# mypy: disable-error-code="empty-body"
# ruff: noqa: F821
import logging
import os
from pathlib import Path
from typing import Dict, List, Literal, Optional, Sequence, Tuple, Union, cast, overload

import numpy as np
import torch
import trimesh
from beartype import beartype
from jaxtyping import Bool, Float, Int
from typing_extensions import deprecated

from fastdev.robo.articulation_spec import ArticulationSpec
from fastdev.robo.kinematics import calculate_jacobian as calculate_jacobian_pt
from fastdev.robo.kinematics import forward_kinematics as forward_kinematics_pt
from fastdev.robo.kinematics import inverse_kinematics as inverse_kinematics_pt
from fastdev.robo.warp_kinematics import calculate_jacobian as calculate_jacobian_wp
from fastdev.robo.warp_kinematics import forward_kinematics as forward_kinematics_wp
from fastdev.robo.warp_kinematics import forward_kinematics_numpy as forward_kinematics_wp_np
from fastdev.robo.warp_kinematics import inverse_kinematics as inverse_kinematics_wp

logger = logging.getLogger("fastdev")

Device = Optional[Union[str, int, torch.device]]  # from torch.types import Device  # make mypy happy


@beartype
class Articulation:
    """Class to manage multiple articulations.

    Args:
        specs (Sequence[ArticulationSpec]): Articulation specifications.
        device (str, optional): Device to store tensors. Defaults to "cpu".

    Examples:
        >>> arti = Articulation(ArticulationSpec(urdf_or_mjcf_path="assets/robot_description/panda.urdf"))
        >>> link_poses = arti.forward_kinematics(torch.zeros(1, arti.total_num_dofs), clamp_joint_values=False)
        >>> torch.allclose(link_poses[0, -1, :3, 3], torch.tensor([0.0880, 0.0000, 0.8676]), atol=1e-3)
        True
    """

    specs: Sequence[ArticulationSpec]

    num_arti: int
    total_num_dofs: int
    total_num_links: int
    total_num_full_joints: int

    def __init__(self, specs: Union[ArticulationSpec, Sequence[ArticulationSpec]], device: Device = "cpu"):
        # ------------------------------ handle parameters ------------------------------
        if isinstance(specs, ArticulationSpec):
            specs = [specs]
        self.specs = specs
        self.device = device

        # ------------------------------ parse specs ------------------------------
        self.num_arti = len(specs)
        self.total_num_dofs = sum([spec.num_dofs for spec in specs])
        self.total_num_links = sum([spec.num_links for spec in specs])
        self.total_num_full_joints = sum([spec.num_full_joints for spec in specs])

        # ------------------------------ lazy init ------------------------------
        # active joints
        self._has_none_joint_limits: Optional[bool] = None
        self._joint_limits_np: Optional[np.ndarray] = None
        self._joint_limits_pt: Optional[torch.Tensor] = None

        # mimic joints
        self._has_mimic_joints: Optional[bool] = None
        self._has_none_mimic_joint_limits: Optional[bool] = None
        self._mimic_joint_indices_np: Optional[np.ndarray] = None
        self._mimic_joint_indices_pt: Optional[torch.Tensor] = None
        self._mimic_multipliers_np: Optional[np.ndarray] = None
        self._mimic_multipliers_pt: Optional[torch.Tensor] = None
        self._mimic_offsets_np: Optional[np.ndarray] = None
        self._mimic_offsets_pt: Optional[torch.Tensor] = None
        self._mimic_joint_limits_np: Optional[np.ndarray] = None
        self._mimic_joint_limits_pt: Optional[torch.Tensor] = None

        # full joints
        self._full_joint_reorder_indices_np: Optional[np.ndarray] = None
        self._full_joint_reorder_indices_pt: Optional[torch.Tensor] = None
        # the following are for pytorch kinematics
        self._full_joint_axes_np: Optional[np.ndarray] = None
        self._full_joint_axes_pt: Optional[torch.Tensor] = None

        # links
        self._link_indices_topological_order_np: Optional[np.ndarray] = None
        self._link_indices_topological_order_pt: Optional[torch.Tensor] = None
        self._link_joint_indices_np: Optional[np.ndarray] = None
        self._link_joint_indices_pt: Optional[torch.Tensor] = None
        self._parent_link_indices_np: Optional[np.ndarray] = None
        self._parent_link_indices_pt: Optional[torch.Tensor] = None
        # NOTE We use _link_joint_xxx because some links have joints that are neither active nor mimic joints.
        # While _link_joint_indices refers to indices in (active_joints + mimic_joints),
        # we need separate arrays for joint properties (type, origin, axis)
        self._link_joint_types_np: Optional[np.ndarray] = None
        self._link_joint_types_pt: Optional[torch.Tensor] = None
        self._link_joint_origins_np: Optional[np.ndarray] = None
        self._link_joint_origins_pt: Optional[torch.Tensor] = None
        self._link_joint_axes_np: Optional[np.ndarray] = None
        self._link_joint_axes_pt: Optional[torch.Tensor] = None

        # first indices
        self._joint_first_indices_np: Optional[np.ndarray] = None
        self._joint_first_indices_pt: Optional[torch.Tensor] = None
        self._link_first_indices_np: Optional[np.ndarray] = None
        self._link_first_indices_pt: Optional[torch.Tensor] = None

    @classmethod
    def from_urdf_or_mjcf_paths(
        cls,
        urdf_or_mjcf_paths: Union[Union[str, Path], Sequence[Union[str, Path]]],
        mesh_dirs: Optional[Union[Union[str, Path], Sequence[Union[str, Path]]]] = None,
        device: Device = "cpu",
    ):
        if isinstance(urdf_or_mjcf_paths, str) or isinstance(urdf_or_mjcf_paths, Path):
            urdf_or_mjcf_paths = [urdf_or_mjcf_paths]
        if mesh_dirs is not None:
            if isinstance(mesh_dirs, str) or isinstance(mesh_dirs, Path):
                mesh_dirs = [mesh_dirs]
            if len(urdf_or_mjcf_paths) != len(mesh_dirs):
                raise ValueError("The number of URDF/MJCF paths and mesh directories must match.")
        specs = []
        for idx, urdf_or_mjcf_path in enumerate(urdf_or_mjcf_paths):
            if mesh_dirs is not None:
                specs.append(ArticulationSpec(urdf_or_mjcf_path, mesh_dir=mesh_dirs[idx]))
            else:
                specs.append(ArticulationSpec(urdf_or_mjcf_path))
        return cls(specs, device=device)

    @classmethod
    def from_urdf_or_mjcf_path(
        cls,
        urdf_or_mjcf_path: Union[Union[str, Path], Sequence[Union[str, Path]]],
        mesh_dir: Optional[Union[Union[str, Path], Sequence[Union[str, Path]]]] = None,
        device: Device = "cpu",
    ):
        """Keep this method for compatibility with old code."""
        return cls.from_urdf_or_mjcf_paths(urdf_or_mjcf_path, mesh_dir, device=device)

    @property
    def first_spec(self) -> ArticulationSpec:
        return self.specs[0]

    @property
    def has_none_joint_limits(self) -> bool:
        if self._has_none_joint_limits is None:
            self._has_none_joint_limits = any([spec.joint_limits is None for spec in self.specs])
        return self._has_none_joint_limits

    @property
    def has_none_mimic_joint_limits(self) -> bool:
        if self._has_none_mimic_joint_limits is None:
            self._has_none_mimic_joint_limits = any([spec.mimic_joint_limits is None for spec in self.specs])
        return self._has_none_mimic_joint_limits

    @property
    def has_mimic_joints(self) -> bool:
        if self._has_mimic_joints is None:
            self._has_mimic_joints = any([spec.has_mimic_joints for spec in self.specs])
        return self._has_mimic_joints

    @property
    def joint_limits(self) -> Optional[Float[torch.Tensor, "total_num_dofs 2"]]:
        return self.get_packed_joint_limits(return_tensors="pt", return_mimic_joints=False)  # type: ignore

    @property
    def num_dofs(self) -> int:
        return self.total_num_dofs

    @property
    def active_joint_names(self) -> Union[List[str], List[List[str]]]:
        if len(self.specs) == 1:
            return self.first_spec.active_joint_names
        else:
            return [spec.active_joint_names for spec in self.specs]

    @property
    def mimic_joint_names(self) -> Union[List[str], List[List[str]]]:
        if len(self.specs) == 1:
            return self.first_spec.mimic_joint_names
        else:
            return [spec.mimic_joint_names for spec in self.specs]

    @property
    def link_names(self) -> Union[List[str], List[List[str]]]:
        if len(self.specs) == 1:
            return self.first_spec.link_names
        else:
            return [spec.link_names for spec in self.specs]

    @overload
    def _get_packed_var_from_specs(self, var_name: str, return_tensors: Literal["np"]) -> np.ndarray: ...
    @overload
    def _get_packed_var_from_specs(self, var_name: str, return_tensors: Literal["pt"]) -> torch.Tensor: ...
    def _get_packed_var_from_specs(
        self, var_name: str, return_tensors: Literal["np", "pt"] = "np"
    ) -> Union[np.ndarray, torch.Tensor]:
        VALID_VAR_NAMES = {
            "joint_limits",
            "mimic_joint_limits",
            "mimic_multipliers",
            "mimic_offsets",
            "full_joint_axes",
            "link_indices_topological_order",
            "link_joint_indices",
            "link_joint_origins",
            "link_joint_axes",
            "link_joint_types",
            "parent_link_indices",
        }
        if var_name not in VALID_VAR_NAMES:
            raise ValueError(f"Variable {var_name} cannot be packed from specs.")
        np_attr = f"_{var_name}_np"
        pt_attr = f"_{var_name}_pt"
        if return_tensors == "np":
            if getattr(self, np_attr) is None:
                values = [getattr(spec, var_name) for spec in self.specs]
                result_np = np.concatenate(values, axis=0)
                setattr(self, np_attr, cast(np.ndarray, result_np))
            return cast(np.ndarray, getattr(self, np_attr))
        elif return_tensors == "pt":
            if getattr(self, pt_attr) is None:
                np_var = self._get_packed_var_from_specs(var_name, return_tensors="np")
                result_pt = torch.from_numpy(np_var).to(self.device, non_blocking=True).contiguous()  # type: ignore
                setattr(self, pt_attr, result_pt)
            return cast(torch.Tensor, getattr(self, pt_attr))

    def _get_packed_mimic_joint_indices(
        self, return_tensors: Literal["np", "pt"] = "np"
    ) -> Union[np.ndarray, torch.Tensor]:
        if return_tensors == "np":
            if self._mimic_joint_indices_np is None:
                joint_offsets = np.cumsum([0] + [spec.num_dofs for spec in self.specs[:-1]])
                self._mimic_joint_indices_np = np.concatenate(
                    [spec.mimic_joint_indices + offset for spec, offset in zip(self.specs, joint_offsets)], axis=0
                )
            return self._mimic_joint_indices_np
        elif return_tensors == "pt":
            if self._mimic_joint_indices_pt is None:
                mimic_joint_indices_np = self._get_packed_mimic_joint_indices(return_tensors="np")
                self._mimic_joint_indices_pt = torch.from_numpy(mimic_joint_indices_np).to(self.device).contiguous()  # type: ignore
            return self._mimic_joint_indices_pt

    def _get_packed_full_joint_reorder_indices(
        self, return_tensors: Literal["np", "pt"] = "np"
    ) -> Union[np.ndarray, torch.Tensor]:
        if return_tensors == "np":
            if self._full_joint_reorder_indices_np is None:
                full_joint_offsets = np.cumsum([0] + [spec.num_full_joints for spec in self.specs[:-1]])
                mimic_joint_indices_in_full_joints = np.concatenate(
                    [
                        np.arange(spec.num_dofs, spec.num_full_joints) + offset
                        for spec, offset in zip(self.specs, full_joint_offsets)
                    ]
                )
                active_joint_indices_in_full_joints = np.concatenate(
                    [np.arange(spec.num_dofs) + offset for spec, offset in zip(self.specs, full_joint_offsets)]
                )
                reorder_indices = np.zeros((self.total_num_full_joints,), dtype=np.int32)
                reorder_indices[mimic_joint_indices_in_full_joints] = np.arange(
                    self.total_num_dofs, self.total_num_full_joints
                )
                reorder_indices[active_joint_indices_in_full_joints] = np.arange(self.total_num_dofs)
                self._full_joint_reorder_indices_np = reorder_indices
            return self._full_joint_reorder_indices_np
        elif return_tensors == "pt":
            if self._full_joint_reorder_indices_pt is None:
                full_joint_reorder_indices_np = self._get_packed_full_joint_reorder_indices(return_tensors="np")
                self._full_joint_reorder_indices_pt = (
                    torch.from_numpy(full_joint_reorder_indices_np).to(self.device).contiguous()  # type: ignore
                )
            return self._full_joint_reorder_indices_pt

    def get_packed_joint_limits(
        self, return_tensors: Literal["np", "pt"] = "np", return_mimic_joints: bool = False
    ) -> Optional[Union[np.ndarray, torch.Tensor]]:
        if not return_mimic_joints and not self.has_none_joint_limits:
            return self._get_packed_var_from_specs("joint_limits", return_tensors=return_tensors)
        elif return_mimic_joints and not self.has_none_mimic_joint_limits:
            return self._get_packed_var_from_specs("mimic_joint_limits", return_tensors=return_tensors)
        else:
            return None

    def get_packed_link_indices_topological_order(
        self, return_tensors: Literal["np", "pt"] = "np"
    ) -> Union[np.ndarray, torch.Tensor]:
        return self._get_packed_var_from_specs("link_indices_topological_order", return_tensors=return_tensors)

    def get_packed_parent_link_indices(
        self, return_tensors: Literal["np", "pt"] = "np"
    ) -> Union[np.ndarray, torch.Tensor]:
        return self._get_packed_var_from_specs("parent_link_indices", return_tensors=return_tensors)

    def get_packed_link_joint_indices(
        self, return_tensors: Literal["np", "pt"] = "np"
    ) -> Union[np.ndarray, torch.Tensor]:
        return self._get_packed_var_from_specs("link_joint_indices", return_tensors=return_tensors)

    def get_packed_link_joint_types(
        self, return_tensors: Literal["np", "pt"] = "np"
    ) -> Union[np.ndarray, torch.Tensor]:
        return self._get_packed_var_from_specs("link_joint_types", return_tensors=return_tensors)

    def get_packed_link_joint_origins(
        self, return_tensors: Literal["np", "pt"] = "np"
    ) -> Union[np.ndarray, torch.Tensor]:
        return self._get_packed_var_from_specs("link_joint_origins", return_tensors=return_tensors)

    def get_packed_link_joint_axes(self, return_tensors: Literal["np", "pt"] = "np") -> Union[np.ndarray, torch.Tensor]:
        return self._get_packed_var_from_specs("link_joint_axes", return_tensors=return_tensors)

    def get_packed_full_joint_axes(self, return_tensors: Literal["np", "pt"] = "np") -> Union[np.ndarray, torch.Tensor]:
        return self._get_packed_var_from_specs("full_joint_axes", return_tensors=return_tensors)

    def get_joint_first_indices(self, return_tensors: Literal["np", "pt"] = "np") -> Union[np.ndarray, torch.Tensor]:
        if return_tensors == "np":
            if self._joint_first_indices_np is None:
                joint_first_indices_np = np.cumsum([0] + [spec.num_full_joints for spec in self.specs[:-1]])
                self._joint_first_indices_np = joint_first_indices_np.astype(np.int32)
            return self._joint_first_indices_np
        elif return_tensors == "pt":
            if self._joint_first_indices_pt is None:
                joint_first_indices_np = self.get_joint_first_indices(return_tensors="np")  # type: ignore
                self._joint_first_indices_pt = torch.from_numpy(joint_first_indices_np).to(self.device).contiguous()  # type: ignore
            return self._joint_first_indices_pt

    def get_link_first_indices(self, return_tensors: Literal["np", "pt"] = "np") -> Union[np.ndarray, torch.Tensor]:
        if return_tensors == "np":
            if self._link_first_indices_np is None:
                link_first_indices_np = np.cumsum([0] + [spec.num_links for spec in self.specs[:-1]])
                self._link_first_indices_np = link_first_indices_np.astype(np.int32)
            return self._link_first_indices_np
        elif return_tensors == "pt":
            if self._link_first_indices_pt is None:
                link_first_indices_np = self.get_link_first_indices(return_tensors="np")  # type: ignore
                self._link_first_indices_pt = torch.from_numpy(link_first_indices_np).to(self.device).contiguous()  # type: ignore
            return self._link_first_indices_pt

    def get_packed_ancestor_links_mask(
        self, target_link_indices: Int[torch.Tensor, "num_arti"], return_tensors: Literal["np", "pt"] = "np"
    ) -> Union[np.ndarray, torch.Tensor]:
        ancestor_link_masks_np = [
            spec.get_ancestor_links_mask(target_link_indices[spec_idx].item())
            for spec_idx, spec in enumerate(self.specs)
        ]
        ancestor_link_masks_np = np.concatenate(ancestor_link_masks_np, axis=0).astype(np.int32)
        if return_tensors == "np":
            return ancestor_link_masks_np  # type: ignore
        elif return_tensors == "pt":
            return torch.from_numpy(ancestor_link_masks_np).to(self.device).contiguous()  # type: ignore

    def get_packed_zero_joint_values(
        self, return_tensors: Literal["np", "pt"] = "np"
    ) -> Union[np.ndarray, torch.Tensor]:
        if return_tensors == "np":
            return np.zeros((self.total_num_dofs,), dtype=np.float32)
        elif return_tensors == "pt":
            return torch.zeros((self.total_num_dofs,), device=self.device, dtype=torch.float32)  # type: ignore

    def get_zero_joint_values(self, return_tensors: Literal["np", "pt"] = "np") -> Union[np.ndarray, torch.Tensor]:
        return self.get_packed_zero_joint_values(return_tensors=return_tensors)

    def get_link_trimesh_meshes(
        self, mode: Literal["visual", "collision"] = "collision", return_empty_meshes: bool = False
    ) -> Union[Dict[str, trimesh.Trimesh], List[Dict[str, trimesh.Trimesh]]]:
        if len(self.specs) == 1:
            return self.first_spec.get_link_trimesh_meshes(mode=mode, return_empty_meshes=return_empty_meshes)
        else:
            return [
                spec.get_link_trimesh_meshes(mode=mode, return_empty_meshes=return_empty_meshes) for spec in self.specs
            ]

    def apply_mimic_joints(
        self,
        joint_values: Float[torch.Tensor, "... total_num_dofs"],
        clamp_joint_values: bool = True,
    ) -> Float[torch.Tensor, "... total_num_full_joints"]:
        if not self.has_mimic_joints:
            return joint_values
        else:
            mimic_joint_indices = self._get_packed_mimic_joint_indices(return_tensors="pt")
            mimic_multipliers = self._get_packed_var_from_specs("mimic_multipliers", return_tensors="pt")
            mimic_offsets = self._get_packed_var_from_specs("mimic_offsets", return_tensors="pt")

            mimic_joint_values = joint_values[..., mimic_joint_indices] * mimic_multipliers + mimic_offsets
            if clamp_joint_values and not self.has_none_mimic_joint_limits:
                mimic_joint_limits = self.get_packed_joint_limits(return_tensors="pt", return_mimic_joints=True)
                mimic_joint_values = torch.clamp(
                    mimic_joint_values,
                    mimic_joint_limits[..., 0],  # type: ignore
                    mimic_joint_limits[..., 1],  # type: ignore
                )
            full_joint_values = torch.cat([joint_values, mimic_joint_values], dim=-1)
            # NOTE No need to reorder full joint values if there is only one articulation, hope this is correct
            if len(self.specs) > 1:
                full_joint_reorder_indices = self._get_packed_full_joint_reorder_indices(return_tensors="pt")
                full_joint_values = torch.index_select(full_joint_values, -1, full_joint_reorder_indices)  # type: ignore
            return full_joint_values

    def _reindex_joint_values(
        self,
        joint_values: Float[torch.Tensor, "... total_num_dofs"],
        joint_names: Optional[Union[List[List[str]], List[str]]] = None,
    ) -> Float[torch.Tensor, "... total_num_dofs"]:
        if joint_names is not None:
            # if a flat list is provided for a single articulation, wrap it in an extra list
            if isinstance(joint_names, list) and joint_names and isinstance(joint_names[0], str):
                joint_names = cast(List[List[str]], [joint_names])
            # convert the offsets to a list of ints
            joints_offset = np.cumsum([0] + [spec.num_dofs for spec in self.specs[:-1]]).tolist()
            joint_reindex_list: List[int] = []
            for spec, j_name_list, offset in zip(self.specs, joint_names, joints_offset):
                for j_name in spec.active_joint_names:
                    # ensure j_name is a string; j_name_list is List[str]
                    index_in_list = j_name_list.index(j_name)
                    joint_reindex_list.append(index_in_list + offset)
            joint_reindex = torch.tensor(joint_reindex_list, device=joint_values.device, dtype=torch.long)
            joint_values = torch.index_select(joint_values, -1, joint_reindex)
        return joint_values

    def forward_kinematics(
        self,
        joint_values: Union[Float[torch.Tensor, "... total_num_dofs"]],
        joint_names: Optional[Union[List[List[str]], List[str]]] = None,
        root_poses: Optional[Union[Float[torch.Tensor, "... num_arti 4 4"], Float[torch.Tensor, "... 4 4"]]] = None,
        clamp_joint_values: bool = True,
        use_warp: bool = True,
    ) -> Float[torch.Tensor, "... total_num_links 4 4"]:
        """Forward kinematics.

        Args:
            joint_values (torch.Tensor): Packed joint values of shape (..., total_num_dofs).
            joint_names (List[List[str]], optional): Joint names for each articulation. Defaults to None.
                Could be a single list of joint names if there is only one articulation.
            root_poses (torch.Tensor, optional): Root poses of shape (..., num_arti, 4, 4). Defaults to None.
                The `num_arti` dimension can be omitted only if a single articulation is being used.
            clamp_joint_values (bool, optional): Whether to clamp joint values to joint limits. Defaults to True.
        """
        if joint_names is not None:
            joint_values = self._reindex_joint_values(joint_values, joint_names)
        if clamp_joint_values and not self.has_none_joint_limits:
            joint_limits = self.get_packed_joint_limits(return_tensors="pt", return_mimic_joints=False)
            joint_values = torch.clamp(joint_values, joint_limits[..., 0], joint_limits[..., 1])  # type: ignore
        if self.has_mimic_joints:
            joint_values = self.apply_mimic_joints(joint_values, clamp_joint_values=clamp_joint_values)

        if root_poses is not None and root_poses.ndim == joint_values.ndim + 1 and self.num_arti == 1:
            root_poses = root_poses.unsqueeze(-3)  # insert num_arti dimension
        if root_poses is not None:
            root_poses = root_poses.expand(*joint_values.shape[:-1], self.num_arti, 4, 4)
        if use_warp:
            link_poses = forward_kinematics_wp(joint_values, articulation=self, root_poses=root_poses)
        else:
            link_poses = forward_kinematics_pt(joint_values, articulation=self, root_poses=root_poses)

        return link_poses

    def _get_target_link_indices(
        self,
        target_links: Optional[Union[str, List[str], int, List[int], Int[torch.Tensor, "num_arti"]]] = None,
        device: Optional[Device] = None,
    ) -> Int[torch.Tensor, "num_arti"]:
        if device is None:
            device = self.device
        if target_links is None:
            target_link_indices = torch.tensor(
                [spec.num_links - 1 for spec in self.specs], device=device, dtype=torch.int32
            )
        elif isinstance(target_links, torch.Tensor):
            target_link_indices = target_links
        else:
            if isinstance(target_links, str) or isinstance(target_links, int):
                target_links = [target_links]  # type: ignore
            if isinstance(target_links, list) and isinstance(target_links[0], str):
                target_link_indices = [spec.link_names.index(n) for spec, n in zip(self.specs, target_links)]  # type: ignore
            else:
                target_link_indices = target_links  # type: ignore
            target_link_indices = torch.tensor(target_link_indices, device=device, dtype=torch.int32)
        return target_link_indices

    def jacobian(
        self,
        joint_values: Float[torch.Tensor, "... total_num_dofs"],
        joint_names: Optional[Union[List[List[str]], List[str]]] = None,
        root_poses: Optional[Union[Float[torch.Tensor, "... num_arti 4 4"], Float[torch.Tensor, "... 4 4"]]] = None,
        target_links: Optional[Union[str, List[str], int, List[int], Int[torch.Tensor, "num_arti"]]] = None,
        clamp_joint_values: bool = True,
        use_warp: bool = True,
        return_target_link_poses: bool = False,
    ) -> Union[
        Float[torch.Tensor, "... 6 total_num_dofs"],
        Tuple[Float[torch.Tensor, "... 6 total_num_dofs"], Float[torch.Tensor, "... num_arti 4 4"]],
    ]:
        if joint_names is not None:
            joint_values = self._reindex_joint_values(joint_values, joint_names)
        if clamp_joint_values and not self.has_none_joint_limits:
            joint_limits = self.get_packed_joint_limits(return_tensors="pt", return_mimic_joints=False)
            joint_values = torch.clamp(joint_values, joint_limits[..., 0], joint_limits[..., 1])  # type: ignore
        if self.has_mimic_joints:
            joint_values = self.apply_mimic_joints(joint_values, clamp_joint_values=clamp_joint_values)

        if root_poses is not None and root_poses.ndim == joint_values.ndim + 1 and self.num_arti == 1:
            root_poses = root_poses.unsqueeze(-3)  # insert num_arti dimension
        target_link_indices = self._get_target_link_indices(target_links, device=joint_values.device)

        if use_warp:
            return calculate_jacobian_wp(
                joint_values,
                target_link_indices=target_link_indices,
                articulation=self,
                root_poses=root_poses,
                return_target_link_poses=return_target_link_poses,
            )
        else:
            return calculate_jacobian_pt(
                joint_values,
                target_link_indices=target_link_indices,
                articulation=self,
                root_poses=root_poses,
                return_target_link_poses=return_target_link_poses,
            )

    def inverse_kinematics(
        self,
        target_link_poses: Union[Float[torch.Tensor, "... num_arti 4 4"], Float[torch.Tensor, "... 4 4"]],
        target_links: Optional[Union[str, List[str], int, List[int], torch.Tensor]] = None,
        use_warp: bool = False,
        max_iterations: int = 30,
        learning_rate: float = 0.2,
        tolerance: float = 1e-3,
        damping: float = 1e-4,
        num_retries: int = 50,
        init_joint_values: Optional[Float[torch.Tensor, "... total_num_dofs"]] = None,
        jitter_strength: float = 1.0,
        return_success: bool = False,
        force_insert_articulation_dim: bool = False,
    ) -> Union[
        Float[torch.Tensor, "... total_num_dofs"],
        Tuple[Float[torch.Tensor, "... total_num_dofs"], Bool[torch.Tensor, "... num_arti"]],
    ]:
        if target_link_poses.ndim == 2:  # it's a single target pose
            target_link_poses = target_link_poses.unsqueeze(0).unsqueeze(0)  # add batch and articulation dimensions
        elif (self.num_arti == 1 and target_link_poses.shape[-3] != 1) or (force_insert_articulation_dim):
            target_link_poses = target_link_poses.unsqueeze(-3)  # add articulation dimension
        if target_link_poses.shape[-3] != self.num_arti:
            raise ValueError(f"target_link_poses must have shape (..., {self.num_arti}, 4, 4) or (..., 4, 4)")
        if init_joint_values is not None and init_joint_values.ndim > 1:  # check batch dimensions
            if target_link_poses.shape[:-3] != init_joint_values.shape[:-1]:
                raise ValueError(
                    f"Batch dimension mismatch between target_link_poses and init_joint_values: {target_link_poses.shape[:-3]} != {init_joint_values.shape[:-1]}",
                    "Sometimes this happens when you only have a single articulation, and the last batch dimension is 1. In this case, you can specify `force_insert_articulation_dim=True`",
                )

        target_link_indices = self._get_target_link_indices(target_links, device=target_link_poses.device)

        if use_warp:
            best_q, final_success = inverse_kinematics_wp(
                target_link_poses=target_link_poses,
                target_link_indices=target_link_indices,
                articulation=self,
                max_iterations=max_iterations,
                learning_rate=learning_rate,
                tolerance=tolerance,
                damping=damping,
                num_retries=num_retries,
                init_joint_values=init_joint_values,
                jitter_strength=jitter_strength,
            )
        else:
            best_q, final_success = inverse_kinematics_pt(
                target_link_poses=target_link_poses,
                target_link_indices=target_link_indices,
                articulation=self,
                max_iterations=max_iterations,
                learning_rate=learning_rate,
                tolerance=tolerance,
                damping=damping,
                num_retries=num_retries,
                init_joint_values=init_joint_values,
                jitter_strength=jitter_strength,
            )
        if return_success:
            return best_q, final_success
        else:
            return best_q

    def apply_mimic_joints_numpy(
        self, joint_values: Float[np.ndarray, "... total_num_dofs"], clamp_joint_values: bool = True
    ) -> Float[np.ndarray, "... total_num_joints"]:
        if not self.has_mimic_joints:
            return joint_values
        else:
            mimic_joint_indices = self._get_packed_mimic_joint_indices(return_tensors="np")
            mimic_multipliers = self._get_packed_var_from_specs("mimic_multipliers", return_tensors="np")
            mimic_offsets = self._get_packed_var_from_specs("mimic_offsets", return_tensors="np")
            mimic_joint_values = joint_values[..., mimic_joint_indices] * mimic_multipliers + mimic_offsets
            if clamp_joint_values:
                mimic_joint_limits = self.get_packed_joint_limits(return_tensors="np", return_mimic_joints=True)
                mimic_joint_values = np.clip(
                    mimic_joint_values,
                    mimic_joint_limits[..., 0],  # type: ignore
                    mimic_joint_limits[..., 1],  # type: ignore
                )
            full_joint_values = np.concatenate([joint_values, mimic_joint_values], axis=-1)
            if len(self.specs) > 1:
                full_joint_reorder_indices = self._get_packed_full_joint_reorder_indices(return_tensors="np")
                full_joint_values = full_joint_values[..., full_joint_reorder_indices]
            return full_joint_values

    def forward_kinematics_numpy(
        self,
        joint_values: Union[Float[np.ndarray, "... total_num_dofs"]],
        joint_names: Optional[Union[List[List[str]], List[str]]] = None,
        root_poses: Optional[Union[Float[np.ndarray, "... num_arti 4 4"], Float[np.ndarray, "... 4 4"]]] = None,
        clamp_joint_values: bool = True,
    ) -> Float[np.ndarray, "... total_num_links 4 4"]:
        """Forward kinematics.

        Args:
            joint_values (torch.Tensor): Packed joint values of shape (..., total_num_dofs).
            joint_names (List[List[str]], optional): Joint names for each articulation. Defaults to None.
                Could be a single list of joint names if there is only one articulation.
            root_poses (torch.Tensor, optional): Root poses of shape (..., num_arti, 4, 4). Defaults to None.
                The `num_arti` dimension can be omitted only if a single articulation is being used.
            clamp_joint_values (bool, optional): Whether to clamp joint values to joint limits. Defaults to True.
        """
        if joint_names is not None:
            if isinstance(joint_names, list) and isinstance(joint_names[0], str):
                joint_names = [joint_names]  # type: ignore
            joints_offset = np.cumsum([0] + [spec.num_dofs for spec in self.specs[:-1]])
            joint_reindex = [
                j_name_list.index(j_name) + offset
                for spec, j_name_list, offset in zip(self.specs, joint_names, joints_offset)
                for j_name in spec.active_joint_names
            ]
            joint_reindex = np.array(joint_reindex, dtype=np.int32)  # type: ignore
            joint_values = joint_values[..., joint_reindex]
        if clamp_joint_values and not self.has_none_joint_limits:
            joint_limits = self.get_packed_joint_limits(return_tensors="np", return_mimic_joints=False)
            joint_values = np.clip(joint_values, joint_limits[..., 0], joint_limits[..., 1])  # type: ignore
        if self.has_mimic_joints:
            joint_values = self.apply_mimic_joints_numpy(joint_values, clamp_joint_values=clamp_joint_values)
        link_poses = forward_kinematics_wp_np(joint_values, articulation=self, root_poses=root_poses)
        return link_poses

    def to(self, device: Device) -> "Articulation":
        self.device = device

        raise NotImplementedError("Not implemented")

        return self

    def __len__(self) -> int:
        return self.num_arti

    def __getitem__(self, idx: Union[int, slice]) -> "Articulation":
        return Articulation(self.specs[idx], device=self.device)

    def __repr__(self) -> str:
        repr_str = f"Articulation(num_arti={len(self)}, "
        repr_str += (
            f"total_num_dofs={self.total_num_dofs}, total_num_links={self.total_num_links}, device={self.device})\n"
        )
        for spec in self.specs:
            filename = os.path.basename(spec.urdf_or_mjcf_path)
            repr_str += f"  - {filename} (num_dofs={spec.num_dofs}, num_links={spec.num_links})\n"
        if self.num_arti == 1:
            repr_str += "\n"
            repr_str += self.first_spec.__repr__()
        return repr_str.rstrip()

    def __str__(self) -> str:
        return self.__repr__()


@deprecated("`RobotModel` is deprecated, use `Articulation` instead")
class RobotModel(Articulation): ...


__all__ = ["Articulation"]
