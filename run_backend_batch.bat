@echo off
cd /d "c:\Users\Shriyansh Mishra\Documents\Codes\Projects\ai-agents-adk\otakuverse"
"C:\Users\Shriyansh Mishra\AppData\Local\Microsoft\WindowsApps\python.exe" -m uvicorn api.server_v2:app --host 0.0.0.0 --port 8000
