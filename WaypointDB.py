import glob

class Waypoint:
    def __init__(self,name,lat,lon):
        self.name = name
        self.lat = lat
        self.lon = lon
class WaypointDB:
    def __init__(self):
        self.waypoints = {}

    def getWaypointByName(self,waypoint_name):
        if waypoint_name in self.waypoints:
            return self.waypoints[waypoint_name]
        else:
            return Waypoint("NULL",0,0)
            
    def readFromFile(self):
        path = './waypointsDB/CSVData/*'
        files = glob.glob(path)
        for file in files:
            csv_file = open(file, 'r')
            lines = csv_file.readlines()
            csv_file.close()
            for line in lines:
                tokens = line.split(',')
                w = Waypoint(str(tokens[0]),float(tokens[1]),float(tokens[2]))
                self.addWaypoint(w)
            
    
    def addWaypoint(self,waypoint):
        self.waypoints[waypoint.name] = waypoint