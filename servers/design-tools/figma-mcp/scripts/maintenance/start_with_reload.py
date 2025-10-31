#!/usr/bin/env python3
"""
Auto-reload wrapper for figma_server_db.py
Monitors source files and restarts server when changes are detected
"""
import os
import sys
import time
import subprocess
import signal
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ServerReloader(FileSystemEventHandler):
    def __init__(self):
        self.server_process = None
        self.restart_server()
    
    def on_modified(self, event):
        if event.is_directory:
            return
        
        # Only restart on Python file changes
        if event.src_path.endswith('.py'):
            print(f"✨ File changed: {event.src_path}")
            print("🔄 Restarting MCP server...")
            self.restart_server()
    
    def restart_server(self):
        # Kill existing server
        if self.server_process:
            self.server_process.terminate()
            self.server_process.wait()
        
        # Start new server
        env = os.environ.copy()
        self.server_process = subprocess.Popen(
            [sys.executable, "src/figma_server_db.py"],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        print("🚀 MCP server restarted")

def main():
    print("🔍 Starting MCP server with auto-reload...")
    
    # Create event handler and observer
    event_handler = ServerReloader()
    observer = Observer()
    observer.schedule(event_handler, "src/", recursive=True)
    
    # Start monitoring
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
        observer.stop()
        if event_handler.server_process:
            event_handler.server_process.terminate()
    
    observer.join()

if __name__ == "__main__":
    main()