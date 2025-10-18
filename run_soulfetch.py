import subprocess
import sys
import os

# Start backend
backend_cmd = [sys.executable, os.path.join('backend', 'main.py')]
backend_proc = subprocess.Popen(backend_cmd)

# Start frontend
frontend_cmd = [sys.executable, os.path.join('frontend', 'main.py')]
frontend_proc = subprocess.Popen(frontend_cmd)

backend_proc.wait()
frontend_proc.wait()
