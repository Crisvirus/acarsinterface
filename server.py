from UDPHandler import UDPHandler
from WebServer import MakeHandlerClassFromArgv
from http.server import HTTPServer
import _thread
handler = UDPHandler(5555)

try:
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
