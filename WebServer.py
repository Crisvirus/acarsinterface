from http.server import BaseHTTPRequestHandler, HTTPServer
from UDPHandler import UDPHandler
from os import curdir, sep
import json

def MakeHandlerClassFromArgv(planes_handler):
    class WebServer(BaseHTTPRequestHandler):

        def _set_response(self,content):
            self.send_response(200)
            self.send_header('Content-type', content)
            self.end_headers()

        def do_GET(self):
            if self.path=="/":
                f = open(curdir + sep + "HTML/index.html")
                self._set_response('text/html')
                self.wfile.write(bytearray(f.read(),"UTF-8"))
                f.close()
                return

            if self.path=="/last_24.html":
                f = open(curdir + sep + "HTML/last_24.html")
                self._set_response('text/html')
                self.wfile.write(bytearray(f.read(),"UTF-8"))
                f.close()
                return

            if self.path=="/all.html":
                f = open(curdir + sep + "HTML/all.html")
                self._set_response('text/html')
                self.wfile.write(bytearray(f.read(),"UTF-8"))
                f.close()
                return

            if self.path=="/planes_list_all":
                self._set_response('application/json')
                self.wfile.write(bytearray(json.dumps(planes_handler.get_list_of_planes()),"UTF-8"))
                return
            
            if self.path=="/planes_list_24":
                self._set_response('application/json')
                self.wfile.write(bytearray(json.dumps(planes_handler.get_list_of_planes_last_24()),"UTF-8"))
                return

            if self.path=="/planes_list_1":
                self._set_response('application/json')
                self.wfile.write(bytearray(json.dumps(planes_handler.get_list_of_planes_last_1()),"UTF-8"))
                return
            
            if '/all' in self.path:
                plane_name = self.path.split('/')[1]
                self._set_response('text/html')
                self.wfile.write(bytearray(planes_handler.getPlaneAllHTMLByName(plane_name),"UTF-8"))
                return
            else:
                plane_name = self.path[1:]
                self._set_response('text/html')
                self.wfile.write(bytearray(planes_handler.getPlaneLast8hHTMLByName(plane_name),"UTF-8"))
                return
                
    return WebServer