import matplotlib.pyplot as plt

def visualiser_12(throughput_data_file, av_throughput_data, rate_gap_file, short_gi_true_file, short_gi_false_file):

    visual_rate_gap = dict()

    throughputs = dict()

    short_gi_false = dict()
    short_gi_true = dict()

############################################################################################################################
#----------------------------------------------------Data extraction-------------------------------------
############################################################################################################################

    with open(short_gi_true_file,"r") as gi_true:
        for line in gi_true:
            data = line.strip().split('::')

            timestamp = float(data[0])
            RSSI = float(data[1])

            short_gi_true[timestamp] = RSSI


    with open(short_gi_false_file,"r") as gi_false:
        for line in gi_false:
            data = line.strip().split('::')

            timestamp = float(data[0])
            RSSI = float(data[1])

            short_gi_false[timestamp] = RSSI


    
    with open(throughput_data_file,"r") as throughput_file:
        for line in throughput_file:
            data = line.strip().split('::')

            timestamp = float(data[0])
            throughput = float(data[1])

            throughputs[timestamp] = throughput

    with open(rate_gap_file,"r") as rate_gap:
        for line in rate_gap:
            data = line.strip().split('::')

            timestamp = float(data[0])
            rate_gap = float(data[1])

            visual_rate_gap[timestamp] = rate_gap

    
    print(f"Total Frames: {av_throughput_data[0]}")
    print(f"Lost Frames: {av_throughput_data[1]}")
    print(f"Frame Loss Rate: {av_throughput_data[2]:.2%}")
    print(f"Average Data Rate (Mbps): {av_throughput_data[3]:.2f}")
    print(f"Average Throughput (Mbps): {av_throughput_data[4]:.2f}")

############################################################################################################################
#-----------------------------------------RSSI average of Short guard interval true and false plot across time--------------
############################################################################################################################

    timestamps_false  = short_gi_false.keys()
    rssi_false = [short_gi_false[sgf] for sgf in timestamps_false]

    timestamps_true  = short_gi_true.keys()
    rssi_true = [short_gi_true[sgf] for sgf in timestamps_true]

    plt.figure(1, figsize=(12, 6))

    plt.plot(timestamps_false, rssi_false, 'b-', label='Short GI = False', linewidth=2)
    plt.plot(timestamps_true, rssi_true, 'r-', label='Short GI = True', linewidth=2)

    plt.title("RSSI Comparison: Short Guard Interval (True vs False)", pad=20)
    plt.xlabel("Timestamp")
    plt.ylabel("RSSI (dBm)")
    plt.grid(True, alpha=0.3)
    plt.legend()

    plt.xticks(rotation=45)
    plt.tight_layout()

############################################################################################################################
#----------------------------------------------------Throughput and Rate gap plots across time----------------------------
############################################################################################################################

    throughput_timestamps = visual_rate_gap.keys()
    throughput_values = [visual_rate_gap[rg] for rg in throughput_timestamps]

    timestamps_for_rate_gap = throughputs.keys()
    values_for_rate_gap = [throughputs[ts] for ts in timestamps_for_rate_gap]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 5))

    ax1.plot(throughput_timestamps, throughput_values, 'b-')
    ax1.set_title("Rate Gap")
    ax1.set_xlabel("Timestamp")
    ax1.set_ylabel("Mbps")

    ax2.plot(timestamps_for_rate_gap, values_for_rate_gap, 'c-')
    ax2.set_title("Throughput")
    ax2.set_xlabel("Timestamp")

    for ax in [ax1, ax2]:
        ax.grid(True)
        ax.tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.show()