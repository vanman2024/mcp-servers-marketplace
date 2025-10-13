#!/usr/bin/env bash
set -euo pipefail

# Creates virtual environments for each subproject that has a requirements.txt
# and optionally installs dependencies into that venv.
#
# Usage:
#   scripts/setup_venvs.sh            # create venvs and install deps
#   scripts/setup_venvs.sh --no-install  # only create venvs (skip pip install)
#   scripts/setup_venvs.sh --force    # recreate venvs if they already exist
#

NO_INSTALL=false
FORCE=false

for arg in "$@"; do
  case "$arg" in
    --no-install)
      NO_INSTALL=true
      shift
      ;;
    --force)
      FORCE=true
      shift
      ;;
    *)
      echo "Unknown option: $arg" >&2
      exit 1
      ;;
  esac
done

if command -v python3 >/dev/null 2>&1; then
  PY=python3
elif command -v python >/dev/null 2>&1; then
  PY=python
else
  echo "Python is not installed or not on PATH." >&2
  exit 1
fi

echo "Finding projects with requirements.txt..."
mapfile -t REQS < <(find . -type f -name requirements.txt -not -path '*/node_modules/*' | sort)

if [ ${#REQS[@]} -eq 0 ]; then
  echo "No requirements.txt files found. Nothing to do."
  exit 0
fi

for req in "${REQS[@]}"; do
  proj_dir=$(dirname "$req")
  venv_dir="$proj_dir/.venv"

  echo "\n==> Processing: $proj_dir"

  if [ -d "$venv_dir" ]; then
    if [ "$FORCE" = true ]; then
      echo "Removing existing venv: $venv_dir"
      rm -rf "$venv_dir"
    else
      echo "Venv already exists: $venv_dir (use --force to recreate)"
    fi
  fi

  if [ ! -d "$venv_dir" ]; then
    echo "Creating venv at $venv_dir"
    "$PY" -m venv "$venv_dir"
  fi

  if [ "$NO_INSTALL" = false ]; then
    echo "Installing dependencies from $req"
    # shellcheck source=/dev/null
    source "$venv_dir/bin/activate"
    python -m pip install --upgrade pip
    pip install -r "$req"
    deactivate || true
  else
    echo "Skipping install as requested (--no-install)"
  fi
done

echo "\nAll done. Venvs created for projects with requirements.txt."

