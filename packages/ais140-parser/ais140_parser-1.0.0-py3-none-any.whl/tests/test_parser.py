import unittest
import pandas as pd
from ais140 import AIS140Parser, AIS140ParserError
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestAIS140Parser(unittest.TestCase):
    def setUp(self):
        self.parser = AIS140Parser()

    def test_parse_multiple_packets(self):
        packets = [
        "$Header,VendorId,VC4.40,OA,12,L,123456789012345,MH01AB1234,1,06042025,120100,28.6139,N,77.2090,E,45.0,303,12,194.0,0.00,1.38,airtel,0,0,0.0,3.7,0,C,24,404,10,93e,96d640b,186,ffff,137,174,ffff,84,0,0,0,0,0,0,000000,1111,002958,0.0,0.0,0.0,0,(domain.com:12345,115,1)*68",
        "$Header,VendorId,VC4.40,NR,12,L,123456789012345,MH01AB1235,1,06042025,120200,19.0760,N,72.8777,E,70.0,303,12,194.0,0.00,1.38,jio,0,0,0.0,3.6,0,C,24,404,10,93e,96d640b,187,ffff,140,174,ffff,88,0,0,0,0,0,0,000000,1111,002959,0.0,0.0,0.0,0,(domain.com:12345,115,1)*71",
        "$Header,VendorId,VC4.40,OA,12,L,123456789012345,MH01AB1236,1,06042025,115900,12.9716,N,77.5946,E,0.0,303,12,194.0,0.00,1.38,bsnl,0,0,0.0,3.8,0,C,24,404,10,93e,96d640b,188,ffff,144,174,ffff,80,0,0,0,0,0,0,000000,1111,002960,0.0,0.0,0.0,0,(domain.com:12345,115,1)*69",
        "$Header,VendorId,VC4.40,HL,12,L,123456789012345,MH01AB1234,1,06042025,120100,good,OK,23,12.5,30.2,4.0,60,engine_ok,battery_ok,GPS_OK,0,(domain.com:12345,115,1)*52",
        "$Header,VendorId,VC4.40,HL,12,L,123456789012345,MH01AB1235,1,06042025,120200,poor,BAD,25,11.0,31.0,4.1,58,engine_fail,battery_low,GPS_FAIL,1,(domain.com:12345,115,1)*56",
        "$Header,VendorId,VC4.40,LG,12,L,123456789012345,MH01AB1234,1,06042025,120100,event1,description1,user1,code1,info1*40",
        "$Header,VendorId,VC4.40,LG,12,L,123456789012345,MH01AB1235,1,06042025,120200,event2,description2,user2,code2,info2*42"
       ]

        valid_df, invalid_df = self.parser.parse_packets(packets)
        print(valid_df)
        print(invalid_df)
        # Check the valid DataFrame is correct
        self.assertEqual(len(valid_df), 2)  # Expecting two valid packets
        self.assertEqual(valid_df.iloc[0]['imei'], '123456789012345')
        
        self.assertEqual(valid_df.iloc[1]['imei'], '123456789012345')

        # Check the invalid DataFrame
        self.assertEqual(len(invalid_df), 1)
        self.assertIn("$Header,Invalid,VC4.40", invalid_df['raw_packet'].values)

if __name__ == "__main__":
    unittest.main()
