# ruff: noqa: F821
from typing import TYPE_CHECKING, Optional, Tuple, Union

import torch
from einops import rearrange
from jaxtyping import Float, Int, Bool

from fastdev.xform.rotation import (
    axis_angle_to_matrix,
    matrix_to_quaternion,
    quaternion_invert,
    quaternion_multiply,
    quaternion_to_axis_angle_vector,
)
from fastdev.xform.transforms import rot_tl_to_tf_mat

if TYPE_CHECKING:
    from fastdev.robo.articulation import Articulation


def forward_kinematics(
    joint_values: Float[torch.Tensor, "... total_num_joints"],
    articulation: "Articulation",
    root_poses: Optional[Float[torch.Tensor, "... num_arti 4 4"]] = None,
) -> Float[torch.Tensor, "... total_num_links 4 4"]:
    batch_shape = joint_values.shape[:-1]
    total_num_links = articulation.total_num_links
    device = joint_values.device
    requires_grad = joint_values.requires_grad or (root_poses is not None and root_poses.requires_grad)

    link_poses = torch.eye(4, device=device, requires_grad=requires_grad).repeat(*batch_shape, total_num_links, 1, 1)

    if root_poses is None:
        root_poses = torch.eye(4, device=device).expand(*batch_shape, articulation.num_arti, 4, 4)

    joint_axes = articulation.get_packed_full_joint_axes(return_tensors="pt")
    pris_jnt_tf = rot_tl_to_tf_mat(tl=joint_axes * joint_values.unsqueeze(-1))  # type: ignore
    rev_jnt_tf = rot_tl_to_tf_mat(rot_mat=axis_angle_to_matrix(joint_axes, joint_values))  # type: ignore

    link_topo_indices = articulation.get_packed_link_indices_topological_order(return_tensors="pt")
    parent_link_indices = articulation.get_packed_parent_link_indices(return_tensors="pt")
    link_joint_types = articulation.get_packed_link_joint_types(return_tensors="pt")
    link_joint_indices = articulation.get_packed_link_joint_indices(return_tensors="pt")
    link_joint_origins = articulation.get_packed_link_joint_origins(return_tensors="pt")
    joint_first_indices = articulation.get_joint_first_indices(return_tensors="pt")
    link_first_indices = articulation.get_link_first_indices(return_tensors="pt")

    identity_matrix = torch.eye(4, device=device).expand(*batch_shape, 4, 4)
    for arti_idx in range(articulation.num_arti):
        link_start = link_first_indices[arti_idx].item()
        link_end = (
            link_first_indices[arti_idx + 1].item()
            if arti_idx < len(link_first_indices) - 1
            else len(link_topo_indices)
        )
        joint_start = joint_first_indices[arti_idx].item()

        for local_link_idx in link_topo_indices[link_start:link_end]:  # type: ignore
            glb_link_idx = local_link_idx + link_start
            joint_type = link_joint_types[glb_link_idx]
            if joint_type == -1:  # Root link
                link_poses[..., glb_link_idx, :, :] = root_poses[..., arti_idx, :, :]
                continue
            glb_parent_idx = parent_link_indices[glb_link_idx] + link_start
            parent_pose = link_poses[..., glb_parent_idx, :, :]
            if joint_type == 1:  # Prismatic
                glb_joint_idx = link_joint_indices[glb_link_idx] + joint_start
                local_tf = pris_jnt_tf[..., glb_joint_idx, :, :]
            elif joint_type == 2:  # Revolute
                glb_joint_idx = link_joint_indices[glb_link_idx] + joint_start
                local_tf = rev_jnt_tf[..., glb_joint_idx, :, :]
            else:  # Fixed
                local_tf = identity_matrix
            origin = link_joint_origins[glb_link_idx]
            link_poses[..., glb_link_idx, :, :] = (parent_pose @ origin) @ local_tf
    return link_poses


def calculate_jacobian(
    joint_values: Float[torch.Tensor, "... total_num_joints"],
    target_link_indices: Int[torch.Tensor, "num_arti"],
    articulation: "Articulation",
    root_poses: Optional[Float[torch.Tensor, "... num_arti 4 4"]] = None,
    return_target_link_poses: bool = False,
) -> Union[
    Float[torch.Tensor, "... 6 total_num_joints"],
    Tuple[Float[torch.Tensor, "... 6 total_num_joints"], Float[torch.Tensor, "... num_arti 4 4"]],
]:
    """Calculate the geometric Jacobian for the end-effector for each joint in the articulated robot.

    The Jacobian is computed in the world frame. For revolute joints, the linear velocity component
    is computed as the cross product of the joint axis (in world frame) and the vector from the joint
    position to the end-effector position, while the angular velocity component is the joint axis.
    For prismatic joints, the linear velocity component is the joint axis and the angular component is zero.
    """
    batch_shape = joint_values.shape[:-1]
    device = joint_values.device

    # compute full forward kinematics for all links
    link_poses = forward_kinematics(joint_values, articulation, root_poses=root_poses)
    total_num_joints = joint_values.shape[-1]
    jacobian = torch.zeros(*batch_shape, 6, total_num_joints, device=device, dtype=joint_values.dtype)

    # extract articulation parameters
    joint_axes = articulation.get_packed_full_joint_axes(return_tensors="pt")  # (total_num_joints, 3)
    link_joint_types = articulation.get_packed_link_joint_types(return_tensors="pt")  # (total_num_links,)
    link_joint_indices = articulation.get_packed_link_joint_indices(return_tensors="pt")  # (total_num_links,)
    link_joint_origins = articulation.get_packed_link_joint_origins(return_tensors="pt")  # (total_num_links, 4, 4)
    parent_link_indices = articulation.get_packed_parent_link_indices(return_tensors="pt")  # (total_num_links,)
    joint_first_indices = articulation.get_joint_first_indices(return_tensors="pt")  # (num_arti,)
    link_first_indices = articulation.get_link_first_indices(return_tensors="pt")  # (num_arti,)
    ancestor_link_masks: torch.Tensor = articulation.get_packed_ancestor_links_mask(  # type: ignore
        target_link_indices, return_tensors="pt"
    )  # (total_num_links,)

    total_num_links = articulation.total_num_links
    num_arti = articulation.num_arti

    if return_target_link_poses:
        target_link_poses = torch.zeros(*batch_shape, num_arti, 4, 4, device=device, dtype=joint_values.dtype)

    for arti_idx in range(num_arti):
        # determine the link and joint index ranges for the current articulation
        link_start = int(link_first_indices[arti_idx].item())
        link_end = int(link_first_indices[arti_idx + 1].item()) if arti_idx < num_arti - 1 else total_num_links
        joint_start = int(joint_first_indices[arti_idx].item())

        # select the designated end-effector for this articulation and extract its position
        eef_idx = target_link_indices[arti_idx] + link_start
        eef_pose = link_poses[..., eef_idx, :, :]
        if return_target_link_poses:
            target_link_poses[..., arti_idx, :, :] = eef_pose
        p_eef = eef_pose[..., :3, 3]

        # identify ancestor links using the respective mask
        link_mask = ancestor_link_masks[link_start:link_end]  # (L,)
        valid_local_links = torch.nonzero(link_mask, as_tuple=True)[0]
        if valid_local_links.numel() == 0:
            continue
        valid_global_links = valid_local_links + link_start

        # filter for joints that are either prismatic (1) or revolute (2)
        joint_types = link_joint_types[valid_global_links].to(torch.int64)  # (N,)
        valid_joint_mask = (joint_types == 1) | (joint_types == 2)
        if valid_joint_mask.sum() == 0:
            continue
        valid_global_links = valid_global_links[valid_joint_mask]
        joint_types = joint_types[valid_joint_mask]
        joint_ids = (link_joint_indices[valid_global_links] + joint_start).long()

        # gather parent's transformation for valid links
        parent_indices = parent_link_indices[valid_global_links] + link_start
        parent_pose = torch.index_select(link_poses, dim=-3, index=parent_indices)
        origin_tf = link_joint_origins[valid_global_links].view(*(1,) * len(batch_shape), -1, 4, 4)
        joint_tf = parent_pose @ origin_tf
        p_joint = joint_tf[..., :3, 3]
        R_joint = joint_tf[..., :3, :3]

        # transform local joint axis into the world frame
        local_axis = joint_axes[joint_ids].view(*(1,) * len(batch_shape), -1, 3)  # type: ignore
        axis_world = torch.matmul(R_joint, local_axis.unsqueeze(-1)).squeeze(-1)

        diff = p_eef.unsqueeze(-2) - p_joint
        is_revolute = joint_types == 2
        rev_mask = is_revolute.view(*(1,) * len(batch_shape), -1, 1).to(joint_values.dtype)
        # for revolute joints, compute linear velocity using cross product; for prismatic, use direct axis
        lin_component = torch.cross(axis_world, diff, dim=-1) * rev_mask + axis_world * (1 - rev_mask)
        ang_component = axis_world * rev_mask
        update = torch.cat((lin_component, ang_component), dim=-1)  # shape: (*batch, N, 6)

        jacobian[..., :, joint_ids] = rearrange(update, "... n m -> ... m n")

    if return_target_link_poses:
        return jacobian, target_link_poses
    else:
        return jacobian


@torch.no_grad()
def delta_pose(T_current: torch.Tensor, pos_target: torch.Tensor, quat_target: torch.Tensor) -> torch.Tensor:
    """Compute the error between current and target poses."""
    pos_error = pos_target - T_current[..., :3, 3]
    current_quat = matrix_to_quaternion(T_current[..., :3, :3])
    quat_err = quaternion_multiply(quat_target, quaternion_invert(current_quat))
    rot_error = quaternion_to_axis_angle_vector(quat_err)
    return torch.cat([pos_error, rot_error], dim=-1)  # shape (..., 6)


@torch.no_grad()
def inverse_kinematics(
    target_link_poses: Float[torch.Tensor, "... num_arti 4 4"],
    target_link_indices: Int[torch.Tensor, "num_arti"],
    articulation: "Articulation",
    max_iterations: int = 100,
    learning_rate: float = 0.1,
    tolerance: float = 1e-6,
    damping: float = 0.01,
    num_retries: int = 50,
    init_joint_values: Optional[Float[torch.Tensor, "... total_num_dofs"]] = None,
    jitter_strength: float = 1.0,
) -> Tuple[Float[torch.Tensor, "... total_num_dofs"], Bool[torch.Tensor, "... num_arti"]]:
    batch_shape = target_link_poses.shape[:-3]
    device = target_link_poses.device
    num_arti = articulation.num_arti
    total_num_dofs = articulation.total_num_dofs

    if init_joint_values is None:
        init_joint_values = (
            articulation.get_packed_zero_joint_values(return_tensors="pt").expand(*batch_shape, -1).clone()  # type: ignore
        )
    if not articulation.has_none_joint_limits:
        lower_limit, upper_limit = articulation.joint_limits[..., 0], articulation.joint_limits[..., 1]  # type: ignore
        lower_q_init = (lower_limit - init_joint_values) * jitter_strength + init_joint_values
        upper_q_init = (upper_limit - init_joint_values) * jitter_strength + init_joint_values
        lower_q_init = lower_q_init.unsqueeze(-2)  # add a retry dimension
        upper_q_init = upper_q_init.unsqueeze(-2)
        q_init = lower_q_init + (upper_q_init - lower_q_init) * torch.rand(
            *batch_shape, num_retries, total_num_dofs, device=device, dtype=target_link_poses.dtype
        )
    else:
        # NOTE use a small range of 0.1 when joint limits are not specified
        lower_q_init = init_joint_values - 0.1
        upper_q_init = init_joint_values + 0.1
        lower_q_init = lower_q_init.unsqueeze(-2)  # add a retry dimension
        upper_q_init = upper_q_init.unsqueeze(-2)
        q_init = lower_q_init + (upper_q_init - lower_q_init) * torch.rand(
            *batch_shape, num_retries, total_num_dofs, device=device, dtype=target_link_poses.dtype
        )
    q = q_init  # shape: (*batch_shape, num_retries, total_num_dofs)

    pos_target = target_link_poses[..., :3, 3].unsqueeze(-3)  # rely on broadcasting
    quat_target = matrix_to_quaternion(target_link_poses[..., :3, :3]).unsqueeze(-3)

    joint_first_indices_tensor = articulation.get_joint_first_indices(return_tensors="pt")
    joint_limits = articulation.get_packed_joint_limits(return_tensors="pt")

    jfi = joint_first_indices_tensor.tolist()
    joint_slices = [slice(jfi[i], jfi[i + 1]) for i in range(num_arti - 1)] + [slice(jfi[-1], total_num_dofs)]

    for _ in range(max_iterations):
        J, current_poses = calculate_jacobian(q, target_link_indices, articulation, return_target_link_poses=True)
        err = delta_pose(current_poses, pos_target, quat_target)  # shape: (*batch_shape, num_retries, A, 6)
        err_norm = err.norm(dim=-1)  # shape: (*batch_shape, num_retries, A)
        success = (err_norm < tolerance).any(dim=-2)  # shape: (*batch_shape, A)
        if success.all():
            break

        dq_list = []  # collect updates for each joint block
        for i, js in enumerate(joint_slices):
            err_i = err[..., i, :]  # shape: (*batch_shape, num_retries, 6)
            J_i = J[..., js]  # shape: (*batch_shape, num_retries, 6, dofs_i)
            reg = damping * torch.eye(6, device=device, dtype=q.dtype).expand(*J_i.shape[:-2], 6, 6)  # regularize
            err_i_unsq = err_i.unsqueeze(-1)
            JJt_i = J_i @ J_i.transpose(-1, -2) + reg
            A_i = torch.linalg.solve(JJt_i, err_i_unsq)
            dq_i = (J_i.transpose(-1, -2) @ A_i).squeeze(-1)
            dq_list.append(dq_i)
        dq_total = torch.cat(dq_list, dim=-1)
        q = q + learning_rate * dq_total
        if joint_limits is not None:
            q = torch.clamp(q, min=joint_limits[..., 0], max=joint_limits[..., 1])  # type: ignore

    # select the best retry per articulation based on squared error norm
    _, current_poses = calculate_jacobian(q, target_link_indices, articulation, return_target_link_poses=True)
    final_err = delta_pose(current_poses, pos_target, quat_target)  # shape: (*batch_shape, num_retries, A, 6)
    final_err_norm = final_err.norm(dim=-1)  # shape: (*batch_shape, num_retries, A)
    final_success = (final_err_norm < tolerance).any(dim=-2)  # shape: (*batch_shape, A)
    best_idx = final_err_norm.argmin(dim=-2)  # shape: (*batch_shape, A)
    best_q_list = []
    for i, js in enumerate(joint_slices):
        sel = best_idx[..., i].unsqueeze(-1)  # shape: (*batch_shape, 1)
        q_seg = q[..., js]  # shape: (*batch_shape, num_retries, dof_range)
        indices = sel.unsqueeze(-1).expand(*sel.shape, q_seg.shape[-1])
        best_q_list.append(torch.gather(q_seg, dim=-2, index=indices).squeeze(-2))
    best_q = torch.cat(best_q_list, dim=-1)
    return best_q, final_success
