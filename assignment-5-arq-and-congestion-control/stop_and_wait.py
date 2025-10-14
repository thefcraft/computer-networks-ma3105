import random
import time

def stop_and_wait_simulation(total_frames_count: int, loss_prob: float):
    print("--- Stop-and-Wait ARQ Simulation ---")
    next_frame_to_send = 0
    timeout = 2  # seconds

    while next_frame_to_send < total_frames_count:
        print(f"Sending Frame {next_frame_to_send}")

        ack_received = False
        start_time = time.time()

        while not ack_received:
            # Wait for ACK or timeout
            if time.time() - start_time > timeout:
                print(f"Timeout for Frame {next_frame_to_send}, retransmitting...")
                print(f"Sending Frame {next_frame_to_send}")
                start_time = time.time() # Reset timer on retransmission

            # Simulate receiver's side
            # Check if the frame is lost
            if random.random() < loss_prob:
                # Frame is lost, do nothing and wait for timeout
                time.sleep(0.5) # Wait a bit to simulate processing
                continue

            # Frame is received, now check if ACK is lost
            if random.random() < loss_prob:
                print(f"ACK for Frame {next_frame_to_send} was lost.")
                # ACK is lost, sender will time out
                time.sleep(0.5)
                continue

            # Both frame and ACK are successfully transmitted
            print(f"ACK {next_frame_to_send} received")
            ack_received = True
            next_frame_to_send += 1

    print("\n--- Simulation Complete ---")

if __name__ == "__main__":
    TOTAL_FRAMES_COUNT = 5
    LOSS_PROBABILITY = 0.3 # 30% chance of loss

    stop_and_wait_simulation(TOTAL_FRAMES_COUNT, LOSS_PROBABILITY)