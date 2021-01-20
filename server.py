from UDPHandler import UDPHandler
from WebServer import MakeHandlerClassFromArgv
from http.server import HTTPServer
from WaypointDB import WaypointDB
from WaypointDB import Waypoint
import _thread
import os
import ssl
waypointsDB = WaypointDB()
handler = UDPHandler(5555,waypointsDB)
try:
    # waypointsDB.readFromFile()
    # print(len(waypointsDB.waypoints))
    handler.init_socket()
    handler.read_from_file()
    handler.start()
    print("Ready to receive ACARS Messages\n")

    httpd = HTTPServer(('',8888),MakeHandlerClassFromArgv(handler))
    # Check if we have certificates
    if len(os.listdir('./certs')) != 0:
        print("Certificates found, using HTTPS")
        httpd.socket = ssl.wrap_socket (httpd.socket,
            keyfile='certs/privkey.pem',
            certfile='certs/fullchain.pem', server_side=True)
    else:
        print("No certificates, using HTTP")
    httpd.serve_forever()

except KeyboardInterrupt:
    print('^C received, shutting down the web server')
    handler.stop()
    handler.join()
