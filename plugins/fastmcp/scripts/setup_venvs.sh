#!/usr/bin/env bash
set -euo pipefail

#!/usr/bin/env bash
set -euo pipefail

# Creates virtual environments for each subproject that has a requirements.txt
# OR a pyproject.toml. For pyproject.toml with PEP 621-style
#   [project]
#   dependencies = ["pkg>=1.0", ...]
# it will generate a basic requirements.txt and install from it.
# For Poetry-style [tool.poetry.dependencies], generation is skipped unless
# dependencies can be inferred; you may use --pyproject-install to attempt
# "pip install ." in those projects.
#
# Usage:
#   scripts/setup_venvs.sh                 # create venvs and install deps
#   scripts/setup_venvs.sh --no-install    # only create venvs (skip pip install)
#   scripts/setup_venvs.sh --force         # recreate venvs if they already exist
#   scripts/setup_venvs.sh --pyproject-install  # run 'pip install .' for pyproject-only projects
#

NO_INSTALL=false
FORCE=false
PYPROJECT_INSTALL=false

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
    --pyproject-install)
      PYPROJECT_INSTALL=true
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

echo "Finding Python projects (requirements.txt or pyproject.toml)..."
mapfile -t REQS < <(find . -type f -name requirements.txt -not -path '*/node_modules/*' | sort)
mapfile -t PYPRO < <(find . -type f -name pyproject.toml -not -path '*/node_modules/*' | sort)

if [ ${#REQS[@]} -eq 0 ] && [ ${#PYPRO[@]} -eq 0 ]; then
  echo "No requirements.txt or pyproject.toml files found. Nothing to do."
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

# Helper: try to generate requirements.txt from PEP 621 [project] dependencies
# Returns 0 if generated non-empty requirements, 1 otherwise.
generate_requirements_from_pyproject() {
  local pyproj="$1"
  local out_req="$2"
  # Extract lines within [project] ... next section that are inside dependencies = [ ... ]
  local deps
  deps=$(sed -n '/^\[project\]/,/^\[/p' "$pyproj" \
    | sed -n '/^[[:space:]]*dependencies[[:space:]]*=\s*\[/,/\]/p' \
    | sed '1d;$d' \
    | sed 's/#.*$//' \
    | sed 's/["\'"\']//g' \
    | sed 's/,//g' \
    | sed 's/^[[:space:]]*//;s/[[:space:]]*$//' \
    | sed '/^$/d')

  if [ -n "$deps" ]; then
    {
      echo "# Generated from $pyproj [project.dependencies]"
      echo "$deps"
    } > "$out_req"
    return 0
  fi
  return 1
}

# Handle pyproject.toml projects that do not already have requirements.txt
for py in "${PYPRO[@]}"; do
  proj_dir=$(dirname "$py")
  req="$proj_dir/requirements.txt"
  venv_dir="$proj_dir/.venv"

  echo "\n==> Processing (pyproject): $proj_dir"

  if [ ! -f "$req" ]; then
    if generate_requirements_from_pyproject "$py" "$req"; then
      echo "Generated $req from PEP 621 dependencies."
    else
      echo "Could not infer dependencies from $py."
      echo "# No PEP 621 dependencies found.\n# If this is Poetry-based, consider exporting with Poetry or run 'pip install .'" > "$req"
    fi
  else
    echo "Existing requirements.txt found; not regenerating."
  fi

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
    # shellcheck source=/dev/null
    source "$venv_dir/bin/activate"
    python -m pip install --upgrade pip
    if [ -s "$req" ] && ! grep -q '^# No PEP 621' "$req"; then
      echo "Installing dependencies from $req"
      pip install -r "$req"
    elif [ "$PYPROJECT_INSTALL" = true ]; then
      echo "Attempting \"pip install .\" for $proj_dir"
      (cd "$proj_dir" && pip install .) || echo "pip install . failed in $proj_dir; please install manually."
    else
      echo "Skipping install: no inferable requirements; use --pyproject-install to try 'pip install .'"
    fi
    deactivate || true
  else
    echo "Skipping install as requested (--no-install)"
  fi
done

echo "\nAll done. Venvs created for projects with requirements.txt or pyproject.toml."
