import socket
import struct
import threading
import logging

# NOTE: 
# ENCODING/DECODING
# ! => Means network (big-endian) byte order
# H => unsigned short (2 bytes, 16-bit)
# I => unsigned int (4 bytes, 32-bit)

def get_local_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't need to succeed, just picks an outbound interface
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    finally:
        s.close()
        
class Server:
    def __init__(self, name: str, backlog: int = 5) -> None:
        self.sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.backlog = backlog
        self.name = name
        self.running = True
        self.server_number = int(input("Enter an integer between 1 and 100: "))
        if not (1 <= self.server_number <= 100):
            logging.error("Invalid number. Exiting.")
            raise ValueError("[SERVER] Invalid number. Exiting.")
        logging.info("Initialized with name=%s, number=%d, backlog=%d",
                     self.name, self.server_number, self.backlog)
    def client_handler(self, client: socket.socket, addr: tuple[str, int]):
        logging.info("Handling new client from %s", addr)
        try:
            # Receive: name length + name + integer
            raw_len = client.recv(2)
            if not raw_len:
                logging.warning("No data from %s, closing connection.", addr)
                return
            name_len = struct.unpack("!H", raw_len)[0]
            client_name = client.recv(name_len).decode("utf-8") 
            client_number = struct.unpack("!I", client.recv(4))[0]
            logging.info("Connected with %s", addr)
            logging.debug("ClientINFO <- name=%s, number=%d", client_name, client_number)
             
            if not (1 <= client_number <= 100):
                logging.error("Invalid number received from %s. Closing server.", addr)
                self.running = False
                self.sock.close()
                return

            # Compute sum
            total_sum = client_number + self.server_number
            logging.debug("ServerINFO -> name=%s, number=%d", self.name, self.server_number)
            logging.info("Sum with client %s: %d", addr, total_sum)
            
            # Send: name length + name + integer
            name_bytes = self.name.encode("utf-8")
            client.sendall(struct.pack("!H", len(name_bytes)))
            client.sendall(name_bytes)
            client.sendall(struct.pack("!I", self.server_number))
            
            logging.info("Sent response to %s -> name=%s, number=%d",
                         addr, self.name, self.server_number)

        finally:
            client.close()
            logging.info("Closed connection with %s", addr)
        
    def run(self, host: str = '127.0.0.1', port: int = 8080):
        self.sock.bind((host, port))
        self.sock.listen(self.backlog)
        
        logging.info("Listening on %s:%d.", host, port)
        if host == '0.0.0.0':
            logging.info("Listening on %s:%d.", get_local_ip(), port)
        
        # self.sock.setblocking(False)
        threads: list[threading.Thread] = []
        while self.running:
            try: 
                client, addr = self.sock.accept()                
                logging.info("Accepted connection from %s", addr)
            except OSError: 
                logging.info("Socket closed, stopping accept loop.")
                break  # socket closed
            # self.client_handler(client=client, addr=addr)
            thread = threading.Thread(
                target=self.client_handler, 
                args=(client, addr), 
                name=f'Client Handler for client(addr={addr})',
                daemon=True,
            )
            threads.append(thread)
            thread.start()
            
            threads = [t for t in threads if t.is_alive()] # Clean up finished threads
            
        logging.info("Waiting for active threads to finish...")
        for thread in threads:
            if thread.is_alive():
                logging.debug("Thread %s is alive, joining with timeout 0.5s", thread.name)
                thread.join(timeout=0.5)
        
        self.sock.close()
        logging.info("Socket closed, server shutdown complete.")
        
def main() -> None:
    server = Server(name='server', backlog=5)
    server.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )
    main()