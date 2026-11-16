#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
runtime="${ISAAC_NATIVE_RUNTIME:-$HOME/.local/share/isaac-steel-rtx}"
python="$runtime/.venv/bin/python"
if [[ ! -x "$python" ]]; then
    printf 'Install the locked Isaac Lab runtime as described in %s/README.md\n' "$root" >&2
    exit 2
fi

export PYTHONPATH="$root/src${PYTHONPATH:+:$PYTHONPATH}"
export PYTHONUNBUFFERED=1
export TMPDIR="${TMPDIR:-$runtime/tmp}"
export XDG_CACHE_HOME="${XDG_CACHE_HOME:-$runtime/cache}"
mkdir -p "$TMPDIR" "$XDG_CACHE_HOME"
if [[ $# == 0 ]]; then
    set -- "$root/scripts/smoke.py"
fi
exec "$python" "$@"
