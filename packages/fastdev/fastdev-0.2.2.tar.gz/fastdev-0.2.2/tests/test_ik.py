from typing import Tuple

import torch

from fastdev.robo.articulation import Articulation


def compute_pose_errors(pred: torch.Tensor, target: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
    """Compute position and rotation error between two poses.

    Args:
        pred: predicted pose tensor of shape [N, 4, 4].
        target: target pose tensor of shape [N, 4, 4].

    Returns:
        A tuple containing the position error (L2 distance) of shape [N] and
        the rotation error (angle in radians) of shape [N].
    """
    pos_err = torch.norm(pred[..., :3, 3] - target[..., :3, 3], dim=-1)
    R_pred = pred[..., :3, :3]
    R_target = target[..., :3, :3]
    R_rel = torch.matmul(R_pred.transpose(-2, -1), R_target)
    trace = R_rel.diagonal(dim1=-2, dim2=-1).sum(-1)
    rot_err = torch.acos(torch.clamp((trace - 1) / 2, -1.0, 1.0))
    return pos_err, rot_err


def test_articulation_ik() -> None:
    """Test our inverse kinematics solver with a known joint configuration."""
    device: str = "cuda" if torch.cuda.is_available() else "cpu"

    full_urdf: str = "assets/robot_description/kuka_iiwa.urdf"
    arti = Articulation.from_urdf_or_mjcf_path(full_urdf, device=device)
    # using a known joint configuration
    q_known = torch.tensor([[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]], device=device)
    goal_tf = arti.forward_kinematics(q_known)[:, -1]
    sol = arti.inverse_kinematics(goal_tf)
    pred_tf = arti.forward_kinematics(sol)[-1]
    pos_err, rot_err = compute_pose_errors(pred_tf, goal_tf)
    # check that positional and rotational errors are low
    assert pos_err.mean().item() < 0.01, f"articulation IK pos error too high: {pos_err.mean().item()}"
    assert rot_err.mean().item() < 0.1, f"articulation IK rot error too high: {rot_err.mean().item()}"


def test_articulation_ik_batch() -> None:
    """Test inverse kinematics with a batch of joint configurations."""
    device: str = "cuda" if torch.cuda.is_available() else "cpu"

    full_urdf: str = "assets/robot_description/kuka_iiwa.urdf"
    arti = Articulation.from_urdf_or_mjcf_path(full_urdf, device=device)
    # using a batch of known joint configurations
    q_batch = torch.tensor(
        [[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7], [0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1], [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]],
        device=device,
    )
    # compute goal poses for each configuration
    goal_tf = arti.forward_kinematics(q_batch)[:, -1]
    sol = arti.inverse_kinematics(goal_tf)
    pred_tf = arti.forward_kinematics(sol)[:, -1]
    pos_err, rot_err = compute_pose_errors(pred_tf, goal_tf)
    # check that errors are low for the batch
    assert pos_err.mean().item() < 0.02, f"articulation IK batch pos error too high: {pos_err.mean().item()}"
    assert rot_err.mean().item() < 0.15, f"articulation IK batch rot error too high: {rot_err.mean().item()}"
