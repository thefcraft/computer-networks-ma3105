import random
import time

def go_back_n_simulation(total_frames_count: int, window_size: int, loss_prob: float):
    print(f"--- Go-Back-N ARQ Simulation (Window Size: {window_size}) ---")
    base = 0
    next_seq_num = 0
    
    while base < total_frames_count:
        # Send all frames within the current window
        while next_seq_num < base + window_size and next_seq_num < total_frames_count:
            print(f"Sending Frame {next_seq_num}")
            time.sleep(0.5) # Simulate transmission time
            next_seq_num += 1

        # Simulate receiving acknowledgments
        # In Go-Back-N, the receiver sends a cumulative ACK for the last correctly received in-order frame.
        ack_to_receive = base 
        
        # Simulate potential loss of frames within the window
        lost_frame = -1
        for i in range(base, next_seq_num):
            if random.random() < loss_prob:
                lost_frame = i
                print(f"!! Frame {lost_frame} was lost.")
                break # First loss in the window breaks transmission
        
        if lost_frame != -1:
            # No frames are acknowledged beyond the lost one.
            # The base remains the same, sender will time out and retransmit.
            print(f"Timeout! Retransmitting from Frame {lost_frame}.")
            next_seq_num = lost_frame # Go back N
        else:
            # All frames in the window were received successfully
            ack_to_receive = next_seq_num
            print(f"-> Cumulative ACK {ack_to_receive} received. Window slides.")
            base = next_seq_num
            
        print("-" * 20)

    print("\n--- Simulation Complete ---")


if __name__ == "__main__":
    TOTAL_FRAMES_COUNT = 10
    WINDOW_SIZE = 4
    LOSS_PROBABILITY = 0.2 # 20% chance of loss

    go_back_n_simulation(TOTAL_FRAMES_COUNT, WINDOW_SIZE, LOSS_PROBABILITY)