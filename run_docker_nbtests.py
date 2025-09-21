#!/usr/bin/env python3
import subprocess
import sys
import os

# -----------------------------
# CONFIG
# -----------------------------
DOCKER_IMAGE = "sagemath/sagemath:latest"
NB_PATH = "Submissions/oxrmeb.ipynb"  # change this if needed
RUN_SCRIPT = "grader/run_nbtests.py"

# Get absolute paths
work_dir = os.path.abspath(os.getcwd())
nb_path_abs = os.path.join(work_dir, NB_PATH)
run_script_abs = os.path.join(work_dir, RUN_SCRIPT)

# -----------------------------
# FUNCTION TO RUN COMMANDS
# -----------------------------
def run_cmd(cmd, check=True):
    try:
        subprocess.run(cmd, shell=True, check=check)
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
        sys.exit(1)

# -----------------------------
# 1️⃣ Check if Docker image exists
# -----------------------------
print(f"Checking if Docker image '{DOCKER_IMAGE}' exists...")
images = subprocess.run(
    ["docker", "images", "-q", DOCKER_IMAGE],
    capture_output=True,
    text=True
).stdout.strip()

if not images:
    print(f"Docker image not found. Pulling '{DOCKER_IMAGE}'...")
    run_cmd(f"docker pull {DOCKER_IMAGE}")
else:
    print(f"Docker image '{DOCKER_IMAGE}' already exists.")

# -----------------------------
# 2️⃣ Run the grading script inside Docker
# -----------------------------
print(f"Running notebook '{NB_PATH}' in Docker...")
if os.name == "nt":
    # Windows uses %cd% style volume mount
    docker_cmd = (
        f'docker run --rm -it -v "{work_dir}:/home/sage/work" '
        f'{DOCKER_IMAGE} sage -python /home/sage/work/{RUN_SCRIPT} '
        f'--nb /home/sage/work/{NB_PATH}'
    )
else:
    # Unix/Linux
    docker_cmd = (
        f'docker run --rm -it -v "{work_dir}:/home/sage/work" '
        f'{DOCKER_IMAGE} sage -python /home/sage/work/{RUN_SCRIPT} '
        f'--nb /home/sage/work/{NB_PATH}'
    )

run_cmd(docker_cmd)
print("Done.")
