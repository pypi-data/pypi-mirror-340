# Import necessary Python standard libraries
import os          # For operating with file system, handling files and directory paths
import json        # For processing JSON format data
import subprocess  # For creating and managing subprocesses
import sys         # For accessing Python interpreter related variables and functions
import platform    # For getting current operating system information
import shutil      # For checking if executables exist in PATH

def check_prerequisites():
    """
    Check if necessary prerequisites are installed
    
    Returns:
        tuple: (python_ok, uv_installed, uvx_installed, terminal_controller_installed)
    """
    # Check Python version
    python_version = sys.version_info
    python_ok = python_version.major >= 3 and python_version.minor >= 11
    
    # Check if uv/uvx is installed
    uv_installed = shutil.which("uv") is not None
    uvx_installed = shutil.which("uvx") is not None
    
    # Check if terminal-controller is already installed via pip
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "show", "terminal-controller"],
            capture_output=True,
            text=True,
            check=False
        )
        terminal_controller_installed = result.returncode == 0
    except Exception:
        terminal_controller_installed = False
        
    return (python_ok, uv_installed, uvx_installed, terminal_controller_installed)

def setup_venv():
    """
    Function to set up Python virtual environment
    
    Features:
    - Checks if Python version meets requirements (3.11+)
    - Creates Python virtual environment (if it doesn't exist)
    - Installs required dependencies in the newly created virtual environment
    
    No parameters required
    
    Returns: Path to Python interpreter in the virtual environment
    """
    # Check Python version
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 11):
        print("Error: Python 3.11 or higher is required.")
        sys.exit(1)
    
    # Get absolute path of the directory containing the current script
    base_path = os.path.abspath(os.path.dirname(__file__))
    # Set virtual environment directory path, will create a directory named '.venv' under base_path
    venv_path = os.path.join(base_path, '.venv')
    # Flag whether a new virtual environment was created
    venv_created = False


    
    # Determine pip and python executable paths based on operating system
    is_windows = platform.system() == "Windows"
    if is_windows:
        pip_path = os.path.join(venv_path, 'Scripts', 'pip.exe')
        python_path = os.path.join(venv_path, 'Scripts', 'python.exe')
    else:
        pip_path = os.path.join(venv_path, 'bin', 'pip')
        python_path = os.path.join(venv_path, 'bin', 'python')
    
    # Install or update dependencies
    print("\nInstalling requirements...")

    
    # Also install dependencies from requirements.txt if it exists
    requirements_path = os.path.join(base_path, 'requirements.txt')
    if os.path.exists(requirements_path):
        subprocess.run([pip_path, 'install', '-r', requirements_path], check=True)
    
    # Install the local package in development mode
    print("\nInstalling terminal-controller in development mode...")
    subprocess.run([pip_path, 'install', '-e', base_path], check=True)
    
    print("Requirements installed successfully!")
    
    return python_path

def generate_mcp_config_local(python_path):
    """
    Generate MCP configuration for locally installed terminal-controller
    
    Parameters:
    - python_path: Path to Python interpreter in the virtual environment
    
    Returns: Path to the generated config file
    """
    # Get absolute path of the directory containing the current script
    base_path = os.path.abspath(os.path.dirname(__file__))
    
    # Path to Terminal Controller server script
    server_script_path = os.path.join(base_path, 'terminal_controller.py')
    
    # Create MCP configuration dictionary
    config = {
        "mcpServers": {
            "terminal-controller": {
                "command": python_path,
                "args": [server_script_path],
                "env": {
                    "PYTHONPATH": base_path
                }
            }
        }
    }
    
    # Save configuration to JSON file
    config_path = os.path.join(base_path, 'mcp-config.json')
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)  # indent=2 gives the JSON file good formatting
    
    return config_path

def generate_mcp_config_uvx():
    """
    Generate MCP configuration for PyPI-installed terminal-controller using UVX
    
    Returns: Path to the generated config file
    """
    # Get absolute path of the directory containing the current script
    base_path = os.path.abspath(os.path.dirname(__file__))
    
    # Create MCP configuration dictionary
    config = {
        "mcpServers": {
            "terminal-controller": {
                "command": "uvx",
                "args": ["terminal_controller"],
                "env": {}
            }
        }
    }
    
    # Save configuration to JSON file
    config_path = os.path.join(base_path, 'mcp-config.json')
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)  # indent=2 gives the JSON file good formatting
    
    return config_path

def generate_mcp_config_module():
    """
    Generate MCP configuration for PyPI-installed terminal-controller using direct script path
    
    Returns: Path to the generated config file
    """
    # Get absolute path of the directory containing the current script
    base_path = os.path.abspath(os.path.dirname(__file__))
    
    # Path to the actual script
    script_path = os.path.join(base_path, 'terminal_controller.py')
    
    # Create MCP configuration dictionary
    config = {
        "mcpServers": {
            "terminal-controller": {
                "command": sys.executable,
                "args": [script_path],
                "env": {
                    "PYTHONPATH": base_path
                }
            }
        }
    }
    
    # Save configuration to JSON file
    config_path = os.path.join(base_path, 'mcp-config.json')
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)  # indent=2 gives the JSON file good formatting
    
    return config_path

def install_from_pypi():
    """
    Install terminal-controller from PyPI
    
    Returns: True if successful, False otherwise
    """
    print("\nInstalling terminal-controller from PyPI...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "terminal-controller"], check=True)
        print("terminal-controller successfully installed from PyPI!")
        return True
    except subprocess.CalledProcessError:
        print("Failed to install terminal-controller from PyPI.")
        return False

def print_config_instructions(config_path):
    """
    Print instructions for using the generated config
    
    Parameters:
    - config_path: Path to the generated config file
    """
    print(f"\nMCP configuration has been written to: {config_path}")
    
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    print("\nMCP configuration for Claude Desktop:")
    print(json.dumps(config, indent=2))
    
    # Provide instructions for adding configuration to Claude Desktop configuration file
    if platform.system() == "Windows":
        claude_config_path = os.path.expandvars("%APPDATA%\\Claude\\claude_desktop_config.json")
    else:  # macOS
        claude_config_path = os.path.expanduser("~/Library/Application Support/Claude/claude_desktop_config.json")
    
    print(f"\nTo use with Claude Desktop, merge this configuration into: {claude_config_path}")

# Code executed when the script is run directly (not imported)
if __name__ == '__main__':
    python_path = setup_venv()
    config_path = generate_mcp_config_local(python_path)
    print_config_instructions(config_path)
    print("\nSetup complete! You can now use the Terminal Controller MCP server with compatible clients.")