import warp as wp

from fastdev.xform.rotation import (
    axis_angle_vector_to_matrix,
    axis_angle_vector_to_quaternion,
    compose_axis_angle_vector,
    matrix_to_axis_angle_vector,
    matrix_to_euler_angles,
    matrix_to_rotation_6d,
    quaternion_invert,
    quaternion_multiply,
    quaternion_real_to_first,
    quaternion_real_to_last,
    quaternion_to_axis_angle_vector,
    quaternion_to_matrix,
    random_rotation_matrix,
    rotation_6d_to_matrix,
    split_axis_angle_vector,
    standardize_quaternion,
)
from fastdev.xform.transforms import (
    expand_tf_mat,
    inverse_tf_mat,
    project_points,
    rot_tl_to_tf_mat,
    swap_major,
    to_homo,
    unproject_points,
)
from fastdev.xform.utils import (
    camera_position_from_spherical_angles,
    compose_intr_mat,
    coord_conversion,
    look_at_rotation,
)
from fastdev.xform.warp_rotation import axis_angle_to_matrix, euler_angles_to_matrix, matrix_to_quaternion
from fastdev.xform.warp_transforms import rotate_points, transform_points

wp.config.quiet = True
# wp.init()  # disabled due to conflict with ZED camera SDK

__all__ = [
    # Transforms
    "transform_points",
    "rotate_points",
    "project_points",
    "unproject_points",
    "inverse_tf_mat",
    "swap_major",
    "rot_tl_to_tf_mat",
    "expand_tf_mat",
    "to_homo",
    # Rotations
    "axis_angle_to_matrix",
    "axis_angle_vector_to_quaternion",
    "axis_angle_vector_to_matrix",
    "matrix_to_axis_angle_vector",
    "split_axis_angle_vector",
    "compose_axis_angle_vector",
    "matrix_to_quaternion",
    "matrix_to_euler_angles",
    "euler_angles_to_matrix",
    "quaternion_to_matrix",
    "quaternion_to_axis_angle_vector",
    "quaternion_real_to_last",
    "quaternion_real_to_first",
    "quaternion_multiply",
    "quaternion_invert",
    "standardize_quaternion",
    "random_rotation_matrix",
    "matrix_to_rotation_6d",
    "rotation_6d_to_matrix",
    # Camera
    "compose_intr_mat",
    "coord_conversion",
    "look_at_rotation",
    "camera_position_from_spherical_angles",
]
