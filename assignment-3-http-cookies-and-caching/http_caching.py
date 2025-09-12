import os
import hashlib
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer # NOTE: wrapper around socket for basic protocols
from datetime import datetime, timezone
import logging

indexfilepath = os.path.join(
    os.path.dirname(__file__), 
    'index.html'
)

class CachingHTTPRequestHandler(SimpleHTTPRequestHandler):
    def _get_etag(self, filepath: str):
        """Generate ETag using MD5 hash of file contents."""
        with open(filepath, 'rb') as f:
            file_content = f.read()
        return hashlib.md5(file_content).hexdigest()
    
    def _get_last_modified(self, filepath: str):
        """Get the last modified time of the file."""
        timestamp = os.path.getmtime(filepath)
        return datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')

    def do_GET(self):
        """Handle GET request with ETag and Last-Modified headers."""
        client_ip = self.client_address[0]  # Capture client IP address
        method = self.command
        url = self.path
        logging.info(f"Incoming request: {method} {url} from {client_ip}")
        
        if not os.path.exists(indexfilepath):
            logging.error(f"File not found: {indexfilepath}")
            self.send_error(404, "File not found")
            logging.info(f"Request {method} {url} completed with status 404.")
            return
        
        etag = self._get_etag(indexfilepath)
        last_modified = self._get_last_modified(indexfilepath)

        if_none_match = self.headers.get('If-None-Match')
        if_modified_since = self.headers.get('If-Modified-Since')

        logging.debug(f"If-None-Match: {if_none_match}")
        logging.debug(f"If-Modified-Since: {if_modified_since}")
        
        if if_none_match == etag or if_modified_since == last_modified:
            logging.info(f"Cache hit: 304 Not Modified for {url}")
            self.send_response(304)
            self.send_header('ETag', etag)
            self.send_header('Last-Modified', last_modified)
            self.end_headers()
            logging.info(f"Request {method} {url} completed with status 304.")
            return
        
        logging.info(f"Serving file: {indexfilepath} for {url}")
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.send_header('ETag', etag)
        self.send_header('Last-Modified', last_modified)
        self.send_header('Cache-Control', 'public, max-age=86400') # NOTE: Cache for 1 day
        self.end_headers()
        
        with open(indexfilepath, 'rb') as file:
            self.wfile.write(file.read())
        logging.info(f"Request {method} {url} completed with status 200.")

def main(host: str = '0.0.0.0', port: int = 8080):
    """Start the HTTP server."""
    server_address = (host, port)
    httpd: TCPServer | None = None
    try:
        httpd = TCPServer(server_address, CachingHTTPRequestHandler)
        logging.info(f"Starting server on {host}:{port}...")
        httpd.serve_forever()
    except Exception as e:
        logging.error(f"Error starting server: {e}")
    finally:
        if httpd is None: return
        httpd.server_close()
        logging.info(f"Server on {host}:{port} closed.")
            
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler()
        ]
    )
    main()
