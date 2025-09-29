import pyshark

def parser_12(throughput_file):

    throughput_data_files = []

    data_frames = dict()
    lost_frames = dict()

    signal_strength = 0
    short_gi = None

    cap = pyshark.FileCapture(throughput_file, display_filter="wlan.fc.type_subtype == 40 || wlan.fc.type_subtype == 32" , use_json=True)

    for pkt in cap:
        timestamp = float(pkt.sniff_timestamp)
        data_rate = float(pkt.wlan_radio.data_rate)  if hasattr(pkt, "wlan_radio") and hasattr(pkt.wlan_radio, "data_rate") else 0
        signal_strength = pkt.wlan_radio.signal_dbm if hasattr(pkt.wlan_radio, 'signal_dbm') else 7
        short_gi = pkt.wlan_radio.short_gi if hasattr(pkt.wlan_radio, 'short_gi') else None
        if data_rate!=0 and signal_strength != 0 and short_gi is not None:
            data_frames[timestamp] = {"data_rate": data_rate, "RSSI": signal_strength, "short_gi": short_gi} 
        else: pass
    cap.close()

    throughput_data_file = f"throughput_file_0.txt"

    throughput_data_files.append(throughput_data_file)

    with open(throughput_data_file, "w", encoding="utf-8") as throughput_data:
            for timestamp in data_frames.keys():
                throughput_data.write(str(timestamp) +"::"+str(data_frames[timestamp]["data_rate"])+"::"+str(data_frames[timestamp]["RSSI"]) +"::"+str(data_frames[timestamp]["short_gi"])+ '\n')

    
    
    cap = pyshark.FileCapture(throughput_file, display_filter= "wlan.fc.retry == 1 && wlan.ta == 2C:F8:9B:DD:06:A0 && wlan.da == 00:20:A6:FC:B0:36", use_json=True)

    for pkt in cap:
        timestamp = float(pkt.sniff_timestamp)
        data_rate = float(pkt.wlan_radio.data_rate)  if hasattr(pkt, "wlan_radio") and hasattr(pkt.wlan_radio, "data_rate") else 0 
        lost_frames[timestamp] = data_rate
        
    cap.close()

    throughput_data_file = f"throughput_file_1.txt"

    throughput_data_files.append(throughput_data_file)

    with open(throughput_data_file, "w", encoding="utf-8") as throughput_data:
            for timestamp in lost_frames.keys():
                throughput_data.write(str(timestamp) +"::"+str(lost_frames[timestamp])+ '\n')


    return throughput_data_files