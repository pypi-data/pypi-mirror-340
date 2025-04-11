# mypy: disable-error-code="valid-type"
# ruff: noqa: F821
from typing import TYPE_CHECKING, Any, Optional, Tuple, Union

import numpy as np
import torch
import warp as wp
from jaxtyping import Float, Int, Bool
from warp.fem.linalg import inverse_qr, solve_triangular

from fastdev.xform import matrix_to_quaternion

if TYPE_CHECKING:
    from fastdev.robo.articulation import Articulation


@wp.func
def axis_angle_to_tf_mat(axis: wp.vec3, angle: wp.float32):
    x, y, z = axis[0], axis[1], axis[2]
    s, c = wp.sin(angle), wp.cos(angle)
    C = 1.0 - c

    xs, ys, zs = x * s, y * s, z * s
    xC, yC, zC = x * C, y * C, z * C
    xyC, yzC, zxC = x * yC, y * zC, z * xC

    # fmt: off
    return wp.mat44(
        x * xC + c, xyC - zs, zxC + ys, 0.0,
        xyC + zs, y * yC + c, yzC - xs, 0.0,
        zxC - ys, yzC + xs, z * zC + c, 0.0,
        0.0, 0.0, 0.0, 1.0,
    )
    # fmt: on


@wp.func
def axis_distance_to_tf_mat(axis: wp.vec3, distance: wp.float32):
    x, y, z = axis[0], axis[1], axis[2]
    # fmt: off
    return wp.mat44(
        1.0, 0.0, 0.0, distance * x,
        0.0, 1.0, 0.0, distance * y,
        0.0, 0.0, 1.0, distance * z,
        0.0, 0.0, 0.0, 1.0,
    )
    # fmt: on


@wp.kernel
def forward_kinematics_kernel(
    joint_values: wp.array2d(dtype=wp.float32),  # [b, num_dofs]
    root_poses: wp.array2d(dtype=wp.mat44),  # [b, num_arti, 4, 4], optional
    joint_first_indices: wp.array(dtype=wp.int32),
    link_indices_topological_order: wp.array(dtype=wp.int32),
    parent_link_indices: wp.array(dtype=wp.int32),
    link_joint_indices: wp.array(dtype=wp.int32),
    link_joint_types: wp.array(dtype=wp.int32),
    link_joint_origins: wp.array(dtype=wp.mat44),
    link_joint_axes: wp.array(dtype=wp.vec3),
    link_first_indices: wp.array(dtype=wp.int32),
    link_poses: wp.array2d(dtype=wp.mat44),  # output, [b, num_links]
):
    b_idx, arti_idx = wp.tid()
    joint_first_idx = joint_first_indices[arti_idx]
    link_first_idx = link_first_indices[arti_idx]
    if arti_idx == wp.int32(link_first_indices.shape[0] - 1):
        link_last_idx = wp.int32(link_indices_topological_order.shape[0])
    else:
        link_last_idx = link_first_indices[arti_idx + 1]

    if root_poses.shape[0] > 0:
        root_pose = root_poses[b_idx, arti_idx]
    else:
        root_pose = wp.identity(n=4, dtype=wp.float32)  # type: ignore

    for glb_topo_idx in range(link_first_idx, link_last_idx):
        glb_link_idx = link_indices_topological_order[glb_topo_idx] + link_first_idx
        joint_type = link_joint_types[glb_link_idx]
        if joint_type == -1:  # Root link
            glb_joint_pose = root_pose
        else:  # Non-root links
            glb_parent_link_idx = parent_link_indices[glb_link_idx] + link_first_idx
            parent_link_pose = link_poses[b_idx, glb_parent_link_idx]
            glb_joint_idx = link_joint_indices[glb_link_idx] + joint_first_idx
            if joint_type == 0:
                local_joint_tf = wp.identity(n=4, dtype=wp.float32)  # type: ignore
            elif joint_type == 1:  # prismatic
                joint_value = joint_values[b_idx, glb_joint_idx]
                joint_axis = link_joint_axes[glb_link_idx]
                local_joint_tf = axis_distance_to_tf_mat(joint_axis, joint_value)
            elif joint_type == 2:  # revolute
                joint_value = joint_values[b_idx, glb_joint_idx]
                joint_axis = link_joint_axes[glb_link_idx]
                local_joint_tf = axis_angle_to_tf_mat(joint_axis, joint_value)
            joint_origin = link_joint_origins[glb_link_idx]
            glb_joint_pose = (parent_link_pose @ joint_origin) @ local_joint_tf  # type: ignore
        link_poses[b_idx, glb_link_idx] = glb_joint_pose


_KERNEL_PARAMS_TYPES_AND_GETTERS = {
    "joint_first_indices": (wp.int32, "get_joint_first_indices"),
    "link_indices_topological_order": (wp.int32, "get_packed_link_indices_topological_order"),
    "parent_link_indices": (wp.int32, "get_packed_parent_link_indices"),
    "link_joint_indices": (wp.int32, "get_packed_link_joint_indices"),
    "link_joint_types": (wp.int32, "get_packed_link_joint_types"),
    "link_joint_origins": (wp.mat44, "get_packed_link_joint_origins"),
    "link_joint_axes": (wp.vec3, "get_packed_link_joint_axes"),
    "link_first_indices": (wp.int32, "get_link_first_indices"),
}


class ForwardKinematics(torch.autograd.Function):
    @staticmethod
    def forward(
        ctx,
        joint_values: Float[torch.Tensor, "... total_num_joints"],
        articulation: "Articulation",
        root_poses: Optional[Float[torch.Tensor, "... num_arti 4 4"]] = None,
    ) -> Float[torch.Tensor, "... total_num_links 4 4"]:
        batch_shape = joint_values.shape[:-1]
        total_num_joints = joint_values.shape[-1]
        total_num_links = articulation.total_num_links
        num_arti = articulation.num_arti
        requires_grad = joint_values.requires_grad or (root_poses is not None and root_poses.requires_grad)
        wp.init()

        joint_values_wp = wp.from_torch(
            joint_values.contiguous().view(-1, total_num_joints),
            dtype=wp.float32,
            requires_grad=joint_values.requires_grad,
        )
        root_poses_wp = (
            wp.from_torch(
                root_poses.contiguous().view(-1, num_arti, 4, 4),
                dtype=wp.mat44,
                requires_grad=root_poses.requires_grad,
            )
            if root_poses is not None
            else wp.zeros(shape=(0, 0), dtype=wp.mat44, requires_grad=False, device=joint_values_wp.device)
        )
        link_poses_wp = wp.from_torch(
            torch.zeros(
                (joint_values_wp.shape[0], total_num_links, 4, 4),
                device=joint_values.device,
                dtype=joint_values.dtype,
                requires_grad=requires_grad,
            ),
            dtype=wp.mat44,
            requires_grad=requires_grad,
        )
        wp_params = {
            name: wp.from_torch(getattr(articulation, fn)(return_tensors="pt"), dtype=dtype)
            for name, (dtype, fn) in _KERNEL_PARAMS_TYPES_AND_GETTERS.items()
        }

        wp.launch(
            kernel=forward_kinematics_kernel,
            dim=(joint_values_wp.shape[0], num_arti),
            inputs=[joint_values_wp, root_poses_wp, *wp_params.values()],
            outputs=[link_poses_wp],
            device=joint_values_wp.device,
        )

        if joint_values_wp.requires_grad or root_poses_wp.requires_grad:
            ctx.shapes = (batch_shape, total_num_joints, total_num_links, num_arti)
            ctx.joint_values_wp = joint_values_wp
            ctx.root_poses_wp = root_poses_wp
            ctx.link_poses_wp = link_poses_wp
            ctx.wp_params = wp_params

        return wp.to_torch(link_poses_wp).view(*batch_shape, total_num_links, 4, 4)

    @staticmethod
    def backward(  # type: ignore
        ctx, link_poses_grad: Float[torch.Tensor, "... total_num_links 4 4"]
    ) -> Tuple[
        Optional[Float[torch.Tensor, "... total_num_joints"]],
        None,
        Optional[Float[torch.Tensor, "... num_arti 4 4"]],
    ]:
        if not ctx.joint_values_wp.requires_grad and (not ctx.root_poses_wp.requires_grad):
            return None, None, None
        batch_shape, total_num_joints, total_num_links, num_arti = ctx.shapes

        ctx.link_poses_wp.grad = wp.from_torch(
            link_poses_grad.contiguous().view(-1, total_num_links, 4, 4), dtype=wp.mat44
        )

        wp.launch(
            kernel=forward_kinematics_kernel,
            dim=(ctx.joint_values_wp.shape[0], num_arti),
            inputs=[ctx.joint_values_wp, ctx.root_poses_wp, *ctx.wp_params.values()],
            outputs=[ctx.link_poses_wp],
            adj_inputs=[ctx.joint_values_wp.grad, ctx.root_poses_wp.grad, *([None] * len(ctx.wp_params))],
            adj_outputs=[ctx.link_poses_wp.grad],
            adjoint=True,
            device=ctx.joint_values_wp.device,
        )

        joint_values_grad = (
            wp.to_torch(ctx.joint_values_wp.grad).view(*batch_shape, total_num_joints)
            if ctx.joint_values_wp.requires_grad
            else None
        )
        root_poses_grad = (
            wp.to_torch(ctx.root_poses_wp.grad).view(*batch_shape, num_arti, 4, 4)
            if ctx.root_poses_wp.requires_grad
            else None
        )
        return joint_values_grad, None, root_poses_grad


def forward_kinematics(
    joint_values: Float[torch.Tensor, "... total_num_joints"],
    articulation: "Articulation",
    root_poses: Optional[Float[torch.Tensor, "... num_arti 4 4"]] = None,
) -> Float[torch.Tensor, "... total_num_links 4 4"]:
    return ForwardKinematics.apply(joint_values, articulation, root_poses)


def forward_kinematics_numpy(
    joint_values: Float[np.ndarray, "... total_num_joints"],  # noqa: F821
    articulation: "Articulation",
    root_poses: Optional[Float[np.ndarray, "... num_arti 4 4"]] = None,
) -> Float[np.ndarray, "... total_num_links 4 4"]:
    total_num_joints = joint_values.shape[-1]
    total_num_links = articulation.total_num_links
    num_arti = articulation.num_arti
    wp.init()
    joint_values_wp = wp.from_numpy(
        joint_values.reshape(-1, total_num_joints), dtype=wp.float32, device="cpu"
    )  # [B, num_dofs]
    link_poses_wp = wp.from_numpy(
        np.zeros(
            (joint_values_wp.shape[0], total_num_links, 4, 4),
            dtype=joint_values.dtype,
        ),
        dtype=wp.mat44,
        device="cpu",
    )
    root_poses_wp = (
        wp.from_numpy(root_poses.reshape(-1, num_arti, 4, 4), dtype=wp.mat44, device="cpu")
        if root_poses is not None
        else wp.zeros(shape=(0, 0), dtype=wp.mat44, requires_grad=False, device=joint_values_wp.device)
    )
    wp_params = {
        name: wp.from_numpy(getattr(articulation, fn)("np"), dtype=dtype, device="cpu")
        for name, (dtype, fn) in _KERNEL_PARAMS_TYPES_AND_GETTERS.items()
    }
    wp.launch(
        kernel=forward_kinematics_kernel,
        dim=(joint_values_wp.shape[0], num_arti),
        inputs=[joint_values_wp, root_poses_wp, *wp_params.values()],
        outputs=[link_poses_wp],
        device="cpu",
    )
    return link_poses_wp.numpy().reshape(joint_values.shape[:-1] + (total_num_links, 4, 4))


@wp.kernel
def calculate_jacobian_kernel(
    link_poses: wp.array2d(dtype=wp.mat44),  # [b, total_num_links]
    target_link_indices: wp.array(dtype=wp.int32),  # [num_arti]
    ancestor_mask: wp.array(dtype=wp.int32),  # [total_num_links]
    joint_axes: wp.array(dtype=wp.vec3),  # [total_num_joints]
    link_joint_types: wp.array(dtype=wp.int32),  # [total_num_links]
    link_joint_indices: wp.array(dtype=wp.int32),  # [total_num_links]
    link_joint_origins: wp.array(dtype=wp.mat44),  # [total_num_links]
    parent_link_indices: wp.array(dtype=wp.int32),  # [total_num_links]
    joint_first_indices: wp.array(dtype=wp.int32),  # [num_arti]
    link_first_indices: wp.array(dtype=wp.int32),  # [num_arti]
    jacobian: wp.array3d(dtype=wp.float32),  # [b, 6, total_num_joints]
):
    """Compute the Jacobian using precomputed target link poses."""
    total_num_links = link_joint_types.shape[0]
    b_idx, global_link_idx = wp.tid()

    arti_idx = -1
    num_arti = link_first_indices.shape[0]
    for i in range(num_arti):
        start = link_first_indices[i]
        if i < num_arti - 1:
            end = link_first_indices[i + 1]
        else:
            end = total_num_links
        if global_link_idx >= start and global_link_idx < end:
            arti_idx = i
            break
    if arti_idx == -1:
        return

    if ancestor_mask[global_link_idx] == 0:
        return

    # use the precomputed target link pose instead of computing indices
    target_global_link_idx = target_link_indices[arti_idx] + link_first_indices[arti_idx]
    eef_pose = link_poses[b_idx, target_global_link_idx]
    p_eef = wp.vec3(eef_pose[0, 3], eef_pose[1, 3], eef_pose[2, 3])

    jt = link_joint_types[global_link_idx]
    if jt == -1 or (jt != 1 and jt != 2):
        return
    glb_joint_idx = link_joint_indices[global_link_idx] + joint_first_indices[arti_idx]
    if global_link_idx == link_first_indices[arti_idx]:
        joint_pose = link_poses[b_idx, global_link_idx] @ link_joint_origins[global_link_idx]
    else:
        parent_idx = parent_link_indices[global_link_idx] + link_first_indices[arti_idx]
        joint_pose = link_poses[b_idx, parent_idx] @ link_joint_origins[global_link_idx]

    p_joint = wp.vec3(joint_pose[0, 3], joint_pose[1, 3], joint_pose[2, 3])
    r0 = wp.vec3(joint_pose[0, 0], joint_pose[0, 1], joint_pose[0, 2])
    r1 = wp.vec3(joint_pose[1, 0], joint_pose[1, 1], joint_pose[1, 2])
    r2 = wp.vec3(joint_pose[2, 0], joint_pose[2, 1], joint_pose[2, 2])

    axis_local = joint_axes[glb_joint_idx]
    axis_world = wp.vec3(
        r0[0] * axis_local[0] + r0[1] * axis_local[1] + r0[2] * axis_local[2],
        r1[0] * axis_local[0] + r1[1] * axis_local[1] + r1[2] * axis_local[2],
        r2[0] * axis_local[0] + r2[1] * axis_local[1] + r2[2] * axis_local[2],
    )

    if jt == 2:  # revolute
        v = wp.vec3(p_eef[0] - p_joint[0], p_eef[1] - p_joint[1], p_eef[2] - p_joint[2])
        linear_jac = wp.vec3(
            axis_world[1] * v[2] - axis_world[2] * v[1],
            axis_world[2] * v[0] - axis_world[0] * v[2],
            axis_world[0] * v[1] - axis_world[1] * v[0],
        )
        angular_jac = axis_world
    elif jt == 1:  # prismatic
        linear_jac = axis_world
        angular_jac = wp.vec3(0.0, 0.0, 0.0)

    jacobian[b_idx, 0, glb_joint_idx] = linear_jac[0]
    jacobian[b_idx, 1, glb_joint_idx] = linear_jac[1]
    jacobian[b_idx, 2, glb_joint_idx] = linear_jac[2]
    jacobian[b_idx, 3, glb_joint_idx] = angular_jac[0]
    jacobian[b_idx, 4, glb_joint_idx] = angular_jac[1]
    jacobian[b_idx, 5, glb_joint_idx] = angular_jac[2]


class CalculateJacobian(torch.autograd.Function):
    @staticmethod
    def forward(
        ctx,
        joint_values: Float[torch.Tensor, "... total_num_joints"],
        target_link_indices: torch.Tensor,
        articulation: "Articulation",
        root_poses: Optional[Float[torch.Tensor, "... num_arti 4 4"]] = None,
    ) -> Tuple[Float[torch.Tensor, "... 6 total_num_joints"], Float[torch.Tensor, "... num_arti 4 4"]]:
        """Forward pass to compute Jacobian and target link poses."""
        batch_shape = joint_values.shape[:-1]
        total_num_joints = joint_values.shape[-1]
        total_num_links = articulation.total_num_links
        num_arti = articulation.num_arti
        requires_grad = joint_values.requires_grad or (root_poses is not None and root_poses.requires_grad)

        wp.init()
        joint_values_wp = wp.from_torch(
            joint_values.contiguous().view(-1, total_num_joints),
            dtype=wp.float32,
            requires_grad=joint_values.requires_grad,
        )
        root_poses_wp = (
            wp.from_torch(
                root_poses.contiguous().view(-1, num_arti, 4, 4),
                dtype=wp.mat44,
                requires_grad=root_poses.requires_grad,
            )
            if root_poses is not None
            else wp.zeros(shape=(0, 0), dtype=wp.mat44, requires_grad=False, device=joint_values_wp.device)
        )
        link_poses_wp = wp.from_torch(
            torch.zeros(
                (joint_values_wp.shape[0], total_num_links, 4, 4),
                device=joint_values.device,
                dtype=joint_values.dtype,
                requires_grad=requires_grad,
            ),
            dtype=wp.mat44,
            requires_grad=requires_grad,
        )
        target_link_indices_wp = wp.from_torch(target_link_indices, dtype=wp.int32, requires_grad=False)
        wp_params = {
            name: wp.from_torch(getattr(articulation, fn)(return_tensors="pt"), dtype=dtype)
            for name, (dtype, fn) in _KERNEL_PARAMS_TYPES_AND_GETTERS.items()
        }

        # launch forward kinematics kernel
        wp.launch(
            kernel=forward_kinematics_kernel,
            dim=(joint_values_wp.shape[0], num_arti),
            inputs=[joint_values_wp, root_poses_wp, *wp_params.values()],
            outputs=[link_poses_wp],
            device=joint_values_wp.device,
        )

        # compute target link poses from link poses
        joint_axes_wp = wp.from_torch(articulation.get_packed_full_joint_axes(return_tensors="pt"), dtype=wp.vec3)
        ancestor_mask_pt = articulation.get_packed_ancestor_links_mask(target_link_indices, return_tensors="pt")
        ancestor_mask_wp = wp.from_torch(ancestor_mask_pt, dtype=wp.int32)

        jacobian_torch = torch.zeros(
            (joint_values_wp.shape[0], 6, total_num_joints),
            device=joint_values.device,
            dtype=joint_values.dtype,
            requires_grad=False,
        )
        jacobian_wp = wp.from_torch(jacobian_torch, dtype=wp.float32, requires_grad=False)

        # launch Jacobian kernel with target link poses as input
        wp.launch(
            kernel=calculate_jacobian_kernel,
            dim=(joint_values_wp.shape[0], total_num_links),
            inputs=[
                link_poses_wp,
                target_link_indices_wp,
                ancestor_mask_wp,
                joint_axes_wp,
                wp_params["link_joint_types"],
                wp_params["link_joint_indices"],
                wp_params["link_joint_origins"],
                wp_params["parent_link_indices"],
                wp_params["joint_first_indices"],
                wp_params["link_first_indices"],
            ],
            outputs=[jacobian_wp],
            device=joint_values_wp.device,
        )

        if requires_grad:
            ctx.batch_shape = batch_shape
            ctx.total_num_joints = total_num_joints
            ctx.total_num_links = total_num_links  # stored for backward launch
            ctx.num_arti = num_arti
            ctx.joint_values_wp = joint_values_wp
            ctx.root_poses_wp = root_poses_wp
            ctx.link_poses_wp = link_poses_wp
            ctx.wp_params = wp_params
            ctx.jacobian_wp = jacobian_wp
            ctx.joint_axes_wp = joint_axes_wp
            ctx.ancestor_mask_wp = ancestor_mask_wp

        link_poses_pt = wp.to_torch(link_poses_wp).view(-1, total_num_links, 4, 4)
        link_first_indices_pt = wp.to_torch(wp_params["link_first_indices"]).view(-1)  # [num_arti]
        target_glb_indices = target_link_indices.to(link_poses_pt.device) + link_first_indices_pt
        target_link_poses = link_poses_pt[:, target_glb_indices.long(), :, :]

        return (
            wp.to_torch(jacobian_wp).view(*batch_shape, 6, total_num_joints),
            target_link_poses.view(*batch_shape, -1, 4, 4),
        )

    @staticmethod
    def backward(  # type: ignore
        ctx,
        jacobian_grad: Float[torch.Tensor, "... 6 total_num_joints"],
        target_link_poses_grad: Float[torch.Tensor, "... num_arti 4 4"],
    ) -> Tuple[
        Optional[Float[torch.Tensor, "... total_num_joints"]],
        None,
        None,
        Optional[Float[torch.Tensor, "... num_arti 4 4"]],
    ]:
        """Backward pass for propagating Jacobian gradients."""
        raise NotImplementedError("Backward pass for Jacobian calculation is not verified yet.")


def calculate_jacobian(
    joint_values: Float[torch.Tensor, "... total_num_joints"],
    target_link_indices: torch.Tensor,
    articulation: "Articulation",
    root_poses: Optional[Float[torch.Tensor, "... num_arti 4 4"]] = None,
    return_target_link_poses: bool = False,
) -> Union[
    Float[torch.Tensor, "... 6 total_num_joints"],
    Tuple[Float[torch.Tensor, "... 6 total_num_joints"], Float[torch.Tensor, "... num_arti 4 4"]],
]:
    jacobian, target_link_poses = CalculateJacobian.apply(joint_values, target_link_indices, articulation, root_poses)
    if return_target_link_poses:
        return jacobian, target_link_poses
    else:
        return jacobian


@wp.kernel
def delta_pose_kernel(
    T_current: wp.array(dtype=wp.mat44),
    pos_target: wp.array(dtype=wp.vec3),
    quat_target: wp.array(dtype=wp.vec4),
    delta: wp.array2d(dtype=wp.float32),
) -> None:
    """Compute delta pose error between current and target poses in axis-angle form."""
    tid = wp.tid()

    # extract current translation error
    T = T_current[tid]
    p_current = wp.vec3(T[0, 3], T[1, 3], T[2, 3])
    pt = pos_target[tid]
    pos_err = wp.vec3(pt[0] - p_current[0], pt[1] - p_current[1], pt[2] - p_current[2])

    # extract rotation matrix elements
    r00 = T[0, 0]
    r01 = T[0, 1]
    r02 = T[0, 2]
    r10 = T[1, 0]
    r11 = T[1, 1]
    r12 = T[1, 2]
    r20 = T[2, 0]
    r21 = T[2, 1]
    r22 = T[2, 2]

    # convert rotation matrix to quaternion (w, x, y, z)
    trace = r00 + r11 + r22
    if trace > 0.0:
        s = wp.sqrt(trace + 1.0) * 2.0
        qw = 0.25 * s
        qx = (r21 - r12) / s
        qy = (r02 - r20) / s
        qz = (r10 - r01) / s
    else:
        if r00 > r11 and r00 > r22:
            s = wp.sqrt(1.0 + r00 - r11 - r22) * 2.0
            qw = (r21 - r12) / s
            qx = 0.25 * s
            qy = (r01 + r10) / s
            qz = (r02 + r20) / s
        elif r11 > r22:
            s = wp.sqrt(1.0 + r11 - r00 - r22) * 2.0
            qw = (r02 - r20) / s
            qx = (r01 + r10) / s
            qy = 0.25 * s
            qz = (r12 + r21) / s
        else:
            s = wp.sqrt(1.0 + r22 - r00 - r11) * 2.0
            qw = (r10 - r01) / s
            qx = (r02 + r20) / s
            qy = (r12 + r21) / s
            qz = 0.25 * s

    # get target quaternion components (w, x, y, z)
    target_q = quat_target[tid]
    qtw = target_q[0]
    qtx = target_q[1]
    qty = target_q[2]
    qtz = target_q[3]

    # compute quaternion error: quat_err = quat_target * quaternion_invert(current)
    q_err_w = qtw * qw + qtx * qx + qty * qy + qtz * qz
    q_err_x = -qtw * qx + qtx * qw - qty * qz + qtz * qy
    q_err_y = -qtw * qy + qtx * qz + qty * qw - qtz * qx
    q_err_z = -qtw * qz - qtx * qy + qty * qx + qtz * qw

    # ensure the error quaternion is in the same hemisphere (w>=0)
    if q_err_w < 0.0:
        q_err_w = -q_err_w
        q_err_x = -q_err_x
        q_err_y = -q_err_y
        q_err_z = -q_err_z

    # clamp to avoid numerical issues (acos domain)
    if q_err_w > 1.0:
        q_err_w = 1.0
    if q_err_w < -1.0:
        q_err_w = -1.0

    # convert the quaternion error to axis-angle representation
    angle = 2.0 * wp.acos(q_err_w)
    sin_half_angle = wp.sqrt(1.0 - q_err_w * q_err_w)
    eps = 1e-6
    if sin_half_angle < eps:
        rot_error_x = 0.0
        rot_error_y = 0.0
        rot_error_z = 0.0
    else:
        rot_error_x = q_err_x / sin_half_angle * angle
        rot_error_y = q_err_y / sin_half_angle * angle
        rot_error_z = q_err_z / sin_half_angle * angle

    # write concatenated translation and rotation error to the output
    delta[tid, 0] = pos_err[0]
    delta[tid, 1] = pos_err[1]
    delta[tid, 2] = pos_err[2]
    delta[tid, 3] = rot_error_x
    delta[tid, 4] = rot_error_y
    delta[tid, 5] = rot_error_z


def delta_pose_warp(
    T_current: Float[torch.Tensor, "... 4 4"],
    pos_target: Float[torch.Tensor, "... 3"],
    quat_target: Float[torch.Tensor, "... 4"],
) -> Float[torch.Tensor, "... 6"]:
    batch_shape = T_current.shape[:-2]
    T_current_wp = wp.from_torch(T_current.contiguous().view(-1, 4, 4), dtype=wp.mat44, requires_grad=False)
    pos_target_wp = wp.from_torch(pos_target.contiguous().view(-1, 3), dtype=wp.vec3, requires_grad=False)
    quat_target_wp = wp.from_torch(quat_target.contiguous().view(-1, 4), dtype=wp.vec4, requires_grad=False)
    delta_wp = wp.zeros(shape=(T_current_wp.shape[0], 6), dtype=wp.float32, device=T_current_wp.device)
    wp.launch(
        kernel=delta_pose_kernel,
        dim=(T_current_wp.shape[0],),
        inputs=[T_current_wp, pos_target_wp, quat_target_wp],
        outputs=[delta_wp],
        device=T_current_wp.device,
    )
    return wp.to_torch(delta_wp).view(*batch_shape, 6)


@wp.func
def solve_lower_triangular(L: Any, b: Any) -> Any:
    """Solves for y in L y = b where L is lower triangular with unit diagonal.

    Returns:
        y: the solution vector.
    """
    y = type(b)()  # initialized vector (assumed zero)
    for i in range(type(b).length):
        sum_val = b.dtype(0)
        for j in range(i):
            # accumulate lower-triangular contributions
            sum_val = sum_val + L[i, j] * y[j]
        y[i] = b[i] - sum_val
    return y


@wp.func
def inverse_lu(A: Any) -> Any:
    """Computes the inverse of a square matrix using LU decomposition without pivoting.

    Returns:
        A_inv: the inverse of A.
    """
    # initialize L as identity and U as a copy of A
    L = wp.identity(n=type(A[0]).length, dtype=A.dtype)
    U = type(A)()
    for i in range(type(A[0]).length):
        for j in range(type(A[0]).length):
            U[i, j] = A[i, j]
    # perform LU decomposition (Doolittle algorithm)
    for i in range(type(A[0]).length):
        for j in range(i + 1, type(A[0]).length):
            pivot = U[i, i]
            factor = U[j, i] / pivot
            L[j, i] = factor
            for k in range(i, type(A[0]).length):
                U[j, k] = U[j, k] - factor * U[i, k]
    # compute inverse column-by-column by solving A x = e for each basis vector e
    A_inv = type(A)()
    for i in range(type(A[0]).length):
        # create standard basis vector e with 1 at index i and 0 elsewhere
        e = type(A[0])()
        for j in range(type(A[0]).length):
            e[j] = A.dtype(0)
        e[i] = A.dtype(1)
        # forward substitution: solve L y = e
        y = solve_lower_triangular(L, e)
        x = solve_triangular(U, y)
        A_inv[i] = x
    return wp.transpose(A_inv)


@wp.kernel
def compute_dq_kernel_v2(
    J: wp.array3d(dtype=wp.float32),  # shape: [b, 6, total_num_joints]
    err: wp.array3d(dtype=wp.float32),  # shape: [b, num_arti, 6]
    A: wp.array3d(dtype=wp.float32),  # shape: [b, num_arti, 6]
    joint_first_indices: wp.array(dtype=wp.int32),  # shape: [num_arti]
    damping: wp.float32,  # damping factor for regularization
    dq: wp.array2d(dtype=wp.float32),  # shape: [b, total_num_joints] (output)
) -> None:
    """Compute joint velocity dq using a damped least-squares formulation."""
    b_idx, arti_idx = wp.tid()

    # determine number of articulations and total joints from input arrays
    num_arti = joint_first_indices.shape[0]
    total_num_joints = int(J.shape[2])

    # determine joint index range for the current articulation
    start_idx = joint_first_indices[arti_idx]
    if arti_idx == num_arti - 1:
        end_idx = total_num_joints
    else:
        end_idx = joint_first_indices[arti_idx + 1]

    # compute the 6x6 JJt matrix for the current articulation
    M = wp.identity(n=6, dtype=wp.float32)  # local 6x6 matrix
    for i in range(6):
        for j in range(6):
            sum_val = float(0.0)
            for k in range(start_idx, end_idx):
                # accumulate product contributions over joint indices
                sum_val = sum_val + J[b_idx, i, k] * J[b_idx, j, k]
            if i == j:
                # add damping regularization on the diagonal
                sum_val = sum_val + damping
            M[i, j] = sum_val

    # compute inverse of the JJt matrix via QR factorization
    inv_M = inverse_qr(M)
    # inv_M = inverse_lu(M)

    # compute vector A = inv_M * err locally for the articulation block
    for i in range(6):
        acc = float(0.0)
        for j in range(6):
            acc = acc + inv_M[i, j] * err[b_idx, arti_idx, j]
        A[b_idx, arti_idx, i] = acc

    # compute dq for each joint in the current articulation block
    for k in range(start_idx, end_idx):
        acc = float(0.0)
        for i in range(6):
            acc = acc + J[b_idx, i, k] * A[b_idx, arti_idx, i]
        dq[b_idx, k] = acc


def compute_dq_warp(
    J: Float[torch.Tensor, "... 6 total_num_joints"],
    err: Float[torch.Tensor, "... num_arti 6"],
    joint_first_indices_pt: Int[torch.Tensor, "num_arti"],
    damping: float,
) -> Float[torch.Tensor, "... total_num_joints"]:
    batch_shape = J.shape[:-2]
    total_num_joints = J.shape[-1]
    num_arti = len(joint_first_indices_pt)

    J_wp = wp.from_torch(J.contiguous().view(-1, 6, total_num_joints), dtype=wp.float32, requires_grad=False)
    err_wp = wp.from_torch(err.contiguous().view(-1, num_arti, 6), dtype=wp.float32, requires_grad=False)  # [b, A, 6]
    A_wp = wp.zeros(shape=(err_wp.shape[0], num_arti, 6), dtype=wp.float32, device=err_wp.device)  # [b, A, 6]
    dq_wp = wp.zeros(shape=(J_wp.shape[0], total_num_joints), dtype=wp.float32, device=J_wp.device)

    wp.launch(
        kernel=compute_dq_kernel_v2,
        dim=(J_wp.shape[0], num_arti),
        inputs=[J_wp, err_wp, A_wp, wp.from_torch(joint_first_indices_pt, dtype=wp.int32), damping, dq_wp],
        device=J_wp.device,
    )

    dq = wp.to_torch(dq_wp).view(*batch_shape, total_num_joints)
    return dq


@torch.no_grad()
def inverse_kinematics(
    target_link_poses: Float[torch.Tensor, "... num_arti 4 4"],
    target_link_indices: Int[torch.Tensor, "num_arti"],
    articulation: "Articulation",
    max_iterations: int = 100,
    learning_rate: float = 0.1,
    tolerance: float = 1e-6,
    damping: float = 0.01,
    num_retries: int = 10,
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

    target_link_poses_particles = target_link_poses.unsqueeze(-4).expand(*batch_shape, num_retries, num_arti, 4, 4)
    pos_target = target_link_poses_particles[..., :3, 3]  # shape: (*batch_shape, num_retries, num_arti, 3)
    # shape: (*batch_shape, num_retries, num_arti, 4)
    quat_target = matrix_to_quaternion(target_link_poses_particles[..., :3, :3])

    joint_first_indices_pt = articulation.get_joint_first_indices(return_tensors="pt")
    joint_limits = articulation.get_packed_joint_limits(return_tensors="pt")

    jfi = joint_first_indices_pt.tolist()
    joint_slices = [slice(jfi[i], jfi[i + 1]) for i in range(num_arti - 1)] + [slice(jfi[-1], total_num_dofs)]

    for _ in range(max_iterations):
        J, current_poses = calculate_jacobian(q, target_link_indices, articulation, return_target_link_poses=True)
        err = delta_pose_warp(current_poses, pos_target, quat_target)  # shape: (*batch_shape, num_retries, A, 6)
        err_norm = err.norm(dim=-1)  # shape: (*batch_shape, num_retries, A)
        if (err_norm < tolerance).any(dim=-2).all():
            break

        dq = compute_dq_warp(J, err, joint_first_indices_pt, damping)  # type: ignore

        q = q + learning_rate * dq
        if joint_limits is not None:
            q = torch.clamp(q, min=joint_limits[..., 0], max=joint_limits[..., 1])  # type: ignore

    # select the best retry per articulation based on squared error norm
    _, current_poses = calculate_jacobian(q, target_link_indices, articulation, return_target_link_poses=True)
    final_err = delta_pose_warp(current_poses, pos_target, quat_target)  # shape: (*batch_shape, num_retries, A, 6)
    final_err_norm = final_err.norm(dim=-1)  # shape: (*batch_shape, num_retries, A)
    best_idx = final_err_norm.argmin(dim=-2)  # shape: (*batch_shape, A)
    final_success = (final_err_norm < tolerance).any(dim=-2)  # shape: (*batch_shape, A)
    best_q_list = []
    for i, js in enumerate(joint_slices):
        sel = best_idx[..., i].unsqueeze(-1)  # shape: (*batch_shape, 1)
        q_seg = q[..., js]  # shape: (*batch_shape, num_retries, dof_range)
        indices = sel.unsqueeze(-1).expand(*sel.shape, q_seg.shape[-1])
        best_q_list.append(torch.gather(q_seg, dim=-2, index=indices).squeeze(-2))
    best_q = torch.cat(best_q_list, dim=-1)
    return best_q, final_success
