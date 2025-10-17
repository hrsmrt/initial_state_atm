#!/usr/bin/env python3
"""
python3 $WORK/initial_state_atm/run_all.py
Run the data generation and plotting scripts in order from any working directory.

Usage:
  python run_all.py [--root /path/to/repo]

This script will:
  1. locate the repository root (either via --root or relative to this script),
  2. run `program/mkdata/cartesian.py`,
  3. then run `program/mkfig/cart_pre.py`, `program/mkfig/cart_qv.py`,
     and `program/mkfig/cart_tem.py` in that order.

If any script exits with a non-zero status, execution stops and the exit code
is propagated.
"""
import argparse
import os
import subprocess
import sys


def find_repo_root(explicit_root=None):
    if explicit_root:
        return os.path.abspath(explicit_root)
    # locate directory containing this script and treat its parent as repo root
    this_file = os.path.abspath(__file__)
    repo_root = os.path.dirname(this_file)
    # repo root is parent of this file
    return os.path.abspath(os.path.join(repo_root))


def run_script(python_exe, script_path, repo_root):
    script_abs = os.path.join(repo_root, script_path)
    if not os.path.exists(script_abs):
        print(f"ERROR: script not found: {script_abs}", file=sys.stderr)
        return 2
    print(f"Running: {python_exe} {script_abs}")
    proc = subprocess.Popen([python_exe, script_abs], cwd=repo_root)
    proc.wait()
    return proc.returncode


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--root', help='path to repository root (optional)')
    p.add_argument('--python', default=sys.executable, help='python executable to use')
    args = p.parse_args()

    repo_root = find_repo_root(args.root)
    print(f"Repository root: {repo_root}")

    # try to import params to obtain plotting style if available
    utils_dir = os.path.join(repo_root, 'program', 'utils')
    if utils_dir not in sys.path:
        sys.path.insert(0, utils_dir)
    style_arg = None
    try:
        import params
        style_arg = params.settings.get('mkfig_params', {}).get('plt_style')
    except Exception:
        # params may not be available; continue without style
        style_arg = None

    # scripts: tuples of (script_relative_path, [extra args])
    scripts = [
        ('program/mkdata/cartesian.py', []),
        ('program/mkfig/cart_pre.py', [style_arg] if style_arg else []),
        ('program/mkfig/cart_qv.py', [style_arg] if style_arg else []),
        ('program/mkfig/cart_tem.py', [style_arg] if style_arg else []),
    ]

    called_from = os.getcwd()
    for i, (script, extra_args) in enumerate(scripts):
        # build command and run
        script_abs = os.path.join(repo_root, script)
        if not os.path.exists(script_abs):
            print(f"ERROR: script not found: {script_abs}", file=sys.stderr)
            sys.exit(2)
        cmd = [args.python, script_abs] + extra_args
        # Run all scripts from the directory where run_all was invoked so that
        # output paths like ./data/ and ./fig/ are created relative to the caller's cwd.
        cwd = called_from
        print('Running:', ' '.join(cmd), 'cwd=', cwd)
        proc = subprocess.Popen(cmd, cwd=cwd)
        proc.wait()
        if proc.returncode != 0:
            print(f"Script failed: {script} (exit {proc.returncode})", file=sys.stderr)
            sys.exit(proc.returncode)

    print('All scripts completed successfully')


if __name__ == '__main__':
    main()
