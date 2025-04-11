from typing import List, Optional, Sequence, Union

import numpy as np
import pinocchio as pin
from beartype import beartype
from jaxtyping import Float

from fastdev.robo.articulation import Articulation, Device
from fastdev.robo.articulation_spec import ArticulationSpec


@beartype
class SingleCPUArticulation(Articulation):
    """Use Pinocchio as the backend for single articulation."""

    def __init__(self, spec: Union[ArticulationSpec, Sequence[ArticulationSpec]], device: Device = "cpu"):
        if isinstance(spec, Sequence):
            if len(spec) != 1:
                raise ValueError(f"Expected a single articulation spec, got {len(spec)}")
            spec = spec[0]
        if device != "cpu":
            raise ValueError(f"Only CPU is supported for SingleCPUArticulation, got {device}")
        super().__init__([spec], device=device)

        # ------------------------------ pinocchio ------------------------------
        if self.first_spec.format != "urdf":
            raise ValueError(f"Only URDF is supported for single articulation, got {self.first_spec.format}")
        self.pin_model = pin.buildModelFromUrdf(self.first_spec.urdf_or_mjcf_path)
        self.pin_data = pin.Data(self.pin_model)
        if self.pin_model.nq != self.first_spec.num_full_joints:
            raise ValueError(
                f"Number of degrees of freedom mismatch: pinocchio model has {self.pin_model.nq} DOFs, but spec has {self.first_spec.num_full_joints} joints."
            )
        self._ours_to_pin_joint_indices = [
            self.first_spec.full_joint_names.index(name)
            for name in self.pin_model.names[1:]  # skip `universe`
        ]

    def forward_kinematics_pinocchio(
        self,
        joint_values: Float[np.ndarray, "num_dofs"],  # noqa: F821
        joint_names: Optional[List[str]] = None,
        root_poses: Optional[Float[np.ndarray, "4 4"]] = None,
        clamp_joint_values: bool = True,
    ) -> Float[np.ndarray, "num_links 4 4"]:
        """Forward kinematics using Pinocchio.

        Args:
            joint_values (np.ndarray): Active joint values of shape (num_dofs,).
            joint_names (List[str], optional): Names corresponding to the joint_values.
                If provided, values will be reordered to match the internal active joint order.
            root_poses (np.ndarray, optional): Root pose transformation of shape (4, 4). Defaults to identity.
            clamp_joint_values (bool, optional): Whether to clamp joint values to joint limits. Defaults to True.

        Returns:
            np.ndarray: Link poses in the world frame of shape (num_links, 4, 4).
        """
        if joint_values.shape != (self.first_spec.num_dofs,):
            raise ValueError(f"Expected joint_values shape ({self.first_spec.num_dofs},), got {joint_values.shape}")
        active_joint_values = joint_values.copy()
        if joint_names is not None:
            if len(joint_names) != self.first_spec.num_dofs:
                raise ValueError(
                    f"Length mismatch: joint_names ({len(joint_names)}) vs num_dofs ({self.first_spec.num_dofs})"
                )
            if joint_names != self.first_spec.active_joint_names:
                reorder_indices = [joint_names.index(name) for name in self.first_spec.active_joint_names]
                active_joint_values = active_joint_values[reorder_indices]
        if clamp_joint_values and self.first_spec.joint_limits is not None:
            limits = self.first_spec.joint_limits
            active_joint_values = np.clip(active_joint_values, limits[:, 0], limits[:, 1])
        full_joint_values = self.apply_mimic_joints_numpy(active_joint_values, clamp_joint_values=clamp_joint_values)

        pin.forwardKinematics(self.pin_model, self.pin_data, full_joint_values[self._ours_to_pin_joint_indices])
        pin.updateFramePlacements(self.pin_model, self.pin_data)

        link_poses_list = [
            self.pin_data.oMf[self.pin_model.getFrameId(lname)].homogeneous for lname in self.first_spec.link_names
        ]
        link_poses = np.stack(link_poses_list, axis=0).astype(np.float32)

        if root_poses is not None:
            final_poses = root_poses @ link_poses
        else:
            final_poses = link_poses

        return final_poses
