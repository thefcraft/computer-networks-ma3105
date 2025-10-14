import matplotlib.pyplot as plt

def tcp_congestion_control_simulation(total_rounds_count: int, initial_ssthresh: int, loss_events: list[int]):
    print("--- TCP Congestion Control Simulation ---")
    
    cwnd = 1  # Congestion window starts at 1 MSS
    ssthresh = initial_ssthresh
    
    cwnd_history: list[int] = []
    
    for round_num in range(total_rounds_count):
        cwnd_history.append(cwnd)
        
        print(f"Round {round_num+1}: cwnd = {cwnd}, ssthresh = {ssthresh}")
        
        # Check for a loss event (timeout)
        if round_num + 1 in loss_events:
            print(f"!! Packet Loss Detected at round {round_num + 1} !!")
            # Multiplicative Decrease 
            ssthresh = max(cwnd // 2, 2)
            cwnd = 1 # Reset cwnd to 1 MSS
            print("-> Entering Slow Start phase.")
            continue

        # Increase cwnd based on the current phase [cite: 48]
        if cwnd < ssthresh:
            # Slow Start Phase: exponential growth
            cwnd *= 2
            if round_num > 0 and cwnd_history[-1] >= ssthresh:
                 print("-> Entering Congestion Avoidance phase.")
        else:
            # Congestion Avoidance Phase: linear growth
            cwnd += 1

    # Plotting the results [cite: 50]
    plt.figure(figsize=(12, 6))
    plt.plot(range(1, total_rounds_count + 1), cwnd_history, marker='o', linestyle='-', label='cwnd')
    plt.axhline(y=initial_ssthresh, color='r', linestyle='--', label=f'Initial ssthresh = {initial_ssthresh}')
    
    for loss_round in loss_events:
        plt.axvline(x=loss_round, color='g', linestyle=':', label=f'Packet Loss at round {loss_round}')

    plt.title('TCP Congestion Window (cwnd) Simulation')
    plt.xlabel('Transmission Rounds')
    plt.ylabel('Congestion Window Size (in MSS)')
    plt.grid(True)
    plt.legend()
    plt.xticks(range(1, total_rounds_count + 1))
    
    # Save the plot
    plt.savefig('cwnd_plot.png')
    print("\nPlot saved as cwnd_plot.png")
    plt.show()


if __name__ == "__main__":
    TOTAL_ROUNDS_COUNT = 25
    INITIAL_SSTHRESH = 16
    LOSS_EVENTS_AT_ROUNDS = [8, 17] # Simulate packet loss (timeout) at these specific rounds
    
    tcp_congestion_control_simulation(TOTAL_ROUNDS_COUNT, INITIAL_SSTHRESH, LOSS_EVENTS_AT_ROUNDS)