from Plane import Plane
import threading
import socket
import json
import time
import glob
import re
from datetime import datetime
from Message import Message
from WaypointDB import Waypoint
from WaypointDB import WaypointDB
from IATAICAOConverter import IATAICAOConverter

class UDPHandler(threading.Thread):
    def __init__(self, port, waypointsDB,iataicao):
        threading.Thread.__init__(self)
        self.iataicao = iataicao
        self._stop_event = threading.Event()
        self.port = port
        self.planes = {}
        self.current_msg_id = 0
        self.logfile = open("./acarsdata/"+str(datetime.fromtimestamp(time.time()).strftime("%d-%m-%y-%H:%M:%S")) + ".out", "w")
        self.waypointsDB = waypointsDB
        self.lastMessageByFlightNo = {}

    def init_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('',self.port))
    
    def read_from_file(self):
        path = './acarsdata/*'
        files = glob.glob(path)
        for file in files:
            f = open(file,'r')
            lines = f.readlines()
            f.close()
            for line in lines:
                try:
                    json_data = json.loads(line)
                    self.process_data(json_data)
                except:
                    print("Not a JSON")
                    print(line)

    def checkRegex(self,sentance):
        if re.search(r"[A-Z]{5}\.[A-Z]{5}\.[A-Z]{5}", sentance):
            return "route"
        if re.search(r",[0-9]{5}\.[A-Z]{5},[0-9]{5}\.[A-Z]{5},[0-9]{5}\.[A-Z]{5}", sentance):
            return "route"
        if re.search(r",[0-9]{6},[0-9A-Z]{6}\.[A-Z]{5},[0-9]{6},[0-9A-Z]{6}\.[A-Z]{5}", sentance):
            return "route"
        if re.search(r"\.\.[A-Z]{5}\.\.[A-Z]{5}\.", sentance):
            return "route"
        if re.search(r"CLEARANCE", sentance):
            return "clearance"
        if re.search(r"CLRD TO", sentance):
            return "takeoff"
        return "text"

    def handleRouteMessage(self,plane,msg,sentance,text,):
        plane.addRoute(sentance)
        msg.mtype = 'route'
        msg.parseRoute(sentance)
        return plane, msg

    def handleClearanceMessage(self,plane,msg,sentance,text):
        msg.mtype = 'clearance'
        return plane, msg

    def handleTakeoffMessage(self,plane,msg,sentance,text):
        msg.mtype = 'takeoff'
        pattern = r"CLRD TO ([A-Z]{4}) OFF\r?\n? ([0-9A-Z]+) VIA ([0-9A-Z]+)"
        extracted = re.findall(pattern, text)
        if len(extracted) == 1:
            plane.destination_airport = extracted[0][0]
            msg.dest = extracted[0][0]
            msg.rwy = extracted[0][1]
            msg.takeoff_waypoint = extracted[0][2]
        
        return plane, msg

    def interpretText(self,plane,msg,text):
        sentances = text.split('\n')
        for sentance in sentances:
            stype = self.checkRegex(sentance)
            if stype == 'route':
                plane, msg = self.handleRouteMessage(plane,msg,sentance,text)
            if stype == 'clearance':
                plane, msg = self.handleClearanceMessage(plane,msg,sentance,text)
            if stype == 'takeoff':
                plane, msg = self.handleTakeoffMessage(plane,msg,sentance,text)
     
        return plane, msg
    def parseLibAcars(self,plane,json_content,msg):
        if 'arinc622' in json_content:
            msg.mtype = 'arinc622'
            msg.json_content = json_content
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
        
        return plane, msg
    
    def parseMessage(self,plane,json_data):
        timestamp = json_data['timestamp']
        text = json_data['text']
        mtype = 'text'
        json_content = ''
        msg = Message(self.current_msg_id,timestamp,text,mtype,json_content)
        self.current_msg_id += 1
        if json_data['assstat']=='skipped' or json_data['assstat']=='complete':
            if 'libacars' in json_data:
                msg.mtype = 'libacars'
                json_content = json_data['libacars']
                plane, msg = self.parseLibAcars(plane,json_content,msg)
                        
            else :
                plane, msg = self.interpretText(plane,msg,text)
            plane.add_message(msg)
        if plane.flight_no_icao != 'UNKNOWN':
            self.lastMessageByFlightNo[plane.flight_no_icao] = msg
        return plane
        
    def process_data(self,json_data):
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
                plane.add_flight_no(json_data['flight'],self.iataicao)
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
                plane = self.parseMessage(plane,json_data)
            
            self.planes[json_data['tail']] = plane
            
            
        else:
            return   
    def getLastMessageByFlightNumber(self,flight_no):
        if flight_no in self.lastMessageByFlightNo:
            return self.lastMessageByFlightNo[flight_no].getShortJSON()
        else:
            return '{"UNKNOWN":1}'

    def run(self):
        while not self._stop_event.is_set():
            # print(self._stop_event.is_set())
            data, address = self.sock.recvfrom(4096)
            try:
                json_data = json.loads(data)
                self.logfile.write(data.decode())
                self.process_data(json_data)
            except:
                print("Not a JSON")
                print(data)
        self.cleanup()

    def stop(self):
        self.logfile.close()
        self._stop_event.set()

    def cleanup(self):
        print("Thread is cleaning up!\n")
        self.sock.close()
        

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
    
    def getPlaneRouteJSONById(self, plane_name, msg_id):
        if plane_name in self.planes:
            return self.planes[plane_name].getRouteJSON(msg_id,self.waypointsDB)
        else:
            return "[]"
    
    def getPlaneRouteById(self, plane_name, msg_id):
        if plane_name in self.planes:
            return self.planes[plane_name].getRoute(msg_id,self.waypointsDB)
        else:
            return "<html>Plane Not Found<\\html>"
    
    def getPlaneLast8hHTMLByName(self,plane_name):
        if plane_name in self.planes:
            return self.planes[plane_name].getLast8HTML()
        else:
            return "<html>Plane Not Found<\\html>"