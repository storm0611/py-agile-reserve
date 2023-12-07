#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AgileReserveSysProject.settings')
    
    # import subprocess
    # subprocess.Popen([r'.\deviceScan\checkDetectedDevicesAutoUpdate.bat'])
    # subprocess.Popen([r'.\deviceScan\checkPriorityDevicesAutoUpdate.bat'])
    # subprocess.Popen([r'.\deviceScan\DeviceScanner.bat'])
    # subprocess.Popen([r'.\deviceScan\HostNameScanner.bat'])
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)



if __name__ == '__main__':
    main()
