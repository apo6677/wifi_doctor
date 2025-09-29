def Monitor(density_files):

    density_for_visualiser = []
    channel_density = []
    number = 0
    other_number = 0
##################################################################################################################################################
#-----------------READ ALL OF THE density_0/density_1 files etc TO READ THE PARSED DATA AND CALCULATE METRICS--------------------------------
##################################################################################################################################################
    for file in density_files:

        BSSIDs = dict()
        CHANNELs = dict()

        with open(file,"r") as density_file:
            for line in density_file:
                data = line.strip().split('::')

                bssid = data[0]
                channel = data[3]
                frequency = data[4]
                strength = int(data[5])
                timestamp = float(data[8])

                if bssid == "None" or timestamp =="None" or frequency == "None" or strength =="None" or bssid == "ff:ff:ff:ff:ff:ff" :
                     pass
                else:

                    if bssid in BSSIDs:
                        BSSIDs[bssid]["strength"]+=strength
                        BSSIDs[bssid]["counter"]+=1
                        BSSIDs[bssid]["timestamp"].append(timestamp)
                        BSSIDs[bssid]["strengths"].append(strength)
                    else:
                        BSSIDs[bssid] = {}
                        BSSIDs[bssid]["strength"]=strength
                        BSSIDs[bssid]["counter"]=1
                        BSSIDs[bssid]["freq"]=frequency
                        BSSIDs[bssid]["timestamp"] = [timestamp]
                        BSSIDs[bssid]["strengths"]=[strength]
                        BSSIDs[bssid]["channel"]=channel

                    if channel in CHANNELs:
                        CHANNELs[channel]["strength"]+=strength
                        CHANNELs[channel]["counter"]+=1
                    else:
                        CHANNELs[channel] = {}
                        CHANNELs[channel]["strength"]=strength
                        CHANNELs[channel]["counter"]=1
                        CHANNELs[channel]["freq"]=frequency


        average_signal_strength = 0

##################################################################################################################################################
#----------------------------------------FOR EACH OF THE DIFFERENT BSSIDs  CALCULATE THE RSSI AVERAGE PER BSSIDs ----------------------------------
# -------------------------------------AND STORE IT IN FILE NAMED density_visualiser_file_0/density_visualiser_file_1-----------------
#--------------------------------------STORE AS WELL A LIST OF ALL VALUES OF RSSI THAT A BSSID HAS AS WELL AS THE TIMESTAMPS OF ALL PACKETS
##################################################################################################################################################


        for bssid in BSSIDs:
            average_signal_strength = BSSIDs[bssid]["strength"]/BSSIDs[bssid]["counter"]

            density_visualiser_file = f"density_visualiser_{number}.txt"
            number+=1
            with open(density_visualiser_file, "w", encoding="utf-8") as density_data:
                    density_data.write(str(bssid) +"::"+str(average_signal_strength)+"::"+str(BSSIDs[bssid]["freq"])+"::"+str(BSSIDs[bssid]["timestamp"])+"::"+str(BSSIDs[bssid]["strengths"])+"::"+str(BSSIDs[bssid]["channel"])+ '\n')

            density_for_visualiser.append(density_visualiser_file)

##################################################################################################################################################
#---------------------------------------FOR EACH OF THE CHANNELS  CALCULATE THE RSSI AVERAGE PER CHANNEL ----------------------------------
# -------------------------------------AND STORE IT IN FILE NAMED density_channel_visualiser_0/density_channel_visualiser_1-----------------
##################################################################################################################################################

        for channel in CHANNELs:
            average_signal_strength = CHANNELs[channel]["strength"]/CHANNELs[channel]["counter"]

            density_visualiser_file = f"density_channel_visualiser_{other_number}.txt"
            other_number+=1

            with open(density_visualiser_file, "w", encoding="utf-8") as density_data:
                    density_data.write(str(channel) +"::"+str(average_signal_strength)+"::"+str(CHANNELs[channel]["freq"])+"::"+str(CHANNELs[channel]["counter"])+ '\n')

            channel_density.append(density_visualiser_file)


    return density_for_visualiser, channel_density
