#!/usr/bin/env python3
"""
Simple HTTP server that serves index.html for directory requests.
This is needed for proper navigation on the static site.
"""
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path


class DirectoryIndexHandler(SimpleHTTPRequestHandler):
    # Set the base path to serve from
    base_path = None
    
    def translate_path(self, path):
        """Translate a /-separated PATH to the local filename syntax."""
        path = path.rstrip('/')
        
        # Check if this is a directory-like request (no file extension)
        if '.' not in path.split('/')[-1]:
            index_path = os.path.join(self.base_path, path.lstrip('/'), 'index.html')
            if os.path.isfile(index_path):
                return index_path
        
        # Fall back to default behavior
        return os.path.join(self.base_path, path.lstrip('/'))
    
    def end_headers(self):
        # Add headers to prevent caching for better development experience
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        super().end_headers()
    
    def log_message(self, format, *args):
        """Log messages in a cleaner format"""
        print(f"{self.client_address[0]} - {format % args}")


if __name__ == '__main__':
    serve_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'public')
    DirectoryIndexHandler.base_path = serve_path
    
    server_address = ('', 8888)
    httpd = HTTPServer(server_address, DirectoryIndexHandler)
    
    print(f"Serving HTTP on 0.0.0.0 port 8888 (http://0.0.0.0:8888/) ...")
    print(f"Serving from: {serve_path}")
    print("Press Ctrl+C to stop.")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        sys.exit(0)
