from UDPHandler import UDPHandler
from WebServer import MakeHandlerClassFromArgv
from http.server import HTTPServer
from WaypointDB import WaypointDB
from WaypointDB import Waypoint
import _thread
waypointsDB = WaypointDB()
handler = UDPHandler(5555,waypointsDB)
try:
    waypointsDB.readFromFile()
    print(len(waypointsDB.waypoints))
    handler.init_socket()
    handler.read_from_file()
    handler.start()
    print("Ready to receive ACARS Messages\n")

    httpd = HTTPServer(('',8888),MakeHandlerClassFromArgv(handler))
    httpd.serve_forever()

except KeyboardInterrupt:
    print('^C received, shutting down the web server')
    handler.stop()
    handler.join()
