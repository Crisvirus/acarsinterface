from datetime import datetime
import json
import jinja2
import re
import urllib.request
from WaypointDB import Waypoint
from WaypointDB import WaypointDB

class Message:
    def __init__(self,id,timestamp,text,mtype,json_content):
        self.timestamp = timestamp
        self.text = text
        self.json_content = json_content
        self.mtype = mtype
        self.id = id
        self.rwy = 'UNKNOWN'
        self.takeoff_waypoint = 'UNKNOWN'
        self.dest = 'UNKNOWN'
        self.link = "https://www.lvnl.nl/eaip/2021-01-14-AIRAC/html/eAIP/EH-AD-2.EHAM-en-GB.html#eham-ad-2.24"
        self.is_Schipol = True
        self.route = ['UNKNOWN']

    def parseRoute(self,route_text):
        if re.search(r"[A-Z]{5}\.[A-Z]{5}\.[A-Z]{5}", route_text):
            self.route = re.findall(r"([0-9A-Z]{5})\.",route_text)
        if re.search(r",[0-9]{5}\.[A-Z]{5},[0-9]{5}\.[A-Z]{5},[0-9]{5}\.[A-Z]{5}", route_text):
            self.route = re.findall(r",[0-9]{5}\.([A-Z]{5})",route_text)

    def getRouteHTML(self, waypointsDB):
        return_string = ''
        for waypoint_name in self.route:
            waypoint = waypointsDB.getWaypointByName(waypoint_name)
            if waypoint.name != 'NULL':
                return_string += waypoint.name +' '+ str(waypoint.lat) +' lat   '+ str(waypoint.lon) +' lon<br>'
        return return_string

    def createLink(self):
        self.link = "https://www.lvnl.nl/eaip/2021-01-14-AIRAC/graphics/eAIP/EH-AD-2.EHAM-SID-"+self.rwy+".pdf"
        if self.rwy == '24':
            if 'VALK' in self.takeoff_waypoint or 'BERG' in self.takeoff_waypoint:
                self.link = "https://www.lvnl.nl/eaip/2021-01-14-AIRAC/graphics/eAIP/EH-AD-2.EHAM-SID-"+self.rwy+"-2.pdf"
            else:
                self.link = "https://www.lvnl.nl/eaip/2021-01-14-AIRAC/graphics/eAIP/EH-AD-2.EHAM-SID-"+self.rwy+"-1.pdf"
        if self.rwy == '36L':
            self.link = "https://www.lvnl.nl/eaip/2021-01-14-AIRAC/graphics/eAIP/EH-AD-2.EHAM-SID-"+self.rwy+"-1.pdf"
        if self.rwy == '06':
            self.link = "https://www.lvnl.nl/eaip/2021-01-14-AIRAC/graphics/eAIP/EH-AD-2.EHAM-SID-"+self.rwy+"-1.pdf"

        return self.link

    
    def getHTMLMessage(self):
        templateLoader = jinja2.FileSystemLoader(searchpath="./templates")
        templateEnv = jinja2.Environment(loader=templateLoader)
        if self.mtype == "text":
            template = templateEnv.get_template('text_message_template.html')
            return template.render(msg = self)
        if self.mtype == "arinc622" or self.mtype == "libacars":
            template = templateEnv.get_template('arinc622_message_template.html')
            return template.render(msg = self)

        if self.mtype == 'route':
            template = templateEnv.get_template('route_message_template.html')
            return template.render(msg = self)
        
        if self.mtype == 'clearance':
            template = templateEnv.get_template('clearance_message_template.html')
            return template.render(msg = self)

        if self.mtype == 'takeoff':
            template = templateEnv.get_template('takeoff_message_template.html')
            return template.render(msg = self)

        template = templateEnv.get_template('text_message_template.html')
        return template.render(msg = self)
        

    def get_text(self):
        return self.text

    def getJson(self):
        return json.dumps(self.json_content)

    def getType(self):
        return self.mtype

    def get_timestamp(self):
        return datetime.fromtimestamp(self.timestamp).strftime("%d-%m-%y %H:%M:%S")