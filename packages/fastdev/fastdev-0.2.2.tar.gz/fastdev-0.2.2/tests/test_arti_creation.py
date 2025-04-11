from fastdev.robo.articulation import Articulation, ArticulationSpec


def test_partial_arti():
    arti = Articulation(ArticulationSpec(urdf_or_mjcf_path="assets/robot_description/wx250s.urdf"))
    full_arti_expected = """
Articulation(num_arti=1, total_num_dofs=8, total_num_links=14, device=cpu)
  - wx250s.urdf (num_dofs=8, num_links=14)

ArticulationSpec(filename=wx250s.urdf, num_dofs=8, num_links=14)
└── base_link (__root__, *)
  └── shoulder_link (waist, R)
    └── upper_arm_link (shoulder, R)
      └── upper_forearm_link (elbow, R)
        └── lower_forearm_link (forearm_roll, R)
          └── wrist_link (wrist_angle, R)
            └── gripper_link (wrist_rotate, R)
              └── ee_arm_link (ee_arm, F)
                ├── gripper_prop_link (gripper, F)
                └── gripper_bar_link (gripper_bar, F)
                  └── fingers_link (ee_bar, F)
                    ├── left_finger_link (left_finger, P)
                    ├── right_finger_link (right_finger, P)
                    └── ee_gripper_link (ee_gripper, F)
"""
    assert str(arti).strip() == full_arti_expected.strip()

    arti = Articulation(
        ArticulationSpec(
            urdf_or_mjcf_path="assets/robot_description/wx250s.urdf",
            base_link_name="base_link",
            ee_link_names="ee_gripper_link",
        )
    )
    arti_expected = """
Articulation(num_arti=1, total_num_dofs=6, total_num_links=11, device=cpu)
  - wx250s.urdf (num_dofs=6, num_links=11)

ArticulationSpec(filename=wx250s.urdf, num_dofs=6, num_links=11)
└── base_link (__root__, *)
  └── shoulder_link (waist, R)
    └── upper_arm_link (shoulder, R)
      └── upper_forearm_link (elbow, R)
        └── lower_forearm_link (forearm_roll, R)
          └── wrist_link (wrist_angle, R)
            └── gripper_link (wrist_rotate, R)
              └── ee_arm_link (ee_arm, F)
                └── gripper_bar_link (gripper_bar, F)
                  └── fingers_link (ee_bar, F)
                    └── ee_gripper_link (ee_gripper, F)
"""
    assert str(arti).strip() == arti_expected.strip()

    arti = Articulation(
        ArticulationSpec(
            urdf_or_mjcf_path="assets/robot_description/wx250s.urdf",
            base_link_name="base_link",
            ee_link_names=["gripper_bar_link", "gripper_prop_link"],
        )
    )
    arti_expected = """
Articulation(num_arti=1, total_num_dofs=6, total_num_links=10, device=cpu)
  - wx250s.urdf (num_dofs=6, num_links=10)

ArticulationSpec(filename=wx250s.urdf, num_dofs=6, num_links=10)
└── base_link (__root__, *)
  └── shoulder_link (waist, R)
    └── upper_arm_link (shoulder, R)
      └── upper_forearm_link (elbow, R)
        └── lower_forearm_link (forearm_roll, R)
          └── wrist_link (wrist_angle, R)
            └── gripper_link (wrist_rotate, R)
              └── ee_arm_link (ee_arm, F)
                ├── gripper_prop_link (gripper, F)
                └── gripper_bar_link (gripper_bar, F)
"""
    assert str(arti).strip() == arti_expected.strip()

    arti = Articulation(
        ArticulationSpec(
            urdf_or_mjcf_path="assets/robot_description/wx250s.urdf",
            base_link_name="upper_arm_link",
            ee_link_names=["upper_forearm_link"],
        )
    )
    arti_expected = """
Articulation(num_arti=1, total_num_dofs=1, total_num_links=2, device=cpu)
  - wx250s.urdf (num_dofs=1, num_links=2)

ArticulationSpec(filename=wx250s.urdf, num_dofs=1, num_links=2)
└── upper_arm_link (__root__, *)
  └── upper_forearm_link (elbow, R)
"""
    assert str(arti).strip() == arti_expected.strip()


if __name__ == "__main__":
    test_partial_arti()
