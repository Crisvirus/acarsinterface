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

            # if self.path=="/scripts/treeview.js":
            #     f = open(curdir + sep + "scripts/treeview.js")
            #     self._set_response('application/javascript')
            #     self.wfile.write(bytearray(f.read(),"UTF-8"))
            #     f.close()
            #     return

            if self.path=="/planes_list_all":
                self._set_response('application/json')
                self.wfile.write(bytearray(json.dumps(planes_handler.get_list_of_planes()),"UTF-8"))
                return
            
            if self.path=="/planes_list_24":
                self._set_response('application/json')
                self.wfile.write(bytearray(json.dumps(planes_handler.get_list_of_planes_last_24()),"UTF-8"))
                return
            
            plane_name = self.path[1:]
            self._set_response('text/html')
            self.wfile.write(bytearray(planes_handler.getPlaneHTMLByName(plane_name),"UTF-8"))
            return
    return WebServer