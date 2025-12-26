"""
Build script for creating Windows executable
Uses PyInstaller to package the chess game
"""

import os
import sys
import shutil
import subprocess

# Project information
APP_NAME = "ChessOnline"
VERSION = "1.0.0"
AUTHOR = "Nhom14"
DESCRIPTION = "Online Chess Game with Beautiful UI"

# Paths
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(ROOT_DIR, "dist")
BUILD_DIR = os.path.join(ROOT_DIR, "build")
ICON_PATH = os.path.join(ROOT_DIR, "assets", "icon.ico")

# Main entry point
MAIN_SCRIPT = os.path.join(ROOT_DIR, "client", "main_enhanced.py")


def check_requirements():
    """Check if required tools are installed"""
    print("📋 Checking requirements...")
    
    # Check PyInstaller
    try:
        import PyInstaller
        print("✅ PyInstaller installed")
    except ImportError:
        print("❌ PyInstaller not found!")
        print("   Install with: pip install pyinstaller")
        return False
    
    # Check if main script exists
    if not os.path.exists(MAIN_SCRIPT):
        print(f"❌ Main script not found: {MAIN_SCRIPT}")
        return False
    
    print("✅ Main script found")
    return True


def clean_build():
    """Clean previous build artifacts"""
    print("\n🧹 Cleaning previous builds...")
    
    for directory in [DIST_DIR, BUILD_DIR]:
        if os.path.exists(directory):
            shutil.rmtree(directory)
            print(f"   Removed {directory}")
    
    # Remove spec file
    spec_file = f"{APP_NAME}.spec"
    if os.path.exists(spec_file):
        os.remove(spec_file)
        print(f"   Removed {spec_file}")


def create_icon():
    """Create icon file if it doesn't exist"""
    assets_dir = os.path.join(ROOT_DIR, "assets")
    os.makedirs(assets_dir, exist_ok=True)
    
    # If icon doesn't exist, user needs to provide one
    if not os.path.exists(ICON_PATH):
        print("⚠️  No icon found. Using default icon.")
        return None
    
    return ICON_PATH


def build_executable():
    """Build the executable using PyInstaller"""
    print("\n🔨 Building executable...")
    
    icon = create_icon()
    
    # Find PyInstaller executable
    pyinstaller_cmd = "pyinstaller"
    if sys.platform == "win32":
        # Try to find in venv
        venv_pyinstaller = os.path.join(sys.prefix, "Scripts", "pyinstaller.exe")
        if os.path.exists(venv_pyinstaller):
            pyinstaller_cmd = venv_pyinstaller
        else:
            # Try python -m PyInstaller
            pyinstaller_cmd = [sys.executable, "-m", "PyInstaller"]
    
    # PyInstaller command
    if isinstance(pyinstaller_cmd, list):
        cmd = pyinstaller_cmd
    else:
        cmd = [pyinstaller_cmd]
    
    cmd.extend([
        "--name", APP_NAME,
        "--onefile",  # Single file
        "--windowed",  # No console window
        "--clean",
    ])
    
    # Add icon if available
    if icon:
        cmd.extend(["--icon", icon])
    
    # Add hidden imports
    hidden_imports = [
        "tkinter",
        "tkinter.ttk",
        "PIL",
        "PIL._tkinter_finder",
        "chess",
        "chess.engine",
        "chess.pgn",
        "pygame",
        "pygame.mixer",
        "numpy",
        "plyer"
    ]
    
    for imp in hidden_imports:
        cmd.extend(["--hidden-import", imp])
    
    # Add data files
    data_files = [
        ("common", "common"),
        ("client/ui", "client/ui"),
        ("client/network", "client/network"),
    ]
    
    for src, dst in data_files:
        if os.path.exists(src):
            cmd.extend(["--add-data", f"{src};{dst}"])
    
    # Main script
    cmd.append(MAIN_SCRIPT)
    
    # Run PyInstaller
    print(f"   Command: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=ROOT_DIR)
    
    if result.returncode == 0:
        print("✅ Build successful!")
        return True
    else:
        print("❌ Build failed!")
        return False


def create_portable_package():
    """Create a portable package with necessary files"""
    print("\n📦 Creating portable package...")
    
    package_dir = os.path.join(DIST_DIR, f"{APP_NAME}_Portable")
    os.makedirs(package_dir, exist_ok=True)
    
    # Copy executable
    exe_src = os.path.join(DIST_DIR, f"{APP_NAME}.exe")
    if os.path.exists(exe_src):
        shutil.copy2(exe_src, package_dir)
        print(f"   Copied {APP_NAME}.exe")
    
    # Copy README
    readme_src = os.path.join(ROOT_DIR, "README.md")
    if os.path.exists(readme_src):
        shutil.copy2(readme_src, package_dir)
        print("   Copied README.md")
    
    # Copy QUICKSTART
    quickstart_src = os.path.join(ROOT_DIR, "QUICKSTART.md")
    if os.path.exists(quickstart_src):
        shutil.copy2(quickstart_src, package_dir)
        print("   Copied QUICKSTART.md")
    
    # Create server folder
    server_dir = os.path.join(package_dir, "server")
    shutil.copytree(os.path.join(ROOT_DIR, "server"), server_dir)
    print("   Copied server files")
    
    # Create common folder
    common_dir = os.path.join(package_dir, "common")
    shutil.copytree(os.path.join(ROOT_DIR, "common"), common_dir)
    print("   Copied common files")
    
    # Create launcher script
    create_launcher(package_dir)
    
    print(f"✅ Portable package created at: {package_dir}")
    
    return package_dir


def create_launcher(package_dir):
    """Create convenient launcher scripts"""
    
    # Windows batch file for running server
    server_bat = os.path.join(package_dir, "Run_Server.bat")
    with open(server_bat, 'w') as f:
        f.write("@echo off\n")
        f.write("echo Starting Chess Server...\n")
        f.write("python server/main.py\n")
        f.write("pause\n")
    
    print("   Created Run_Server.bat")
    
    # Windows batch file for running client
    client_bat = os.path.join(package_dir, "Run_Client.bat")
    with open(client_bat, 'w') as f:
        f.write("@echo off\n")
        f.write(f"echo Starting {APP_NAME}...\n")
        f.write(f"start {APP_NAME}.exe\n")
    
    print("   Created Run_Client.bat")
    
    # Create README for package
    package_readme = os.path.join(package_dir, "HOW_TO_RUN.txt")
    with open(package_readme, 'w', encoding='utf-8') as f:
        f.write(f"{'='*60}\n")
        f.write(f"  {APP_NAME} - Portable Version\n")
        f.write(f"{'='*60}\n\n")
        f.write("🎮 HOW TO RUN:\n\n")
        f.write("1. START SERVER:\n")
        f.write("   - Double-click 'Run_Server.bat'\n")
        f.write("   - OR run: python server/main.py\n")
        f.write("   - Keep this window open!\n\n")
        f.write("2. START CLIENT:\n")
        f.write("   - Double-click 'ChessOnline.exe'\n")
        f.write("   - OR double-click 'Run_Client.bat'\n\n")
        f.write("3. PLAY:\n")
        f.write("   - Enter username\n")
        f.write("   - Create room or join existing room\n")
        f.write("   - Wait for opponent\n")
        f.write("   - Enjoy!\n\n")
        f.write(f"{'='*60}\n")
        f.write("📝 REQUIREMENTS:\n")
        f.write("   - Python 3.8+ (for server)\n")
        f.write("   - No requirements for .exe client!\n\n")
        f.write(f"{'='*60}\n")
        f.write(f"Made with ❤️ by {AUTHOR}\n")
        f.write(f"Version {VERSION}\n")
    
    print("   Created HOW_TO_RUN.txt")


def main():
    """Main build process"""
    print("="*60)
    print(f"  Building {APP_NAME} v{VERSION}")
    print("="*60)
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Build aborted due to missing requirements")
        return 1
    
    # Clean previous builds
    clean_build()
    
    # Build executable
    if not build_executable():
        print("\n❌ Build failed!")
        return 1
    
    # Create portable package
    package_dir = create_portable_package()
    
    print("\n" + "="*60)
    print("✅ BUILD COMPLETE!")
    print("="*60)
    print(f"\n📂 Output location: {package_dir}")
    print(f"\n🚀 To run:")
    print(f"   1. Run server: python server/main.py")
    print(f"   2. Run client: {APP_NAME}.exe")
    print("\n💡 Or use the launcher scripts in the package!")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
