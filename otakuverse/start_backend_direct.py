#!/usr/bin/env python
import subprocess
import sys
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Start uvicorn server
subprocess.run([
    sys.executable, '-m', 'uvicorn', 
    'api.server:app', 
    '--host', '127.0.0.1',
    '--port', '8001',
    '--reload'
], cwd=os.getcwd())
