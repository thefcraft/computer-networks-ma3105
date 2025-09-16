import cv2
import os
import socket
import time
import struct
import logging


CLIENT_IP = '127.0.0.1'
CLIENT_PORT = 9999
CHUNK_SIZE = 65500
VIDEO_PATH = os.path.join(os.path.dirname(__file__), 'suzume_1080p.mp4')

def main() -> None:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_addr = (CLIENT_IP, CLIENT_PORT)
    logging.info(f"Streaming video to {CLIENT_IP}:{CLIENT_PORT}")

    try:
        vid = cv2.VideoCapture(VIDEO_PATH)
        if not vid.isOpened():
            logging.error(f"Error: Could not open video file at {VIDEO_PATH}")
            return
    except Exception as e:
        logging.error(f"Error opening video capture: {e}")
        return

    fps: float = vid.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        logging.error(f"Error: Invalid FPS value ({fps}).")
        return

    frame_interval: float = 1 / fps
    logging.info(f"Video FPS: {fps:.2f}, Frame Interval: {frame_interval:.4f}s")

    try:
        while vid.isOpened():
            ret, frame = vid.read()
            if not ret:
                logging.info("End of video stream.")
                break

            frame = cv2.resize(frame, (640, 480)) # Resize frame to 640x480 for smaller payload
            result, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            if not result:
                logging.warning("Failed to encode frame.")
                continue

            data = buffer.tobytes()
            data_size = len(data)
            num_chunks = (data_size // CHUNK_SIZE) + 1

            for i in range(num_chunks):
                start = i * CHUNK_SIZE
                end = start + CHUNK_SIZE
                chunk = data[start:end]
                marker = 1 if i == num_chunks - 1 else 0
                header = struct.pack('!B', marker)
                message = header + chunk
                try:
                    server_socket.sendto(message, client_addr)
                except Exception as e:
                    logging.error(f"Failed to send chunk {i + 1}: {e}")
                    continue

            time.sleep(frame_interval) # sleep to maintain the frame rate

    finally:
        logging.info("Closing resources.")
        vid.release()
        server_socket.close()

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler()
        ]
    )
    main()
