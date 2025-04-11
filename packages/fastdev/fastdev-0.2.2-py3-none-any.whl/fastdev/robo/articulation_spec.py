# mypy: disable-error-code="empty-body"
# ruff: noqa: F821
import logging
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Set, Tuple, Union, cast

import numpy as np
import transforms3d
import trimesh
import yourdfpy
from beartype import beartype
from jaxtyping import Float, Int
from lxml import etree
from trimesh.util import concatenate

logger = logging.getLogger("fastdev")
ROOT_JOINT_NAME: str = "__root__"


class Geometry(ABC):
    @abstractmethod
    def get_trimesh_mesh(self) -> trimesh.Trimesh: ...


@dataclass
class Box(Geometry):
    size: List[float]

    def get_trimesh_mesh(self) -> trimesh.Trimesh:
        return trimesh.creation.box(self.size)


@dataclass
class Cylinder(Geometry):
    radius: float
    length: float

    def get_trimesh_mesh(self) -> trimesh.Trimesh:
        return trimesh.creation.cylinder(radius=self.radius, height=self.length)


@dataclass
class Capsule(Geometry):
    radius: float
    length: float

    def get_trimesh_mesh(self) -> trimesh.Trimesh:
        return trimesh.creation.capsule(radius=self.radius, height=self.length)


@dataclass
class Sphere(Geometry):
    radius: float

    def get_trimesh_mesh(self) -> trimesh.Trimesh:
        return trimesh.creation.icosphere(subdivisions=3, radius=self.radius)


def _try_very_hard_to_find_mesh_path(mesh_filename: str, mesh_dir: Optional[str] = None) -> str:
    mesh_filename = mesh_filename.replace("package://", "")  # remove package://
    if mesh_dir is not None:
        for level in range(len(os.path.normpath(mesh_filename).split(os.path.sep))):
            mesh_filename = os.path.normpath(mesh_filename).split(os.path.sep, level)[-1]
            if os.path.exists(os.path.join(mesh_dir, mesh_filename)):
                return os.path.join(mesh_dir, mesh_filename)
    else:
        for level in range(len(os.path.normpath(mesh_filename).split(os.path.sep))):
            mesh_filename = os.path.normpath(mesh_filename).split(os.path.sep, level)[-1]
            if os.path.exists(mesh_filename):
                return mesh_filename
    raise FileNotFoundError(f"Mesh file not found: {mesh_filename=}, {mesh_dir=}")


@dataclass
class Mesh(Geometry):
    scale: List[float]

    filename: Optional[str] = None  # usually relative path
    mesh_dir: Optional[str] = None  # usually urdf/mjcf file directory
    is_collision_geometry: bool = False

    vertices: Optional[np.ndarray] = None  # unscaled vertices
    faces: Optional[np.ndarray] = None

    _scaled_trimesh_mesh: Optional[trimesh.Trimesh] = None

    def get_trimesh_mesh(self) -> trimesh.Trimesh:
        if self._scaled_trimesh_mesh is not None:
            return self._scaled_trimesh_mesh

        if self.vertices is not None and self.faces is not None:
            self._scaled_trimesh_mesh = trimesh.Trimesh(self.vertices * np.asarray(self.scale), self.faces)
        else:
            if self.filename is None:
                raise ValueError("Either filename or vertices and faces must be provided")
            mesh_path = _try_very_hard_to_find_mesh_path(self.filename, self.mesh_dir)
            mesh: trimesh.Trimesh = trimesh.load(mesh_path, force="mesh", skip_materials=self.is_collision_geometry)  # type: ignore
            mesh.apply_scale(self.scale)
            self._scaled_trimesh_mesh = mesh

        return self._scaled_trimesh_mesh


@dataclass
class Material:
    name: Optional[str] = None
    color: Optional[np.ndarray] = None
    texture: Optional[str] = None


@dataclass
class Visual:
    origin: np.ndarray
    geometry: Geometry
    name: Optional[str] = None
    material: Optional[Material] = None

    def get_trimesh_mesh(self) -> trimesh.Trimesh:
        mesh = self.geometry.get_trimesh_mesh()
        return mesh.apply_transform(self.origin)


@dataclass
class Collision:
    origin: np.ndarray
    geometry: Geometry
    name: Optional[str] = None

    def get_trimesh_mesh(self) -> trimesh.Trimesh:
        mesh = self.geometry.get_trimesh_mesh()
        return mesh.apply_transform(self.origin)


class JointType(Enum):
    ROOT = -1  # used for base link, which has no parent joint
    FIXED = 0
    PRISMATIC = 1
    REVOLUTE = 2  # aka. rotational


@dataclass(frozen=True)
@beartype
class Joint:
    name: str
    type: JointType
    origin: Float[np.ndarray, "4 4"]
    axis: Float[np.ndarray, "3"]
    limit: Optional[Float[np.ndarray, "2"]]

    parent_link_name: str
    child_link_name: str

    mimic_joint: Optional[str] = None
    mimic_multiplier: Optional[float] = None
    mimic_offset: Optional[float] = None

    def set_child_link_name(self, child_link_name: str):
        object.__setattr__(self, "child_link_name", child_link_name)

    def __post_init__(self):
        if self.origin.shape != (4, 4):
            raise ValueError(f"Invalid origin shape: {self.origin.shape}")
        if self.axis.shape != (3,):
            raise ValueError(f"Invalid axis shape: {self.axis.shape}")
        if self.limit is not None and self.limit.shape != (2,):
            raise ValueError(f"Invalid limit shape: {self.limit.shape}")


@dataclass(frozen=True)
@beartype
class Link:
    name: str
    visuals: List[Visual] = field(default_factory=list)
    collisions: List[Collision] = field(default_factory=list)

    joint_name: str = field(init=False)  # parent joint name in urdf

    def set_joint_name(self, joint_name: str):
        object.__setattr__(self, "joint_name", joint_name)

    def get_trimesh_mesh(self, mode: Literal["visual", "collision"] = "collision") -> trimesh.Trimesh:
        if mode == "visual":
            meshes = [visual.get_trimesh_mesh() for visual in self.visuals]
        elif mode == "collision":
            meshes = [collision.get_trimesh_mesh() for collision in self.collisions]
        else:
            raise ValueError(f"Unknown mode: {mode}")
        return concatenate(meshes)  # type: ignore


@beartype
class ArticulationSpec:
    """Specification for a single articulation.

    Args:
        urdf_or_mjcf_path (str): Path to the URDF or MJCF file.
        mesh_dir (str, optional): Directory to store mesh files. Defaults to None.
        format (str, optional): Format of the file, either "urdf" or "mjcf". Defaults to None.
        mjcf_assets (Dict[str, Any], optional): Assets for MJCF files. Defaults to None.
        enable_mimic_joints (bool, optional): Whether to enable mimic joints. Defaults to True.

    Examples:
        >>> arti_spec = ArticulationSpec(urdf_or_mjcf_path="assets/robot_description/panda.urdf")
        >>> arti_spec.num_dofs
        8
    """

    base_link_name: str
    ee_link_names: List[str]
    link_names: List[str]
    num_links: int

    num_dofs: int
    active_joint_names: List[str]
    has_mimic_joints: bool
    mimic_joint_names: List[str]
    full_joint_names: List[str]  # active joints + mimic joints
    num_full_joints: int

    def __init__(
        self,
        urdf_or_mjcf_path: Union[str, Path],
        mesh_dir: Optional[Union[str, Path]] = None,
        format: Optional[Literal["urdf", "mjcf"]] = None,  # will be inferred if not provided
        base_link_name: Optional[str] = None,
        ee_link_names: Optional[Union[str, List[str]]] = None,
        mjcf_assets: Optional[Dict[str, Any]] = None,
        enable_mimic_joints: bool = True,  # if False, mimic joints will be considered as active joints, only for URDF
    ):
        # ------------------------------ handle parameters ------------------------------
        self.urdf_or_mjcf_path = str(urdf_or_mjcf_path)
        if not os.path.exists(self.urdf_or_mjcf_path):
            raise FileNotFoundError(f"URDF/MJCF file not found: {self.urdf_or_mjcf_path}")

        if mesh_dir is None:
            mesh_dir = os.path.abspath(os.path.dirname(self.urdf_or_mjcf_path))
        self.mesh_dir = str(mesh_dir)

        if format is None:
            if self.urdf_or_mjcf_path.endswith(".urdf"):
                format = "urdf"
            elif self.urdf_or_mjcf_path.endswith(".xml"):
                format = "mjcf"
            else:
                raise ValueError(f"Unknown file format: {self.urdf_or_mjcf_path}")
        self.format = format

        self.mjcf_assets = mjcf_assets
        self.enable_mimic_joints = enable_mimic_joints

        # ------------------------------ parse URDF/MJCF ------------------------------
        if self.format == "urdf":
            self.joint_map, self.link_map = self.parse_urdf()
        elif self.format == "mjcf":
            self.joint_map, self.link_map = self.parse_mjcf()
        else:
            raise ValueError(f"Unknown file format: {self.format}")

        # set base link name
        if base_link_name is None:
            self.base_link_name = self.joint_map[ROOT_JOINT_NAME].child_link_name
        else:  # prune joint map and link map according to provided base link name
            if base_link_name not in self.link_map:
                raise ValueError(f"Base link name {base_link_name} not found.")
            # disconnect base link from its current parent joint
            self.joint_map[self.link_map[base_link_name].joint_name].set_child_link_name("")
            # update root joint to connect to the new base link
            self.joint_map[ROOT_JOINT_NAME].set_child_link_name(base_link_name)
            # update the base link's joint reference
            self.link_map[base_link_name].set_joint_name(ROOT_JOINT_NAME)
            self.base_link_name = base_link_name
            # keep only links in the subtree rooted at the chosen base link
            descendant_links: Set[str] = self._collect_descendant_links(base_link_name)
            self.link_map = {name: link for name, link in self.link_map.items() if name in descendant_links}
            self.joint_map = {
                name: joint for name, joint in self.joint_map.items() if joint.child_link_name in descendant_links
            }

        # set ee link names
        if ee_link_names is None:  # infer ee link names if not provided
            _link_names = list(self.link_map.keys())
            for joint in self.joint_map.values():
                if joint.parent_link_name in _link_names:
                    _link_names.remove(joint.parent_link_name)
            if len(_link_names) == 0:
                raise ValueError("Could not determine end effector link.")
            self.ee_link_names = _link_names
        else:  # prune joint map and link map according to provided ee link names
            if isinstance(ee_link_names, str):
                ee_link_names = [ee_link_names]
            for link_name in ee_link_names:
                if link_name not in self.link_map:
                    raise ValueError(f"End effector link name {link_name} not found.")
            self.ee_link_names = ee_link_names
            # compute set of links to keep: every provided ee link plus all its ancestors
            keep_links = set()
            for ee_link_name in ee_link_names:
                keep_links |= self._collect_ancestor_links(ee_link_name)
            self.link_map = {name: link for name, link in self.link_map.items() if name in keep_links}
            self.joint_map = {
                name: joint
                for name, joint in self.joint_map.items()
                if name == ROOT_JOINT_NAME or joint.child_link_name in keep_links
            }

        # collect link names
        self.link_names = list(self.link_map.keys())
        self.num_links = len(self.link_names)

        # sort all links in topological order
        cur_links = [self.base_link_name]
        topological_order = []
        while cur_links:
            next_links = []
            for link_name in cur_links:
                topological_order.append(link_name)
                for joint in self.joint_map.values():
                    if joint.parent_link_name == link_name:
                        next_links.append(joint.child_link_name)
            cur_links = next_links
        self._link_names_topological_order = topological_order

        # infer active joint names (including mimic joints here)
        self.active_joint_names = [
            joint_name
            for joint_name, joint in self.joint_map.items()
            if joint.type not in [JointType.FIXED, JointType.ROOT]
        ]
        # filter out mimic joints from active joint names if `enable_mimic_joints`
        if self.enable_mimic_joints:
            self.active_joint_names = [
                joint_name for joint_name in self.active_joint_names if self.joint_map[joint_name].mimic_joint is None
            ]
        # infer number of DOFs
        self.num_dofs = len(self.active_joint_names)
        # check if contains mimic joints
        self.has_mimic_joints: bool = any(
            self.joint_map[joint_name].mimic_joint is not None for joint_name in self.joint_map
        )
        # collect mimic joint
        if self.has_mimic_joints:
            self.mimic_joint_names: List[str] = []
            mimic_joint_indices, mimic_multipliers, mimic_offsets = [], [], []
            for joint_name in self.joint_map:
                if self.joint_map[joint_name].mimic_joint is not None:
                    self.mimic_joint_names.append(joint_name)

                    mimic_joint_indices.append(self.active_joint_names.index(self.joint_map[joint_name].mimic_joint))  # type: ignore
                    mimic_multipliers.append(self.joint_map[joint_name].mimic_multiplier)
                    mimic_offsets.append(self.joint_map[joint_name].mimic_offset)
            self._mimic_joint_indices_np: np.ndarray = np.array(mimic_joint_indices, dtype=np.int64)
            self._mimic_multipliers_np: np.ndarray = np.array(mimic_multipliers, dtype=np.float32)
            self._mimic_offsets_np: np.ndarray = np.array(mimic_offsets, dtype=np.float32)
        else:
            self.mimic_joint_names = []
            self._mimic_joint_indices_np = np.array([], dtype=np.int64)
            self._mimic_multipliers_np = np.array([], dtype=np.float32)
            self._mimic_offsets_np = np.array([], dtype=np.float32)
        self.num_mimic_joints = len(self.mimic_joint_names)
        self.full_joint_names = self.active_joint_names + self.mimic_joint_names
        self.num_full_joints = len(self.full_joint_names)

        # collect joint limits
        if len(self.active_joint_names) == 0:
            self._joint_limits_np: Optional[np.ndarray] = None
        elif any(self.joint_map[joint_name].limit is None for joint_name in self.active_joint_names):
            self._joint_limits_np = None
        else:
            self._joint_limits_np = np.stack(
                [self.joint_map[joint_name].limit for joint_name in self.active_joint_names],  # type: ignore
                axis=0,
            )
        if not self.has_mimic_joints:
            self._mimic_joint_limits_np: Optional[np.ndarray] = None
        elif any(self.joint_map[joint_name].limit is None for joint_name in self.mimic_joint_names):
            self._mimic_joint_limits_np = None
        else:
            self._mimic_joint_limits_np = np.stack(
                [self.joint_map[joint_name].limit for joint_name in self.mimic_joint_names],  # type: ignore
                axis=0,
            )

        # ------------------------------ lazy init ------------------------------
        self._full_joint_axes_np: Optional[np.ndarray] = None
        self._link_joint_indices_np: Optional[np.ndarray] = None
        self._link_indices_topological_order_np: Optional[np.ndarray] = None
        self._link_joint_axes_np: Optional[np.ndarray] = None
        self._link_joint_origins_np: Optional[np.ndarray] = None
        self._link_joint_types_np: Optional[np.ndarray] = None
        self._parent_link_indices_np: Optional[np.ndarray] = None
        self._link_trimesh_meshes: Optional[Dict[str, trimesh.Trimesh]] = None

    def _collect_descendant_links(self, root: str) -> Set[str]:
        links: Set[str] = {root}
        stack: List[str] = [root]
        while stack:
            current: str = stack.pop()
            # add every child link of the current link
            for joint in self.joint_map.values():
                if joint.parent_link_name == current:
                    child: str = joint.child_link_name
                    if child not in links:
                        links.add(child)
                        stack.append(child)
        return links

    def _collect_ancestor_links(self, leaf: str) -> Set[str]:
        ancestors: Set[str] = {leaf}
        current: str = leaf
        while current != self.base_link_name:
            parent_joint = self.joint_map[self.link_map[current].joint_name]
            current = parent_joint.parent_link_name
            ancestors.add(current)
        return ancestors

    def parse_urdf(self) -> Tuple[Dict[str, Joint], Dict[str, Link]]:
        def urdf_str_to_joint_type(joint_type_str: str) -> JointType:
            if joint_type_str == "fixed":
                return JointType.FIXED
            elif joint_type_str == "prismatic":
                return JointType.PRISMATIC
            elif joint_type_str == "revolute":
                return JointType.REVOLUTE
            else:
                raise ValueError(f"Unknown joint type: {joint_type_str}")

        def build_joint_from_urdf(joint_spec: yourdfpy.urdf.Joint) -> Joint:
            joint_type = urdf_str_to_joint_type(joint_spec.type)
            if (
                joint_spec.limit is not None
                and joint_spec.limit.lower is not None
                and joint_spec.limit.upper is not None
            ):
                limit = np.array([joint_spec.limit.lower, joint_spec.limit.upper], dtype=np.float32)
            else:
                limit = None
            origin = joint_spec.origin if joint_spec.origin is not None else np.eye(4, dtype=np.float32)
            return Joint(
                name=joint_spec.name,
                type=joint_type,
                origin=origin.astype(np.float32),
                axis=joint_spec.axis.astype(np.float32),
                limit=limit,
                parent_link_name=joint_spec.parent,
                child_link_name=joint_spec.child,
                mimic_joint=None if joint_spec.mimic is None else joint_spec.mimic.joint,
                mimic_multiplier=None if joint_spec.mimic is None else joint_spec.mimic.multiplier,
                mimic_offset=None if joint_spec.mimic is None else joint_spec.mimic.offset,
            )

        def build_geometry_from_urdf(
            urdf_geometry: yourdfpy.urdf.Geometry, mesh_dir: str, use_collision_geometry: bool = False
        ) -> Geometry:
            if urdf_geometry.box is not None:
                return Box(size=urdf_geometry.box.size.tolist())
            elif urdf_geometry.cylinder is not None:
                return Cylinder(radius=urdf_geometry.cylinder.radius, length=urdf_geometry.cylinder.length)
            elif urdf_geometry.sphere is not None:
                return Sphere(radius=urdf_geometry.sphere.radius)
            elif urdf_geometry.mesh is not None:
                scale_spec = urdf_geometry.mesh.scale
                if isinstance(scale_spec, float):
                    scale: List[float] = [scale_spec, scale_spec, scale_spec]
                elif isinstance(scale_spec, np.ndarray):
                    scale = scale_spec.tolist()
                elif scale_spec is None:
                    scale = [1.0, 1.0, 1.0]
                else:
                    raise ValueError(f"Unknown scale type: {scale_spec}")
                return Mesh(
                    filename=urdf_geometry.mesh.filename,
                    mesh_dir=mesh_dir,
                    scale=scale,
                    is_collision_geometry=use_collision_geometry,
                )
            else:
                raise ValueError(f"Unknown geometry type: {urdf_geometry}")

        def build_material_from_urdf(urdf_material: yourdfpy.urdf.Material) -> Material:
            return Material(
                name=urdf_material.name,
                color=urdf_material.color.rgba if urdf_material.color is not None else None,
                texture=urdf_material.texture.filename if urdf_material.texture is not None else None,
            )

        def build_link_from_urdf(link_spec: yourdfpy.urdf.Link, mesh_dir: str) -> Link:
            link = Link(name=link_spec.name)
            for visual_spec in link_spec.visuals:
                assert visual_spec.geometry is not None, f"Visual {visual_spec.name} has no geometry"
                if visual_spec.origin is None:
                    origin = np.eye(4, dtype=np.float32)
                else:
                    origin = visual_spec.origin
                visual = Visual(
                    origin=origin,
                    geometry=build_geometry_from_urdf(
                        visual_spec.geometry, mesh_dir=mesh_dir, use_collision_geometry=False
                    ),
                    name=visual_spec.name,
                    material=build_material_from_urdf(visual_spec.material)
                    if visual_spec.material is not None
                    else None,
                )
                link.visuals.append(visual)
            for collision_spec in link_spec.collisions:
                if collision_spec.origin is None:
                    origin = np.eye(4, dtype=np.float32)
                else:
                    origin = collision_spec.origin
                collision = Collision(
                    origin=origin,
                    geometry=build_geometry_from_urdf(
                        collision_spec.geometry, mesh_dir=mesh_dir, use_collision_geometry=True
                    ),
                    name=collision_spec.name,
                )
                link.collisions.append(collision)
            return link

        # parse URDF
        urdf = yourdfpy.URDF.load(
            self.urdf_or_mjcf_path,
            load_meshes=False,
            build_scene_graph=False,
            mesh_dir=self.mesh_dir,
            filename_handler=yourdfpy.filename_handler_null,
        )

        # build joint maps
        joint_map: Dict[str, Joint] = {
            joint_name: build_joint_from_urdf(joint_spec) for joint_name, joint_spec in urdf.joint_map.items()
        }
        # infer base link name
        link_names: List[str] = list(urdf.link_map.keys())
        for joint in joint_map.values():
            if joint.child_link_name in link_names:
                link_names.remove(joint.child_link_name)
        if len(link_names) != 1:
            raise ValueError(f"Expected exactly one base link, got {len(link_names)}")
        base_link_name = link_names[0]
        # add a root joint for base link
        joint_map[ROOT_JOINT_NAME] = Joint(
            name=ROOT_JOINT_NAME,
            type=JointType.ROOT,
            origin=np.eye(4, dtype=np.float32),
            axis=np.zeros(3, dtype=np.float32),
            limit=np.array([0.0, 0.0], dtype=np.float32),
            parent_link_name="",
            child_link_name=base_link_name,
        )

        # build link maps
        link_map = {
            link_name: build_link_from_urdf(link_spec, mesh_dir=self.mesh_dir)
            for link_name, link_spec in urdf.link_map.items()
        }
        # set parent joint names for links
        for joint_name, joint in joint_map.items():
            link_map[joint.child_link_name].set_joint_name(joint_name)

        return joint_map, link_map

    def parse_mjcf(self) -> Tuple[Dict[str, Joint], Dict[str, Link]]:
        def is_collision_geometry(geom_spec) -> Optional[bool]:
            if geom_spec.contype is None or geom_spec.conaffinity is None:
                return None
            return geom_spec.contype ^ geom_spec.conaffinity

        def build_geometry_from_mjcf(geom_spec, use_collision_geometry: bool = True) -> Geometry:
            if geom_spec.type == "box":
                return Box(size=geom_spec.size * 2)
            elif geom_spec.type == "cylinder":
                raise NotImplementedError("Cylinder geometry is not supported in MJCF")
            elif geom_spec.type == "mesh" or geom_spec.mesh is not None:
                scale_spec = geom_spec.mesh.scale
                if isinstance(scale_spec, float):
                    scale: List[float] = [scale_spec, scale_spec, scale_spec]
                elif isinstance(scale_spec, np.ndarray):
                    scale = scale_spec.tolist()
                elif scale_spec is None:
                    scale = [1.0, 1.0, 1.0]
                else:
                    raise ValueError(f"Unknown scale type: {scale_spec}")
                mesh: trimesh.Trimesh = trimesh.load(  # type: ignore
                    trimesh.util.wrap_as_stream(geom_spec.mesh.file.contents),
                    file_type=geom_spec.mesh.file.extension.replace(".", ""),
                    force="mesh",
                    skip_materials=use_collision_geometry,
                )
                mesh.apply_scale(scale)
                return Mesh(scale=scale, _scaled_trimesh_mesh=mesh, is_collision_geometry=use_collision_geometry)
            elif geom_spec.type == "capsule":
                return Capsule(radius=geom_spec.size[0], length=geom_spec.size[1] * 2)
            elif geom_spec.type == "sphere" or geom_spec.type is None:
                return Sphere(radius=geom_spec.size)
            else:
                raise ValueError(f"Unknown geometry type: {geom_spec.type}")

        def build_pose_from_mjcf(quat: Optional[np.ndarray], pos: Optional[np.ndarray]) -> np.ndarray:
            # rot_mat = quaternion_to_matrix(to_torch(quat)) if quat is not None else torch.eye(3)
            # return to_numpy(rot_tl_to_tf_mat(rot_mat=rot_mat, tl=to_torch(pos)))
            rot_mat = transforms3d.quaternions.quat2mat(quat) if quat is not None else np.eye(3)
            tf_mat = np.eye(4)
            tf_mat[:3, :3] = rot_mat
            tf_mat[:3, 3] = pos if pos is not None else 0.0
            return tf_mat

        def build_link_from_mjcf(link_spec) -> Link:
            link = Link(name=link_spec.name)
            for geom in link_spec.geom:
                origin = build_pose_from_mjcf(geom.quat, geom.pos)
                is_collision = is_collision_geometry(geom)
                if is_collision is None or is_collision:
                    collision = Collision(
                        origin=origin,
                        geometry=build_geometry_from_mjcf(geom, use_collision_geometry=True),
                        name=geom.name,
                    )
                    link.collisions.append(collision)
                elif is_collision is None or not is_collision:
                    visual = Visual(origin=origin, geometry=build_geometry_from_mjcf(geom), name=geom.name)
                    link.visuals.append(visual)
            return link

        def mjcf_str_to_joint_type(joint_type_str: Optional[str] = "hinge") -> JointType:
            # https://mujoco.readthedocs.io/en/stable/XMLreference.html#body-joint
            if joint_type_str == "fixed":
                return JointType.FIXED
            elif joint_type_str == "slide":
                return JointType.PRISMATIC
            elif joint_type_str == "hinge" or joint_type_str is None:
                return JointType.REVOLUTE
            else:
                raise ValueError(f"Unknown joint type: {joint_type_str}")

        def build_joint_from_mjcf(joint_spec, origin: np.ndarray, parent_link_name: str, child_link_name: str) -> Joint:
            joint_type = mjcf_str_to_joint_type(joint_spec.type)
            if joint_spec.range is not None:
                limit = np.asarray(joint_spec.range, dtype=np.float32)
            else:
                limit = None
            if joint_spec.axis is None:
                axis = np.asarray([0.0, 0.0, 1.0], dtype=np.float32)
            else:
                axis = np.asarray(joint_spec.axis, dtype=np.float32)
            return Joint(
                name=joint_spec.name,
                type=joint_type,
                origin=np.asarray(origin, dtype=np.float32),
                axis=axis,
                limit=limit,
                parent_link_name=parent_link_name,
                child_link_name=child_link_name,
            )

        try:
            import warnings

            from absl import flags

            # ignore annoying warning from dm_control
            warnings.filterwarnings("ignore", message=".*X11: The DISPLAY environment variable is missing.*")

            for name in list(flags.FLAGS):
                if "pymjcf" in name:
                    delattr(flags.FLAGS, name)

            import dm_control.mjcf
        except ImportError:
            raise ImportError("dm_control is required to parse MJCF files, please install by `pip install dm_control`")

        # The mjcf file by IsaacGym does not follow the convention of mujoco mjcf precisely
        # We need to handle it separately when the mjcf file is not valid by normal mjcf parser
        try:
            with open(self.urdf_or_mjcf_path, "r") as f:
                mjcf = dm_control.mjcf.from_file(f, assets=self.mjcf_assets, model_dir=self.mesh_dir)
        except KeyError:
            file_root = os.path.dirname(self.urdf_or_mjcf_path)
            tree = etree.parse(self.urdf_or_mjcf_path)  # type: ignore
            root = tree.getroot()
            invalid_includes = root.findall("*/include")
            for include in invalid_includes:
                parent = include.getparent()
                file: str = include.get("file")
                child_xml = etree.parse(os.path.join(file_root, file)).getroot().getchildren()  # type: ignore
                parent.remove(include)
                parent.extend(child_xml)

            xml_string = etree.tostring(tree)
            mjcf = dm_control.mjcf.from_xml_string(xml_string, model_dir=self.mesh_dir)

        # Substitute geom with default values
        for geom in mjcf.find_all("geom"):
            dm_control.mjcf.commit_defaults(geom)

        base_link_spec = mjcf.worldbody.body[0]  # type: ignore
        base_link_name = str(base_link_spec.name)

        link_map: Dict[str, Link] = {}
        joint_map: Dict[str, Joint] = {}
        link_specs = [(base_link_spec, "")]
        while link_specs:
            link_spec, parent_link_name = link_specs.pop()
            link_map[link_spec.name] = build_link_from_mjcf(link_spec)
            if len(link_spec.joint) > 0:
                if len(link_spec.joint) > 1:
                    raise ValueError(f"Link {link_spec.name} has multiple joints")
                joint_map[link_spec.joint[0].name] = build_joint_from_mjcf(
                    link_spec.joint[0],
                    origin=build_pose_from_mjcf(link_spec.quat, link_spec.pos),
                    parent_link_name=parent_link_name,
                    child_link_name=link_spec.name,
                )
                link_map[link_spec.name].set_joint_name(link_spec.joint[0].name)
            else:
                fixed_joint = Joint(
                    name=f"{link_spec.name}_fixed",
                    type=JointType.FIXED,
                    origin=np.eye(4, dtype=np.float32),
                    axis=np.zeros(3, dtype=np.float32),
                    limit=np.array([0.0, 0.0], dtype=np.float32),
                    parent_link_name=parent_link_name,
                    child_link_name=link_spec.name,
                )
                joint_map[fixed_joint.name] = fixed_joint
                link_map[link_spec.name].set_joint_name(fixed_joint.name)
            link_specs.extend([(child_link, link_spec.name) for child_link in link_spec.body])
        # add a root joint for base link
        joint_map[ROOT_JOINT_NAME] = Joint(
            name=ROOT_JOINT_NAME,
            type=JointType.ROOT,
            origin=np.eye(4, dtype=np.float32),
            axis=np.zeros(3, dtype=np.float32),
            limit=np.array([0.0, 0.0], dtype=np.float32),
            parent_link_name="",
            child_link_name=base_link_name,
        )
        link_map[base_link_name].set_joint_name(ROOT_JOINT_NAME)
        return joint_map, link_map

    def __repr__(self) -> str:
        repr_str = f"ArticulationSpec(filename={os.path.basename(self.urdf_or_mjcf_path)}, num_dofs={self.num_dofs}, num_links={self.num_links})\n"

        def _joint_type_str(joint_type: JointType) -> str:
            if joint_type == JointType.FIXED:
                return "F"
            elif joint_type == JointType.PRISMATIC:
                return "P"
            elif joint_type == JointType.REVOLUTE:
                return "R"
            elif joint_type == JointType.ROOT:
                return "*"
            return "?"

        def _chain_str(link_name: str, prefix: str = "", is_last: bool = True) -> str:
            current_prefix = "└──" if is_last else "├──"
            next_prefix = prefix + ("  " if is_last else "│ ")

            # Get joint info for current link
            joint = self.joint_map[self.link_map[link_name].joint_name]
            joint_type = _joint_type_str(joint.type)

            # Format link name with joint type
            chain_str = f"{prefix}{current_prefix} {link_name} ({joint.name}, {joint_type})\n"

            # Get and sort child joints
            child_joints = [(j_name, j) for j_name, j in self.joint_map.items() if j.parent_link_name == link_name]

            for i, (_, joint) in enumerate(child_joints):
                is_last_child = i == len(child_joints) - 1
                chain_str += _chain_str(joint.child_link_name, next_prefix, is_last_child)

            return chain_str

        repr_str += _chain_str(self.base_link_name, "")
        return repr_str

    def __str__(self) -> str:
        return self.__repr__()

    @property
    def joint_limits(self) -> Optional[Float[np.ndarray, "num_dofs 2"]]:
        return self._joint_limits_np

    @property
    def mimic_joint_limits(self) -> Optional[Float[np.ndarray, "num_mimic_joints 2"]]:
        return self._mimic_joint_limits_np

    @property
    def mimic_joint_indices(self) -> Int[np.ndarray, "num_mimic_joints"]:
        return self._mimic_joint_indices_np

    @property
    def mimic_multipliers(self) -> Float[np.ndarray, "num_mimic_joints"]:
        return self._mimic_multipliers_np

    @property
    def mimic_offsets(self) -> Float[np.ndarray, "num_mimic_joints"]:
        return self._mimic_offsets_np

    @property
    def link_joint_indices(self) -> Int[np.ndarray, "num_links"]:
        if self._link_joint_indices_np is None:
            link_joint_indices = []
            for link_name in self.link_names:
                joint_name = self.link_map[link_name].joint_name
                if joint_name not in self.full_joint_names:
                    link_joint_indices.append(-1)
                else:
                    link_joint_indices.append(self.full_joint_names.index(joint_name))
            self._link_joint_indices_np = np.array(link_joint_indices, dtype=np.int32)
        return self._link_joint_indices_np

    @property
    def link_indices_topological_order(self) -> Int[np.ndarray, "num_links"]:
        if self._link_indices_topological_order_np is None:
            link_indices = [self.link_names.index(link_name) for link_name in self._link_names_topological_order]
            self._link_indices_topological_order_np = np.array(link_indices, dtype=np.int32)
        return self._link_indices_topological_order_np

    @property
    def parent_link_indices(self) -> Int[np.ndarray, "num_links"]:
        if self._parent_link_indices_np is None:
            parent_link_indices = []
            for link_name in self.link_names:
                joint = self.joint_map[self.link_map[link_name].joint_name]
                if joint.type == JointType.ROOT:
                    parent_link_indices.append(-1)
                else:
                    parent_link_indices.append(self.link_names.index(joint.parent_link_name))
            self._parent_link_indices_np = np.array(parent_link_indices, dtype=np.int32)
        return self._parent_link_indices_np

    @property
    def link_joint_axes(self) -> Optional[Float[np.ndarray, "num_links 3"]]:
        if self._link_joint_axes_np is None:
            link_joint_axes = [
                self.joint_map[self.link_map[link_name].joint_name].axis for link_name in self.link_names
            ]
            self._link_joint_axes_np = np.stack(link_joint_axes, axis=0)
        return self._link_joint_axes_np

    @property
    def full_joint_axes(self) -> Float[np.ndarray, "num_full_joints 3"]:
        if self._full_joint_axes_np is None:
            full_joint_axes = [self.joint_map[joint_name].axis for joint_name in self.full_joint_names]
            self._full_joint_axes_np = np.stack(full_joint_axes, axis=0)
        return self._full_joint_axes_np

    @property
    def link_joint_origins(self) -> Float[np.ndarray, "num_links 4 4"]:
        if self._link_joint_origins_np is None:
            link_joint_origins = [
                self.joint_map[self.link_map[link_name].joint_name].origin for link_name in self.link_names
            ]
            self._link_joint_origins_np = np.stack(link_joint_origins, axis=0)
        return self._link_joint_origins_np

    @property
    def link_joint_types(self) -> Int[np.ndarray, "num_links"]:
        if self._link_joint_types_np is None:
            link_joint_types = [
                self.joint_map[self.link_map[link_name].joint_name].type.value for link_name in self.link_names
            ]
            self._link_joint_types_np = np.array(link_joint_types, dtype=np.int32)
        return self._link_joint_types_np

    @lru_cache(maxsize=None)
    def get_ancestor_links_mask(self, link_name_or_idx: Union[str, int]) -> Int[np.ndarray, "num_links"]:
        link_name = self.link_names[link_name_or_idx] if isinstance(link_name_or_idx, int) else link_name_or_idx
        ancestor_link_names = self._collect_ancestor_links(link_name)
        ancestor_link_indices = [self.link_names.index(ln) for ln in ancestor_link_names]
        return cast(np.ndarray, np.isin(np.arange(len(self.link_names)), ancestor_link_indices))

    def get_link_trimesh_meshes(
        self, mode: Literal["visual", "collision"] = "collision", return_empty_meshes: bool = True
    ) -> Dict[str, trimesh.Trimesh]:
        if self._link_trimesh_meshes is None:
            self._link_trimesh_meshes = {
                link_name: self.link_map[link_name].get_trimesh_mesh(mode=mode) for link_name in self.link_names
            }
        if not return_empty_meshes:
            return {n: m for n, m in self._link_trimesh_meshes.items() if len(m.vertices) > 0 and len(m.faces) > 0}
        else:
            return self._link_trimesh_meshes
