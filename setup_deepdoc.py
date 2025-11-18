import os
import subprocess
import sys
import venv

# ---------------------------------------------
# CONFIG: Minimal dependencies matching RagFlow
# ---------------------------------------------
MINIMAL_DEPENDENCIES = [
    "beartype>=0.18.5,<0.19.0",
    "numpy>=1.26.0,<2.0.0",
    "pillow==10.4.0",
    "nltk==3.9.1",
    "trio>=0.29.0",
    "huggingface-hub>=0.25.0,<0.26.0",
]

# More dependencies will be added later when we inspect DeepDoc files
EXTRA_DEPENDENCIES = [
    # "example==1.0.0",
]


def create_virtual_env(env_path="deepdoc_env"):
    """Create a virtual environment if it doesn't exist."""
    if not os.path.exists(env_path):
        print(f"[+] Creating virtual environment at: {env_path}")
        venv.EnvBuilder(with_pip=True).create(env_path)
    else:
        print("[i] Virtual environment already exists.")


def install_dependencies(env_path="deepdoc_env"):
    """Install minimal + extra deps inside the virtual environment."""
    pip_exe = os.path.join(env_path, "Scripts", "pip.exe")

    if not os.path.exists(pip_exe):
        raise FileNotFoundError("pip not found inside virtual environment!")

    print("\n[+] Installing minimal dependencies...")
    for dep in MINIMAL_DEPENDENCIES:
        print(f"   → {dep}")
        subprocess.check_call([pip_exe, "install", dep])

    if EXTRA_DEPENDENCIES:
        print("\n[+] Installing extra dependencies...")
        for dep in EXTRA_DEPENDENCIES:
            print(f"   → {dep}")
            subprocess.check_call([pip_exe, "install", dep])

    print("\n[✔] All dependencies installed successfully.\n")


def main():
    print("=======================================")
    print("      DeepDoc Minimal Setup Tool       ")
    print("=======================================")

    env_name = "deepdoc_env"

    # Step 1 — Create Environment
    create_virtual_env(env_name)

    # Step 2 — Install Dependencies
    install_dependencies(env_name)

    print("=======================================")
    print(" Setup Completed. To activate env run: ")
    print("=======================================")
    print(f"\n    .\\{env_name}\\Scripts\\activate\n")
    print("Then run your DeepDoc code normally.\n")


if __name__ == "__main__":
    main()