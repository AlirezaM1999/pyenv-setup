# Python Project Environment Setup

A simple Python script that automates the creation of Python projects with isolated virtual environments using pyenv.

## Features

- 🐍 **Automatic Python Version Management** - Installs Python versions if not available
- 🏠 **Project Directory Creation** - Creates organized project folders
- 📦 **Virtual Environment Setup** - Creates isolated environments using pyenv
- 🔧 **Package Installation** - Installs specified packages automatically
- 💻 **VSCode Integration** - Opens projects directly in VSCode
- 🔄 **Environment Cleanup** - Removes existing environments to avoid conflicts

## Prerequisites

Before using this script, make sure you have:

- [pyenv](https://github.com/pyenv/pyenv) installed and configured
- [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) plugin installed
- [VSCode](https://code.visualstudio.com/) installed (optional, but recommended)

### Installation of Prerequisites

**Install pyenv:**
```bash
# macOS
brew install pyenv pyenv-virtualenv

# Ubuntu/Debian
curl https://pyenv.run | bash
```

**Add to your shell configuration:**
```bash
# Add to ~/.bashrc, ~/.zshrc, etc.
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

## Usage

1. Clone this repository:
```bash
git clone https://github.com/yourusername/python-project-setup.git
cd python-project-setup
```

2. Run the script:
```bash
python create_env.py
```

3. Follow the prompts:
```
Project name: my-awesome-project
Python version: 3.11.5
Packages to be installed(leave blank if there are none): requests fastapi uvicorn
```

4. The script will:
   - Create a project directory
   - Install the specified Python version (if needed)
   - Create a virtual environment
   - Install the specified packages
   - Open the project in VSCode

## Example

```bash
$ python create_env.py
Project name: web-scraper
Python version: 3.10.12
Packages to be installed(leave blank if there are none): requests beautifulsoup4 pandas

Creating project directory: web-scraper
Python 3.10.12 already installed
Deleting existing virtual environment web-scraper-3.10.12...
Deleted web-scraper-3.10.12
Installing requests in web-scraper-3.10.12...
Installing beautifulsoup4 in web-scraper-3.10.12...
Installing pandas in web-scraper-3.10.12...
```

## How It Works

1. **Python Version Check**: Validates if the specified Python version exists in pyenv's available versions
2. **Installation**: Downloads and installs the Python version if not already available
3. **Environment Creation**: Creates a virtual environment named `{project-name}-{python-version}`
4. **Package Installation**: Uses the virtual environment's pip to install packages
5. **VSCode Launch**: Opens the project directory in VSCode for immediate development

## File Structure

After running the script, your project will have this structure:

```
my-project/
├── .python-version          # pyenv configuration (if using pyenv local)
└── (your project files)
```

The virtual environment is stored in `~/.pyenv/versions/my-project-3.11.5/` and managed by pyenv.

## Activating the Environment

### In VSCode
When you open the project in VSCode:
1. Select the Python interpreter: `Ctrl+Shift+P` → "Python: Select Interpreter"
2. Choose the environment that matches your project name
3. The environment will be automatically activated in VSCode's integrated terminal

### In Terminal
```bash
cd your-project-directory
pyenv activate your-project-python-version
```

## Troubleshooting

**"pyenv: command not found"**
- Make sure pyenv is installed and added to your PATH
- Restart your terminal after installation

**"Invalid Python version"**
- Use full version numbers (e.g., `3.11.5` instead of `3.11`)
- Check available versions with: `pyenv install --list`

**Packages installing globally instead of in virtual environment**
- The script uses the virtual environment's pip directly to avoid this issue
- If this persists, check that pyenv is properly configured

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [pyenv](https://github.com/pyenv/pyenv) for Python version management
- Inspired by the need for quick, isolated Python project setup