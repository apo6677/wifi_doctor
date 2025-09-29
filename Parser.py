import pyshark

def parse_packets(files):
    density_data_files = []

#########################################################################################################################################
#--------------------------------------------FOR EVERY FILE IN THE LIST FILES DO FILECAPTURE-------------------------------------------
#########################################################################################################################################
    for file in range(0,len(files)):
        packets = dict()

        cap = pyshark.FileCapture(files[file], 'wlan.fc.type_subtype == 8', use_json=True)

        packet_count = 0


        for packet in cap:
            if packet_count >= 100:
                break


            bssid = None
            transmitter_mac = None
            phy_type = None
            channel = None
            frequency = None
            signal_strength = None
            signal_noise_ratio = None

            timestamp = float(packet.sniff_timestamp) if hasattr(packet, 'sniff_timestamp') else None

            if hasattr(packet, 'wlan'):
                bssid = packet.wlan.bssid if hasattr(packet.wlan, 'bssid') else None
                transmitter_mac = packet.wlan.ta if hasattr(packet.wlan, 'ta') else None


            if hasattr(packet, 'wlan_radio'):                     
                ssid = packet.wlan.ssid if hasattr(packet.wlan, 'ssid') else None
                phy_type = packet.wlan_radio.phy if hasattr(packet.wlan_radio, 'phy') else None
                channel = packet.wlan_radio.channel if hasattr(packet.wlan_radio, 'channel') else None
                frequency = packet.wlan_radio.frequency if hasattr(packet.wlan_radio, 'frequency') else None
                signal_strength = packet.wlan_radio.signal_dbm if hasattr(packet.wlan_radio, 'signal_dbm') else None
                signal_noise_ratio = packet.wlan_radio.snr if hasattr(packet.wlan_radio, 'snr') else None

############################################################################################################################################
#-------------------------STORING DATA FOR FUTURE CALCULAITIONS IN DICTIONARY packets------------------------------------------------------
#-------------------------FOR EACH OF THE PCAP/PCAPNG FILES PRODUCE A FILE CONTAINING THE PARSED DATA NAMED density_0/density_1 etc--------
############################################################################################################################################
            
            packets[packet_count] = {
                "SSID": ssid,
                "BSSID": bssid,
                "Transmitter MAC": transmitter_mac,
                "PHY": phy_type,
                "Channel": channel,
                "Frequency": frequency,
                "Signal Strength": signal_strength,
                "SNR": signal_noise_ratio,
                "Timestamp": timestamp
            }

            packet_count += 1 

        cap.close()

        density_data_file = f"density_{file}.txt"

        density_data_files.append(density_data_file)

        with open(density_data_file, "w", encoding="utf-8") as density_data:
            for packet in packets.keys():
                density_data.write(str(packets[packet]["BSSID"]) +"::"+str(packets[packet]["Transmitter MAC"])+"::"+packets[packet]["PHY"]+"::"+packets[packet]["Channel"]+"::"+packets[packet]["Frequency"]+"::"+packets[packet]["Signal Strength"]+"::"+str(packets[packet]["SNR"])+"::"+str(packets[packet]["SSID"])+"::"+str(packets[packet]["Timestamp"]) + '\n')

    return density_data_files