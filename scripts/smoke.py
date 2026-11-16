"""Verify actual CUDA Graph replay and contact in a small headless Isaac scene."""

import json
import math

from isaaclab.app import launch_simulation
from isaaclab.sim import SimulationCfg

from isaaclab_steel_template.physics import steel_physics


def run(sim_cfg: SimulationCfg) -> dict:
    from newton.solvers import SolverSteel

    import isaaclab.sim as sim_utils
    from isaaclab.assets import AssetBaseCfg, RigidObjectCfg
    from isaaclab.scene import InteractiveScene, InteractiveSceneCfg
    from isaaclab.utils import configclass

    @configclass
    class DropSceneCfg(InteractiveSceneCfg):
        table = AssetBaseCfg(
            prim_path="{ENV_REGEX_NS}/Table",
            spawn=sim_utils.CuboidCfg(
                size=(1.0, 1.0, 0.05),
                collision_props=sim_utils.UsdPhysicsCollisionCfg(),
            ),
            init_state=AssetBaseCfg.InitialStateCfg(pos=(0.0, 0.0, -0.025)),
        )
        cube = RigidObjectCfg(
            prim_path="{ENV_REGEX_NS}/Cube",
            spawn=sim_utils.CuboidCfg(
                size=(0.06, 0.06, 0.06),
                rigid_props=sim_utils.UsdPhysicsRigidBodyCfg(),
                collision_props=sim_utils.UsdPhysicsCollisionCfg(),
                mass_props=sim_utils.MassCfg(mass=0.1),
            ),
            init_state=RigidObjectCfg.InitialStateCfg(pos=(0.0, 0.0, 0.30)),
        )

    sim = sim_utils.SimulationContext(sim_cfg)
    scene = InteractiveScene(DropSceneCfg(num_envs=1, env_spacing=1.0, replicate_physics=False))
    cube = scene["cube"]
    sim.reset()
    initial_z = float(cube.data.root_pos_w.torch[0, 2])
    for _ in range(200):
        sim.step(render=False)
        scene.update(sim_cfg.dt)

    backend = sim.backend_manager.backend
    if not isinstance(backend.solver, SolverSteel) or not backend.graphs:
        raise RuntimeError("Expected the native Steel solver with a captured CUDA Graph.")
    z = float(cube.data.root_pos_w.torch[0, 2])
    speed = float(cube.data.root_lin_vel_w.torch[0].norm())
    if not math.isclose(initial_z, 0.30, abs_tol=0.001) or not math.isclose(z, 0.03, abs_tol=0.003) or speed > 0.01:
        raise RuntimeError(f"Cube did not settle on the table (z={z}, speed={speed}).")
    return {
        "device": str(sim.device),
        "solver": type(backend.solver).__name__,
        "cuda_graph": True,
        "steps": 200,
        "start_z_m": initial_z,
        "settled_z_m": z,
        "settled_speed_m_s": speed,
    }


if __name__ == "__main__":
    cfg = SimulationCfg(dt=0.005, device="cuda:0", physics=steel_physics())
    with launch_simulation(cfg, {"headless": True, "require_kit": True}):
        print(json.dumps(run(cfg)), flush=True)
