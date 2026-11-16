"""Native Isaac Lab physics configuration shared by the project's tasks."""

from isaaclab_newton.physics import NewtonCfg, SteelSolverCfg
from isaaclab_newton.physics.newton_manager_cfg import NewtonShapeCfg


def steel_physics(*, friction_anchor_beta: float = 0.0) -> NewtonCfg:
    """Return a new GPU Steel configuration for each simulation."""
    return NewtonCfg(
        solver_cfg=SteelSolverCfg(
            iterations=16,
            enable_joint_limits=True,
            enable_joint_velocity_limits=True,
            articulation_constraint_max=512,
            friction_anchor_beta=friction_anchor_beta,
        ),
        default_shape_cfg=NewtonShapeCfg(gap=0.02),
        use_cuda_graph=True,
    )
