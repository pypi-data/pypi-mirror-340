import re
import pandas as pd

class AIS140ParserError(Exception):
    """Custom exception for AIS-140 parsing errors."""
    pass

class AIS140Parser:
    def __init__(self):
        # Default headers for different packet types
        self.tracking_headers = [
            'Header','vendor_id', 'firmware_version', 'Packet type', 'gps_fix', 'vehicle_mode','imei','vehicle_registration_number',
            'alert_id', 'gps_signal_strength',  
            'packet_status', 'date', 'time', 'latitude', 'lat_direction', 'longitude',
            'long_direction', 'speed', 'heading', 'satellites', 'altitude', 'pdop',
            'hdop', 'network_operator', 'ignition', 'main_power_status',
            'battery_voltage', 'emergency_status', 'tamper_alert', 'frame_number',
            'mcc', 'mnc', 'lac', 'cell_id', 'signal_strength'
        ]
        self.health_headers = [
            'Header','vendor_id', 'firmware_version', 'imei', 'vehicle_registration_number',
            'date', 'time', 'internal_battery_voltage', 'external_battery_voltage', 'temperature',
            'charging_status', 'last_gps_fix', 'memory_percentage', 'gsm_signal_strength'
        ]
        self.logging_headers = [
            'Header','vendor_id', 'firmware_version', 'imei', 'vehicle_registration_number',
            'log_timestamp', 'log_data'
        ]

    def parse_packets(self, packets):
        """Parses multiple AIS-140 packets and categorizes them into tracking, health, logging, and unknown."""
        tracking_packets = []
        health_packets = []
        logging_packets = []
        unknown_packets = []

        for packet in packets:
            try:
                parsed_data, packet_type = self.parse_packet(packet)
                if packet_type == 'tracking':
                    tracking_packets.append(parsed_data)
                elif packet_type == 'health':
                    health_packets.append(parsed_data)
                elif packet_type == 'logging':
                    logging_packets.append(parsed_data)
                else:
                    unknown_packets.append(packet)
            except AIS140ParserError:
                unknown_packets.append(packet)

        # Create DataFrames for each category
        tracking_df = pd.DataFrame(tracking_packets, columns=self.tracking_headers)
        health_df = pd.DataFrame(health_packets, columns=self.health_headers)
        logging_df = pd.DataFrame(logging_packets, columns=self.logging_headers)
        unknown_df = pd.DataFrame(unknown_packets, columns=['raw_packet'])

        return tracking_df, health_df, logging_df, unknown_df

    def calculate_checksum(self, data):
        """Calculates the checksum for the given data (before the '*' character)."""
        checksum = 0
        for char in data:
            checksum ^= ord(char)
        return f"{checksum:02X}"
    
    def parse_packet(self, raw_message):
        """Parses a single AIS-140 packet based on packet type and calls the appropriate method."""
        
        if not raw_message.startswith('$'):
            raise AIS140ParserError("Invalid AIS-140 message format")
        
         
        
        try:
            message_without_checksum = raw_message.split('*')[0]
            parts = message_without_checksum.split(',')
        except Exception:
            raise AIS140ParserError("Error in parsing message fields")

        packet_type = parts[3]  # Packet type is in the 4th field
        if packet_type == 'OA' or packet_type == 'NR':  # Tracking packets
            return self._parse_tracking_packet(parts), 'tracking'
        elif packet_type == 'HL':  # Health packets
            return self._parse_health_packet(parts), 'health'
        elif packet_type == 'LG':  # Logging packets
            return self._parse_logging_packet(parts), 'logging'
        else:
            raise AIS140ParserError(f"Unknown packet type: {packet_type}")

        
    def _parse_tracking_packet(self, parts):
        """Parses a tracking packet and adds unknown headers for extra fields."""
        # Adjust the number of headers dynamically if there are extra fields
        if len(parts) > len(self.tracking_headers):
            extra_fields_count = len(parts) - len(self.tracking_headers)
            unknown_headers = [f'unknown{i + 1}' for i in range(extra_fields_count)]
            adjusted_headers = self.tracking_headers + unknown_headers
            self.tracking_headers = adjusted_headers
        else:
            adjusted_headers = self.tracking_headers
        
        # If the packet has fewer fields than expected, raise an error
        if len(parts) < len(self.tracking_headers):
            raise AIS140ParserError("Invalid tracking packet format")
        # Return all fields, including extra fields, with the adjusted headers
        return dict(zip(adjusted_headers, parts))

    def _parse_health_packet(self, parts):
        """Parses a health packet and adds unknown headers for extra fields."""
        if len(parts) > len(self.health_headers):
            extra_fields_count = len(parts) - len(self.health_headers)
            unknown_headers = [f'unknown{i + 1}' for i in range(extra_fields_count)]
            adjusted_headers = self.health_headers + unknown_headers
            self.health_headers = adjusted_headers 
        else:
            adjusted_headers = self.health_headers

        if len(parts) < len(self.health_headers):
            raise AIS140ParserError("Invalid health packet format")

        return dict(zip(adjusted_headers, parts))

    def _parse_logging_packet(self, parts):
        """Parses a logging packet and adds unknown headers for extra fields."""
        if len(parts) > len(self.logging_headers):
            extra_fields_count = len(parts) - len(self.logging_headers)
            unknown_headers = [f'unknown{i + 1}' for i in range(extra_fields_count)]
            adjusted_headers = self.logging_headers + unknown_headers
            self.logging_headers = adjusted_headers
        else:
            adjusted_headers = self.logging_headers

        if len(parts) < len(self.logging_headers):
            raise AIS140ParserError("Invalid logging packet format")

        return dict(zip(adjusted_headers, parts))
