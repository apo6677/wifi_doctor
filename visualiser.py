import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import random
from matplotlib.patches import Patch

def visualiser(density_data, channel_data):
    number = 1

    BSSIDs = dict()
    CHANNELS = dict()
    channel_occ = dict()
    heatmap_data = []

    Bar_Bssids = dict()

############################################################################################################################
#----------------------------------------------------Extracting data for differen graphs----------------------------
############################################################################################################################
  
    for file in density_data:
        with open(file, "r") as density_file:
            for line in density_file:
                data = line.strip().split("::")
                bssid = data[0]
                frequency = int(data[2])
                rssi = float(data[1])
                timestamps = [float(i) for i in data[3].strip("[]").split(',')]
                strengths = [int(i) for i in data[4].strip("[]").split(',')]
                channel = int(data[5])

                if (bssid, channel) not in BSSIDs:
                    BSSIDs[(bssid, channel)] = {"freq": frequency, "timestamps": timestamps, "strengths": strengths}


                if channel not in channel_occ:
                    channel_occ[channel]=[]
                if (bssid, channel) not in channel_occ[channel]:
                    channel_occ[channel].append((bssid, channel))

                if bssid not in Bar_Bssids:
                    Bar_Bssids[bssid] = {"strength": rssi, "freq": frequency}



    for file in channel_data:
        with open(file, "r") as density_file:
            for line in density_file:
                data = line.strip().split("::")
                frequency = int(data[2])
                rssi = float(data[1])
                channel = int(data[0])
                channel_count = int(data[3])


                if channel not in CHANNELS:
                    CHANNELS[channel] = {"freq": frequency, "strength": rssi, "packet_count": channel_count}

############################################################################################################################
#----------------------------------------------------BSSIDs RSSI average plot across frequency----------------------------
############################################################################################################################

    frequencies = []
    signal_strengths = []
    bssid_labels = []


    for bssid, values in Bar_Bssids.items():
       frequencies.append(values["freq"])
       signal_strengths.append(values["strength"]+100)
       bssid_labels.append(bssid)

    if sum(frequencies)/len(frequencies)<3000:
        bw = 20
    elif sum(frequencies)/len(frequencies)>4500:
        bw = 40
    else: print("Not possible to plot for different frequency bands")


    color_map = {bssid: f"#{random.randint(0, 0xFFFFFF):06x}" for bssid in bssid_labels}
    colors = [color_map[bssid] for bssid in bssid_labels]

    # Set plot limits
    min_freq = min(frequencies) - 20
    max_freq = max(frequencies) + 20

    # Generate tick positions every 5 MHz
    tick_positions = list(range(min_freq, max_freq + 1, 5))

    # Create Plot
    plt.figure(number, figsize=(12, 6))
    number+=1
    plt.bar(
        frequencies,
        signal_strengths,
        width=bw,
        color=colors,
        edgecolor="black",
        alpha=0.5,
        align="center",
        bottom = -100
    )

    # Create legend using the exact colors used in the plot
    legend_patches = [Patch(color=color_map[bssid], label=bssid) for bssid in bssid_labels]
    plt.legend(handles=legend_patches, loc="upper right", fontsize=8, frameon=True)

    # Labels and Titles
    plt.xlabel("Frequency (MHz)")
    plt.ylabel("Signal Strength (dBm)")
    plt.title("Wi-Fi Signal Strength by Frequency and BSSID")
    plt.ylim(-100, 0)  # Signal Strength range (dBm)
    plt.xlim(min_freq, max_freq)  # Frequency range (-20 to +60 MHz from min/max)
    plt.xticks(tick_positions)  # Set ticks every 5 MHz
    plt.grid(axis="y", linestyle="--")

############################################################################################################################
#-------------------------------Heatmap relating average Signal strength of different channels-----------------------
############################################################################################################################


    legend_patches = None

    data = []
    for channel, values in CHANNELS.items():
        data.append([channel, values["freq"], values["strength"]])

    df = pd.DataFrame(data, columns=["Channel", "Frequency", "RSSI"])

    # Pivot data to create heatmap format
    heatmap_data = df.pivot(index="Channel", columns="Frequency", values="RSSI")

    # Create heatmap
    plt.figure(number,figsize=(8, 6))
    number+=1
    ax = sns.heatmap(
        heatmap_data, annot=True, fmt=".1f", cmap="coolwarm", linewidths=0.5,
        cbar_kws={'label': 'Average RSSI (dBm)'}
    )

    # Titles and labels
    plt.title("Heatmap of Signal Strength (RSSI) across Frequency and Channel")
    plt.xlabel("FREQUENCY")
    plt.ylabel("CHANNEL")

############################################################################################################################
#----------------------------------------------------Channel packet counter bar chart----------------------------
############################################################################################################################

    channels = list(CHANNELS.keys())
    packet_counts = [CHANNELS[ch]["packet_count"] for ch in channels]

    # Create bar chart
    plt.figure(number,figsize=(8, 6))
    number+=1
    plt.bar(channels, packet_counts, color="royalblue", alpha=0.7, edgecolor="black")

    # Labels and Titles
    plt.xlabel("Wi-Fi Channel")
    plt.ylabel("Packet Count")
    plt.title("Packet Count per Wi-Fi Channel")
    plt.xticks(channels) 

############################################################################################################################
#----------------------------------------------------BSSIDs RSSI plot across time for each channel-------------------------
############################################################################################################################
    
    for channel, bssid_list in channel_occ.items():
        plt.figure(number ,figsize=(12, 6))  # New figure for each channel
        number+=1

        for (bssid, ch) in bssid_list:
            if (bssid, ch) in BSSIDs:  # Ensure the key exists
                plt.plot(
                    BSSIDs[(bssid, ch)]["timestamps"],
                    BSSIDs[(bssid, ch)]["strengths"],
                    label=f'BSSID: {bssid}',
                    linewidth=2
                )

        plt.title(f"RSSI Over Time (Channel {channel})")
        plt.xlabel("Timestamp")
        plt.ylabel("RSSI (dBm)")
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
    plt.show() 
