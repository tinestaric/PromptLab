"""
Setup script for the Prompt Engineering Workshop application.
Run this script to set up the development environment.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path


def create_env_file():
    """Create .env file from template if it doesn't exist."""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists() and env_example.exists():
        shutil.copy(env_example, env_file)
        print("✅ Created .env file from template")
        print("⚠️  Please edit .env file with your actual configuration")
    elif env_file.exists():
        print("✅ .env file already exists")
    else:
        print("❌ .env.example file not found")


def create_logs_directory():
    """Create logs directory if it doesn't exist."""
    logs_dir = Path("logs")
    if not logs_dir.exists():
        logs_dir.mkdir()
        print("✅ Created logs directory")
    else:
        print("✅ Logs directory already exists")


def install_dependencies():
    """Install Python dependencies."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Installed dependencies from requirements.txt")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False
    return True


def run_tests():
    """Run basic tests to verify setup."""
    try:
        subprocess.check_call([sys.executable, "-m", "pytest", "tests/", "-v"])
        print("✅ All tests passed")
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Some tests failed: {e}")
    except FileNotFoundError:
        print("⚠️  pytest not installed, skipping tests")


def main():
    """Main setup function."""
    print("🚀 Setting up Prompt Engineering Workshop...")
    print("=" * 50)
    
    # Change to script directory
    script_dir = Path(__file__).parent.parent
    os.chdir(script_dir)
    
    # Setup steps
    create_env_file()
    create_logs_directory()
    
    if install_dependencies():
        print("\n🧪 Running tests...")
        run_tests()
    
    print("\n" + "=" * 50)
    print("✅ Setup complete!")
    print("\nNext steps:")
    print("1. Edit .env file with your Azure OpenAI credentials")
    print("2. Run: streamlit run app.py")
    print("3. Open your browser to the displayed URL")


if __name__ == "__main__":
    main()
