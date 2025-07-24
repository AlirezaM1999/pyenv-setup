import subprocess
import os
#user types envscript.py 
# input project name
# input python version
# input packages to be installed
# open the project in vscode



#check if the pyenv has it already installed, if not install it

    #if yes, create a virtualevn with the version
    # activate environment
    #loop through packages, 
    #if any package is not valid, throw error, else install

import subprocess

def is_valid_python_version(version: str) -> bool:
    try:
        # Get the list of available Python versions
        result = subprocess.run(
            ["pyenv", "install", "--list"],
            capture_output=True,
            text=True,
            check=True
        )
        available_versions = result.stdout.splitlines()
        
        # Clean and check for match
        available_versions = [v.strip() for v in available_versions if v.strip()]
        return version in available_versions

    except subprocess.CalledProcessError as e:
        print("Error fetching versions:", e)
        return False



def install_version(version):
    try:
        result = subprocess.run(["pyenv", "versions", "--bare"],
                              capture_output=True,
                              text=True,
                              check=True)
        installed_versions = result.stdout.strip().split('\n')
        if version not in installed_versions:
            if is_valid_python_version(version):
                print("Installing python version...")
                subprocess.run(["pyenv", "install", version], check=True)
                return True  
            else:
                print(f"Invalid Python version: {version}")
                return False
        else:
            print(f"Python {version} already installed")
            return True 
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error with pyenv operations")
        return False



def install_packages(packages):
    if not packages.strip():
        print("No packages to install")
        return
    packages = packages.split(' ')
    venv_pip = f"/home/{os.getenv('USER')}/.pyenv/versions/{venv_name}/bin/pip"
    for package in packages:
        print(f"Installing {package} in {venv_name}...")
        subprocess.run([venv_pip, "install", package], check=True)


def delete_existing_venv(venv_name):
    """Delete virtual environment if it exists"""
    try:
        # Check if virtual environment exists
        result = subprocess.run(["pyenv", "versions", "--bare"], 
                               capture_output=True, text=True, check=True)
        existing_envs = result.stdout.strip().split('\n')
        
        if venv_name in existing_envs:
            print(f"Deleting existing virtual environment {venv_name}...")
            subprocess.run(["pyenv", "uninstall", "-f", venv_name], check=True)
            print(f"Deleted {venv_name}")
            return True
        else:
            print(f"Virtual environment {venv_name} doesn't exist")
            return False
    except subprocess.CalledProcessError as e:
        print(f"Error checking/deleting virtual environment: {e}")
        return False




if __name__ == "__main__":
    project_name = input("Project name: ")
    python_version = input('Python version: ')
    packages = input("Packages to be installed(leave blank if there are none): ")

    subprocess.run(["mkdir", project_name])
    install_version(python_version)
    os.chdir(project_name)

   

    #create a venv
    venv_name = f"{project_name}-{python_version}"
    delete_existing_venv(venv_name)
    subprocess.run(["pyenv", "virtualenv", python_version, venv_name], check=True)

    # set_local_environment(venv_name)
    install_packages(packages)

    subprocess.run(["code", "."])

    
