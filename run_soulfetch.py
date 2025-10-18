import subprocess
import sys

# Start backend as module
backend_cmd = [sys.executable, '-m', 'backend.main']
backend_proc = subprocess.Popen(backend_cmd)

# Start frontend as module
frontend_cmd = [sys.executable, '-m', 'frontend.main']
frontend_proc = subprocess.Popen(frontend_cmd)

backend_proc.wait()
frontend_proc.wait()
