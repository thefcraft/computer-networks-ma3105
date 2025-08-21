import socket
import struct
import logging

# NOTE: 
# ENCODING/DECODING
# ! => Means network (big-endian) byte order
# H => unsigned short (2 bytes, 16-bit)
# I => unsigned int (4 bytes, 32-bit)

class Client:
    def __init__(self, name: str, 
                 server_host: str, 
                 server_port: int) -> None:
        self.sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.server_host = server_host 
        self.server_port = server_port
        self.name = name
        logging.info("Initialized with name=%s, target=%s:%d",
                     self.name, self.server_host, self.server_port)
        
    def run(self):
        client_number = int(input("Enter an integer between 1 and 100: "))
        if not (1 <= client_number <= 100):
            logging.warning("Invalid number entered (%d), still sending to server (will cause server shutdown).",
                            client_number)
        
        logging.info("Connecting to %s:%d ...", self.server_host, self.server_port)
        self.sock.connect((self.server_host, self.server_port))
        logging.info("Connected to %s:%d", self.server_host, self.server_port)

        # Send: name length + name + integer
        name_bytes = self.name.encode("utf-8")
        self.sock.sendall(struct.pack("!H", len(name_bytes)))
        self.sock.sendall(name_bytes)
        self.sock.sendall(struct.pack("!I", client_number))
        logging.debug("ClientINFO -> name=%s, number=%d", self.name, client_number)

        # Stop locally if invalid number
        if not (1 <= client_number <= 100): 
            # NOTE: this kills the server as we already sent invalid data
            self.sock.close()
            logging.error("Invalid number (%d). Exiting client.", client_number)
            raise ValueError("Invalid number. Exiting.")

        # Receive: name length + name + integer
        raw_len = self.sock.recv(2)
        if not raw_len:
            logging.warning("No data received, server may have closed connection.")
            return
        name_len = struct.unpack("!H", raw_len)[0]
        server_name = self.sock.recv(name_len).decode("utf-8")
        server_number = struct.unpack("!I", self.sock.recv(4))[0]
        # Display
        total_sum = client_number + server_number
        logging.debug("ServerINFO <- name=%s, number=%d", server_name, server_number)
        logging.info("Computed sum: %d", total_sum)

        self.sock.close()
        logging.info("Connection closed.")

def main() -> None:
    client = Client(name='client', 
                    server_host='127.0.0.1', 
                    server_port=8080)
    client.run()

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,  # or INFO if you want less detail
        format="%(asctime)s [%(levelname)s] %(message)s",
    )
    main()