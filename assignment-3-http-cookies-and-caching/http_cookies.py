import socket
import logging
import secrets

def generate_session_id(length: int = 16) -> str:
    return secrets.token_hex(length)


def parse_headers(request: str) -> dict[str, str]: # HEADER IS LOWERED...
    headers: dict[str, str] = {}
    lines = request.split("\r\n")
    for line in lines[1:]:  # Skip the first line (request line)
        if not line:
            break
        key, value = line.split(": ", 1)
        headers[key.lower()] = value
    return headers

def handle_request(client_socket: socket.socket):
    request = client_socket.recv(1024).decode()

    headers: dict[str, str] = parse_headers(request)
    cookies = headers.get("cookie", "")

    if "session_id" not in cookies:
        session_id = generate_session_id()
        logging.info(f"New session created: {session_id}")
        response_body = f"Welcome, new user! Your session ID is {session_id}"
        response_headers = [
            "HTTP/1.1 200 OK",
            "Content-Type: text/html",
            f"Set-Cookie: session_id={session_id}",
            "Connection: close",
            f"Content-Length: {len(response_body)}",
            "\r\n"
        ]
    else:
        session_id = cookies.split('=')[1]
        logging.info(f"Returning user with session ID: {session_id}")
        response_body = f"Welcome back, user with session ID {session_id}!"
        response_headers = [
            "HTTP/1.1 200 OK",
            "Content-Type: text/html",
            "Connection: close",
            f"Content-Length: {len(response_body)}",
            "\r\n"
        ]
        
    response = "\r\n".join(response_headers) + "\r\n" + response_body
    client_socket.sendall(response.encode())
    client_socket.close()
    
def mainloop(server_socket: socket.socket):
    while True:
        client_socket, client_address = server_socket.accept()
        logging.info(f"Connection from {client_address}")
        try: 
            handle_request(client_socket)
        finally:
            client_socket.close()

def start_server(host: str = '0.0.0.0', port: int = 8000):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    logging.info(f"Server started at {host}:{port}")
    try: 
        mainloop(server_socket)
    finally: 
        server_socket.close()
    

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler()
        ]
    )
    start_server()
