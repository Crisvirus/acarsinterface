import jinja2
from datetime import datetime
from Message import Message
import time
class Plane:
    def __init__(self, registration_no, timestamp):
        self.registration_no = registration_no
        self.first_seen = timestamp
        self.last_seen = timestamp
        self.flight_no = 'Unknown'
        self.departure_airport = 'Unknown'
        self.destination_airport = 'Unknown'
        self.eta = 'Unknown'
        self.gout = 'Unknown'
        self.gin = 'Unknown'
        self.won = 'Unknown'
        self.woff = 'Unknown'
        self.messages = []
        self.route = ''
        self.has_extra = 'No'
        self.lat = 'Unknown'
        self.lon = 'Unknown'
        self.alt = 'Unknown'
        self.speed = 'Unknown'
        self.heading = 'Unknown'
        self.m_wind_speed = 'Unknown'
        self.m_direction = 'Unknown'
        self.m_temp = 'Unknown'
        self.has_location = 'No'
        self.has_meteo = 'No'

    def update_last_seen(self, last_seen):
        self.last_seen = last_seen

    def add_flight_no(self, flight_no):
        self.flight_no = flight_no

    def add_departure_airport(self, departure_airport):
        self.departure_airport = departure_airport

    def add_destination_airport(self, destination_airport):
        self.destination_airport = destination_airport

    def add_eta(self, eta):
        self.eta = eta

    def add_gin(self, gin):
        self.has_extra = 'Yes'
        self.gin = gin

    def add_gout(self, gout):
        self.has_extra = 'Yes'
        self.gout = gout

    def add_won(self, won):
        self.has_extra = 'Yes'
        self.won = won

    def add_woff(self, woff):
        self.has_extra = 'Yes'
        self.woff = woff

    def add_message(self, message):
        self.messages.append(message)

    def get_brief(self):
        output = {}
        output['key'] = self.registration_no
        output['timestamp'] = datetime.fromtimestamp(self.last_seen).strftime("%d-%m-%y %H:%M:%S")
        output['msgno'] = len(self.messages)
        output['extra'] = self.has_extra
        output['location'] = self.has_location
        output['meteo'] = self.has_meteo
        return output

    def getLast8HTML(self):
        first_dt = datetime.fromtimestamp(self.first_seen).strftime("%d-%m-%y %H:%M:%S")
        last_dt = datetime.fromtimestamp(self.last_seen).strftime("%d-%m-%y %H:%M:%S")
        templateLoader = jinja2.FileSystemLoader(searchpath="./templates")
        templateEnv = jinja2.Environment(loader=templateLoader)
        template = templateEnv.get_template('planeinfo.html')
        last8hmessages = []
        for msg in self.messages:
            if msg.timestamp > time.time() - 8*60*60:
                last8hmessages.append(msg)
        
        return template.render(gin = self.gin, 
                                gout = self.gout, 
                                won = self.won, 
                                woff = self.woff, 
                                registration_no=self.registration_no, 
                                flight_no = self.flight_no, 
                                departure_airport = self.departure_airport, 
                                destination_airport = self.destination_airport, 
                                first_seen = str(first_dt), 
                                last_seen = str(last_dt), 
                                msg_no = str(len(self.messages)), 
                                messages = last8hmessages,
                                msg_last_8 = len(last8hmessages),
                                lat = str(self.lat),
                                lon = str(self.lon),
                                alt = str(self.alt),
                                speed = str(self.speed),
                                hdg = str(self.heading),
                                m_speed = str(self.m_wind_speed),
                                m_dir = str(self.m_direction),
                                m_temp = str(self.m_temp))

    def getHTML(self):
        first_dt = datetime.fromtimestamp(self.first_seen).strftime("%d-%m-%y %H:%M:%S")
        last_dt = datetime.fromtimestamp(self.last_seen).strftime("%d-%m-%y %H:%M:%S")
        templateLoader = jinja2.FileSystemLoader(searchpath="./templates")
        templateEnv = jinja2.Environment(loader=templateLoader)
        template = templateEnv.get_template('planeinfo_all.html')
        return template.render(gin = self.gin, 
                                gout = self.gout, 
                                won = self.won, 
                                woff = self.woff, 
                                registration_no=self.registration_no, 
                                flight_no = self.flight_no, 
                                departure_airport = self.departure_airport, 
                                destination_airport = self.destination_airport, 
                                first_seen = str(first_dt), 
                                last_seen = str(last_dt), 
                                msg_no = str(len(self.messages)), 
                                messages = self.messages,
                                lat = str(self.lat),
                                lon = str(self.lon),
                                alt = str(self.alt),
                                speed = str(self.speed),
                                hdg = str(self.heading),
                                m_speed = str(self.m_wind_speed),
                                m_dir = str(self.m_direction),
                                m_temp = str(self.m_temp))
