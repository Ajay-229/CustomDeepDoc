import os
import subprocess
import sys
import venv

# ---------------------------------------------
# CONFIG: Minimal dependencies matching RagFlow
# ---------------------------------------------
MINIMAL_DEPENDENCIES = [
    "beartype>=0.18.5,<0.19.0",
    "beautifulsoup4==4.12.3",
    "chardet==5.2.0",
    "datrie>=0.8.3,<0.9.0",
    "hanziconv==0.3.2",
    "huggingface-hub>=0.25.0,<0.26.0",
    "markdown==3.6",
    "nltk==3.9.1",
    "numpy>=1.26.0,<2.0.0",
    "onnxruntime==1.19.2; sys_platform == 'darwin' or platform_machine != 'x86_64'",
    "onnxruntime-gpu==1.19.2; sys_platform != 'darwin' and platform_machine == 'x86_64'",
    "opencv-python==4.10.0.84",
    "openpyxl>=3.1.5",
    "pandas>=2.2.0,<3.0.0",
    "pdfplumber==0.10.4",
    "pillow==10.4.0",
    "pyclipper==1.3.0.post5",
    "pypdf==6.0.0",
    "python-docx>=1.1.2",
    "python-pptx>=1.0.2,<2.0.0",
    "six==1.16.0",
    "shapely==2.0.5",
    "tiktoken==0.7.0",
    "trio>=0.29.0",
    "xgboost==1.6.0"
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