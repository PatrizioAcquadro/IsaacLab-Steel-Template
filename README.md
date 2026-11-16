# Isaac Lab Steel starter

External project generated with the official Isaac Lab generator. The project
uses Newton's native `SteelSolverCfg` on CUDA with CUDA Graph enabled.

## Run on a machine with the shared runtime

~~~bash
./scripts/isaac-run.sh
~~~

The smoke test runs headless on the GPU. A successful run prints a JSON result
with `SolverSteel`, `"cuda_graph": true`, and a cube settled on a table. The
launcher uses `$HOME/.local/share/isaac-steel-rtx`. Set `ISAAC_NATIVE_RUNTIME`
to use a separate installation. Accept the NVIDIA terms on first use.

## Install the pinned runtime on a new machine

Use Linux with a compatible NVIDIA GPU, Python 3.12, Git and uv. Run these
commands from the project root with a fresh runtime path. If you choose a path
other than the default, export `ISAAC_NATIVE_RUNTIME` when running the launcher.

~~~bash
runtime="${ISAAC_NATIVE_RUNTIME:-$HOME/.local/share/isaac-steel-rtx}"
revision=67fe12806afbdb8bf8e125866661dd201088a54d
mkdir -p "$runtime"
git init "$runtime/IsaacLab"
git -C "$runtime/IsaacLab" fetch --depth=1 https://github.com/isaac-sim/IsaacLab.git "$revision"
GIT_LFS_SKIP_SMUDGE=1 git -C "$runtime/IsaacLab" checkout --detach "$revision"
git -C "$runtime/IsaacLab" apply --unidiff-zero "$PWD/configs/isaac-native-numpy.patch"
UV_PROJECT_ENVIRONMENT="$runtime/.venv" uv --directory "$runtime/IsaacLab" \
  sync --locked --python python3.12 --extra isaacsim
uv pip check --python "$runtime/.venv/bin/python"
~~~

The patch pins NumPy 2.4.6 for the Numba version already in the upstream lock.
The `isaacsim` extra installs the Kit runtime for RTX sensors.

## Start a task

Copy this directory for a new project. Add task code and registrations under
`src/isaaclab_steel_template/tasks/` and project assets under
`src/isaaclab_steel_template/assets/data/`. Use the same configuration in the
environment and its launcher.

~~~python
from isaaclab.sim import SimulationCfg

from isaaclab_steel_template.physics import steel_physics

sim_cfg = SimulationCfg(device="cuda:0", physics=steel_physics())
~~~

The factory uses point friction by default. For sustained grasps, VLA-LEGO
validated `steel_physics(friction_anchor_beta=0.2)` on its nominal five-block
tower. Set this parameter in the task that uses it and check its contact
behavior. Add cameras and controls through the Isaac Lab scene APIs.

Pass a Python entry point and its arguments to `./scripts/isaac-run.sh`.
For Gymnasium task discovery, install the project into the pinned environment
with `uv pip install --no-deps --python "$runtime/.venv/bin/python" -e .`.

[NVIDIA Isaac Lab launcher](https://isaac-sim.github.io/IsaacLab/main/source/tutorials/00_sim/launch_app.html) ·
[Native Newton solver configuration](https://isaac-sim.github.io/IsaacLab/main/source/concepts/physics-backends/newton.html)
