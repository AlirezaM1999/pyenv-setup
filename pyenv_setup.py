import subprocess, os, sys, logging, requests

# Configure logging to show timestamp, log level, and message
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()  # Log to console
    ]
)

# -----------------------------------------------------
# Check if pyenv is installed by running "pyenv --version".
# Exit the script if pyenv is not found.
# -----------------------------------------------------
def check_pyenv_installed():
    try:
        subprocess.run(["pyenv", "--version"], check=True, capture_output=True)
    except FileNotFoundError:
        logging.error("Error: pyenv is not installed. Please install pyenv first")
        sys.exit(1)

# -----------------------------------------------------
# Check if a Python version is valid by comparing it 
# against the list of available pyenv install versions.
# -----------------------------------------------------
def is_valid_python_version(version: str) -> bool:
    try:
        result = subprocess.run(
            ["pyenv", "install", "--list"],
            capture_output=True,
            text=True,
            check=True
        )
        # Clean up version list and see if our version matches
        available_versions = [v.strip() for v in result.stdout.splitlines() if v.strip()]
        return version in available_versions
    except subprocess.CalledProcessError as e:
        logging.info("Error fetching versions:", e)
        return False

# -----------------------------------------------------
# Install a given Python version if not already installed.
# Uses `is_valid_python_version()` to verify the version.
# Raises SystemExit if the version is invalid.
# -----------------------------------------------------
def install_version(version):
    try:
        result = subprocess.run(["pyenv", "versions", "--bare"],
                              capture_output=True,
                              text=True,
                              check=True)
        installed_versions = result.stdout.strip().split('\n')
        
        # Install the version if not present
        if version not in installed_versions:
            if is_valid_python_version(version):
                logging.warning("Installing python version. This may take awhile...")
                subprocess.run(["pyenv", "install", version], check=True)
                return True  
            else:
                # Abort script if version is invalid
                raise SystemExit(f"Invalid Python version: {version}")
        else:
            logging.info(f"Python {version} already installed")
            return True 
    except (subprocess.CalledProcessError, FileNotFoundError):
        logging.error("Error with pyenv operations")
        sys.exit(1)

# -----------------------------------------------------
# Check if a Python package is valid using pip's `--dry-run`.
# This checks package availability without installing it.
# -----------------------------------------------------
def is_package_valid(venv_pip, package):
    try:
        subprocess.run([venv_pip, "install", package, "--dry-run"], 
                       capture_output=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

# -----------------------------------------------------
# Fetch the latest version of a package from PyPI using the JSON API.
# Returns (True, "package==version") if found, otherwise (False, None).
# -----------------------------------------------------
def get_package_info(package):
    url = f"https://pypi.org/pypi/{package}/json"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            package_info = package + "==" + data['info']['version']
            return True, package_info 
        return False, None
    except requests.RequestException as e:
        logging.error(f"Network error while checking {package}: {e}")
        return False, None

# -----------------------------------------------------
# Install packages into the virtual environment.
# - Creates a requirements.txt file with validated packages.
# - Only installs packages that are valid and exist on PyPI.
# -----------------------------------------------------
def install_packages(venv_name, packages):
    if not packages:
        logging.info("No packages to install")
        return

    # Clear/create requirements.txt
    open("requirements.txt", "w").close()
    venv_pip = f"/home/{os.getenv('USER')}/.pyenv/versions/{venv_name}/bin/pip"

    # Remove duplicate packages while preserving order
    packages = list(dict.fromkeys(packages)) 

    for package in packages:
        if is_package_valid(venv_pip, package):
            valid, package_info = get_package_info(package)
            if valid:
                with open('requirements.txt', 'a') as file:
                    file.write(package_info + '\n')
            else:
                logging.warning(f"Package {package} is invalid or not found")

    # Install from requirements.txt if it is not empty
    try:
        if os.path.getsize("requirements.txt") == 0:
            logging.info("No valid packages to install. Skipping pip install.")
            return
        else:
            logging.info("Installing Packages...")
            subprocess.run([venv_pip, "install", "-r", "requirements.txt"], check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error {e}")
        sys.exit(1)

# -----------------------------------------------------
# Delete an existing pyenv virtual environment if it exists.
# -----------------------------------------------------
def delete_existing_venv(venv_name):
    try:
        result = subprocess.run(["pyenv", "versions", "--bare"], 
                               capture_output=True, text=True, check=True)
        existing_envs = result.stdout.strip().split('\n')
        
        if venv_name in existing_envs:
            logging.warning(f"Deleting existing virtual environment {venv_name}...")
            subprocess.run(["pyenv", "uninstall", "-f", venv_name], check=True)
            logging.info(f"Deleted {venv_name}")
            return True
        else:
            logging.info(f"Virtual environment {venv_name} doesn't exist")
            return False
    except subprocess.CalledProcessError as e:
        logging.info(f"Error checking/deleting virtual environment: {e}")
        return False

# -----------------------------------------------------
# Validate and parse command-line arguments.
# Requires:
#   1. Project name
#   2. Python version
#   3. (Optional) list of packages to install
# -----------------------------------------------------
def check_argv_length():
    if len(sys.argv) < 3:
        raise SystemExit(
            "You must provide at least 2 arguments: <project_name> <python_version> [packages...]"
        )
    
    project_name = sys.argv[1]
    python_version = sys.argv[2]
    packages = sys.argv[3:]  # Treat everything after python_version as packages
    return project_name, python_version, packages

# -----------------------------------------------------
# Main script execution
# -----------------------------------------------------
if __name__ == "__main__":

    # Ensure pyenv is installed
    check_pyenv_installed()

    # Parse command-line arguments
    project_name, python_version, packages = check_argv_length()

    # Check if project folder already exists
    if os.path.exists(project_name):
        logging.error(f"Error: The directory '{project_name}' already exists.")
        sys.exit(1)
    else:
        os.makedirs(project_name, exist_ok=True)
    
    # Install the requested Python version if needed
    install_version(python_version)
        
    # Move into the project directory
    os.chdir(project_name)

    # Create a new virtual environment
    venv_name = f"{project_name}-{python_version}"
    delete_existing_venv(venv_name)
    subprocess.run(["pyenv", "virtualenv", python_version, venv_name], check=True)

    # Install user-requested packages
    install_packages(venv_name, packages)

    # Open project in VSCode
    subprocess.run(["code", "."])
