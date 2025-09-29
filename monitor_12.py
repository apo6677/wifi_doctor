def monitor(throughput_files):          
    
    total_frames = 0
    losses = 0
    rates = []

    data_frames = dict()
    lost_frames = dict()
    data_rates = dict()
    throughput = dict()

    rate_gaps = dict()

    short_gi_true = dict()
    short_gi_false = dict()

############################################################################################################################
#--------------------------------------------Extract data from parser and store them in---------------------------------
# ------------------------------------------the appropriately named dictionaries in order to calculate throughput----------
############################################################################################################################

    with open(throughput_files[0],"r") as throughput_file: # this is for thruoghput
        for line in throughput_file:
            data = line.strip().split('::')

            timestamp = float(data[0])
            data_rate = float(data[1])
            signal_strength = int(data[2])
            short_gi = int(data[3])
            total_frames+=1
            rates.append(data_rate)

            data_frames[timestamp] = {"data_rate": data_rate, "RSSI": signal_strength, "short_gi": short_gi}

############################################################################################################################
#----------------------------------------------------Calculate and store rate gap in dict rate_gaps-------------------------
############################################################################################################################

    for timestamp in data_frames:
        data_rate = data_frames[timestamp]["data_rate"]
        RSSI = data_frames[timestamp]["RSSI"]
        short_gi = data_frames[timestamp]["short_gi"]

        if RSSI > -40 and short_gi == 1:
            if data_rate < 144.4:
                rate_gaps[timestamp] = 144.4 - data_rate
            else: rate_gaps[timestamp] = 0
        elif RSSI > -40 and short_gi ==0:
            if data_rate < 130:
                rate_gaps[timestamp] = 130 - data_rate
            else: rate_gaps[timestamp] = 0

############################################################################################################################
#----------------------------------------------------Store short guard interval in dicts over time-------------------------
############################################################################################################################

    for timestamp in data_frames:
        RSSI = data_frames[timestamp]["RSSI"]
        short_gi = data_frames[timestamp]["short_gi"]

        if short_gi == 1:
            short_gi_true[timestamp] =  RSSI
        elif short_gi == 0:
            short_gi_false[timestamp] = RSSI


    with open(throughput_files[1],"r") as throughput_file:
        for line in throughput_file:
            data = line.strip().split('::')

            timestamp = float(data[0])
            data_rate = float(data[1])
            losses +=1
            total_frames+=1
            rates.append(data_rate)

            lost_frames[timestamp] = data_rate

######################################################################################################################
#---------------------------------Sort dictionaries regarding throughput by timestamp and------------------------
# ------------------------------- store in dictionary data_rates as well as calculate -------------------------
# --------------------------------how many packets have been lost up to the i-th timestamp ----------------
#####################################################################################################################

    L = 0
    all_timestamps = sorted(set(data_frames.keys()).union(lost_frames.keys()))

    for timestamp in all_timestamps:
        if timestamp in data_frames and timestamp in lost_frames:
            L += 1
            data_rates[timestamp] = {
                "data_rate": lost_frames[timestamp],
                "frame_losses": L
            }
        elif timestamp in data_frames:
            data_rates[timestamp] = {
                "data_rate": data_frames[timestamp]["data_rate"],
                "frame_losses": L
            }
        elif timestamp in lost_frames:
            L += 1
            data_rates[timestamp] = {
                "data_rate": lost_frames[timestamp],
                "frame_losses": L
            }

############################################################################################################################
#----------------------------------------------------Calculating Throughput for every timestamp----------------------------
############################################################################################################################

    prev_timestamp = None
    length = 1

    for timestamp in data_rates:
        if prev_timestamp is not None:
            throughput[timestamp] = data_rates[timestamp]["data_rate"]*(1-data_rates[timestamp]["frame_losses"]/length)
            length+=1
            prev_timestamp = timestamp
        else: 
            throughput[timestamp] = data_rates[timestamp]["data_rate"]
            prev_timestamp = timestamp
            length+=1

    throughput_file_for_visualiser = f"throughput_file_for_visualiser.txt"

############################################################################################################################
#----------------------------------------------------Store data regarding Throughput and rate gap in differen files---------
############################################################################################################################

    with open(throughput_file_for_visualiser, "w", encoding="utf-8") as throughput_file:
            for timestamp in throughput.keys():
                throughput_file.write(str(timestamp) +"::"+str(throughput[timestamp])+ '\n')

    rate_gap_file = f"rate_gap_file.txt"

    with open(rate_gap_file, "w", encoding="utf-8") as rate_gap:
            for timestamp in rate_gaps.keys():
                rate_gap.write(str(timestamp) +"::"+str(rate_gaps[timestamp])+ '\n')

    
    short_gi_true_file = f"short_gi_true_file.txt"

    with open(short_gi_true_file, "w", encoding="utf-8") as gi_true:
        for timestamp in short_gi_true.keys():
            gi_true.write(str(timestamp) +"::"+str(short_gi_true[timestamp])+ '\n')

    short_gi_false_file = f"short_gi_false_file.txt"

    with open(short_gi_false_file, "w", encoding="utf-8") as gi_false:
        for timestamp in short_gi_false.keys():
            gi_false.write(str(timestamp) +"::"+str(short_gi_false[timestamp])+ '\n')


############################################################################################################################
#----------------------------------------------------Calculate and print the throughput average----------------------------
############################################################################################################################

    frame_loss_rate = losses / total_frames
    avg_data_rate = sum(rates) / len(rates)
    av_throughput = avg_data_rate * (1 - frame_loss_rate)

    av_throughput_data = []

    av_throughput_data.append(total_frames)
    av_throughput_data.append(losses)
    av_throughput_data.append(frame_loss_rate)
    av_throughput_data.append(avg_data_rate)
    av_throughput_data.append(av_throughput)

    return throughput_file_for_visualiser, av_throughput_data , rate_gap_file, short_gi_true_file, short_gi_false_file