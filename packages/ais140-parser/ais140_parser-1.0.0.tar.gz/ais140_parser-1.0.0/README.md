# AIS-140 Protocol Parser

This is a Python library that parses AIS-140 protocol messages used for tracking public and commercial vehicles. The parser extracts latitude, longitude, speed, and GPS status from raw messages, and validates checksums if present.

## Installation
Alternatively, you can install with pip:
    pip install ais140-parser

Basic Usage

To install the library, clone the repository and install the dependencies:

```bash
git clone https://github.com/your-username/ais140-parser.git
cd ais140-parser
pip install .


Alternatively, you can install with pip:
    pip install ais140-parser

Basic Usage
The simplest way to use  ais140-parser library for parsing your data and analyze it.
    from ais140.parser import AIS140Parser
    from ais140.kpi import AIS140KPI

    def main():
        # Create an instance of the parser
        parser = AIS140Parser()

        # Define a list of AIS-140 packets (could also be read from a file), below are sample data. 
        packets = [
            "$PKT,VID1234,FW1.2.3,NR,1,N,123456789012345,KA01AB1234,100,22,0,130425,143015,12.971598,N,77.594566,E,48.5,270.0,10,920.0,1.8,0.9,Airtel,1,1,12.6,0,0,000123,404,45,5678,123456,25",
            "$LGN,istartracker,andy123456,867458047932167,V100,AIS140,22.678880,N,114.047001,E", 
            "$HBT,istartracker,V100,HP,867458047932167,94%,20%,0.00%,20,30,0000,00,0.0,0.0*",
            "$EPB,istartracker,EMR,867458047932167,NM,02012020062650,A,22.678373,N,114.046198,E,80,1,1863,G,car123456,,473A0F35 "
        ]

        # Parse the packets into tracking, health, logging, and unknown dataframes
        tracking_df, health_df, logging_df, unknown_df = parser.parse_packets(packets)

        # Output the valid tracking packets
        print("Tracking Packets:")
        print(tracking_df)

        # Output the health packets
        print("\nHealth Packets:")
        print(health_df)

        # Output the logging packets
        print("\nLogging Packets:")
        print(logging_df)

        # Output the unknown packets
        print("\nUnknown Packets:")
        print(unknown_df)

        #KPI Analysis
        tracking_df, *_ = parser.parse_packets(packets)
        
        kpi = AIS140KPI(tracking_df)

        print("Total Devices:", kpi.total_devices())
        print("Online Devices:", kpi.online_devices())
        print("Offline Devices:", kpi.offline_devices())
        print("Average Speed:", kpi.average_speed())
        print("Over-speeding Devices:", kpi.overspeeding_devices())
        print("Current Locations:\n", kpi.current_locations())


    if __name__ == "__main__":
        main()

#Output should be like below Total Devices: 1
    '''Online Devices: 0
    Offline Devices: 1
    Average Speed: 48.5
    Over-speeding Devices: 0
    Current Locations:
                imei   latitude  longitude
    0  123456789012345  12.971598  77.594566'''