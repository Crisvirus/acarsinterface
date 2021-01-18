from Plane import Plane
import threading
import socket
import json
import time
import glob
from Message import Message
class UDPHandler(threading.Thread):
    def __init__(self, port):
        threading.Thread.__init__(self)
        self.port = port
        self.planes = {}

    def init_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('',self.port))
    
    def read_from_file(self):
        path = './acarsdata/*'
        files = glob.glob(path)
        for file in files:
            f = open(file,'r')
            f.readline()
            lines = f.readlines()
            f.close()
            for line in lines:
                self.process_data(line)

    def process_data(self,data):
        json_data = json.loads(data)
        if 'tail' in json_data:
            if json_data['tail'] == '':
                return
            plane = ''
            if json_data['tail'] in self.planes:
                plane = self.planes[json_data['tail']]
            else:
                plane = Plane(json_data['tail'],json_data['timestamp'])
            
            plane.update_last_seen(json_data['timestamp'])
            if 'flight' in json_data:
                plane.add_flight_no(json_data['flight'])
            if 'depa' in json_data:
                plane.add_departure_airport(json_data['depa'])
            if 'dsta' in json_data:
                plane.add_destination_airport(json_data['dsta'])
            if 'gin' in json_data:
                plane.add_gin(json_data['gin'])
            if 'gout' in json_data:
                plane.add_out(json_data['out'])
            if 'won' in json_data:
                plane.add_won(json_data['won'])
            if 'woff' in json_data:
                plane.add_woff(json_data['woff'])
            if 'text' in json_data:
                timestamp = json_data['timestamp']
                text = json_data['text']
                mtype = 'text'
                json_content = ''
                if 'libacars' in json_data:
                    mtype = 'libacars'
                    json_content = json_data['libacars']
                    if 'arinc622' in json_content:
                        if json_content["arinc622"]["msg_type"] == 'adsc_msg':
                            adsc_msg = json_content["arinc622"]["adsc"]
                            tags = adsc_msg['tags']
                            for tag in tags:
                                if 'basic_report' in tag:
                                    basic = tag['basic_report']
                                    plane.lat = basic['lat']
                                    plane.lon = basic['lon']
                                    plane.alt = int(float(basic['alt'])*0.3048)
                                    plane.has_location = "Yes"

                                if 'earth_ref_data' in tag:
                                    basic = tag['earth_ref_data']
                                    plane.speed = int(float(basic['gnd_spd_kts'])*1.852)
                                    plane.heading = basic['true_trk_deg']
                                    plane.has_location = "Yes"

                                if 'meteo_data' in tag:
                                    basic = tag['meteo_data']
                                    plane.m_wind_speed = int(float(basic['wind_spd_kts'])*1.852)
                                    plane.m_direction = basic['wind_dir_true_deg']
                                    plane.m_temp = basic['temp_c']
                                    plane.has_meteo = "Yes"
                                

                if json_data['assstat']=='skipped' or json_data['assstat']=='complete':
                    msg = Message(timestamp,text,mtype,json_content)
                    plane.add_message(msg)

            self.planes[json_data['tail']] = plane
            # print(plane.get_brief())
            
        else:
            return   
        
    def run(self):
        while True:
            data, address = self.sock.recvfrom(4096) 
            self.process_data(data)

    def get_list_of_planes(self):
        return_list = []
        for key in self.planes:
            return_list.append(self.planes[key].get_brief())
        return return_list
    
    def get_list_of_planes_last_24(self):
        return_list = []
        for key in self.planes:
            timestamp = self.planes[key].last_seen
            if timestamp > time.time() - 24*60*60:
                return_list.append(self.planes[key].get_brief())
        return return_list

    def get_list_of_planes_last_1(self):
        return_list = []
        for key in self.planes:
            timestamp = self.planes[key].last_seen
            if timestamp > time.time() - 1*60*60:
                return_list.append(self.planes[key].get_brief())
        return return_list
        
    def getPlaneAllHTMLByName(self,plane_name):
        if plane_name in self.planes:
            return self.planes[plane_name].getHTML()
        else:
            return "<html>Plane Not Found<\\html>"

    def getPlaneLast8hHTMLByName(self,plane_name):
        if plane_name in self.planes:
            return self.planes[plane_name].getLast8HTML()
        else:
            return "<html>Plane Not Found<\\html>"