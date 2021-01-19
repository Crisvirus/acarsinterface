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
            
            if '/plane' in self.path:
                tokens = self.path.split('/')
                print(tokens)
                plane_name = tokens[2]
                if len(tokens) >= 4:
                    if tokens[3] == 'all':
                        self._set_response('text/html')
                        self.wfile.write(bytearray(planes_handler.getPlaneAllHTMLByName(plane_name),"UTF-8"))
                        return
                    
                    if tokens[3] == '8h':
                        self._set_response('text/html')
                        self.wfile.write(bytearray(planes_handler.getPlaneLast8hHTMLByName(plane_name),"UTF-8"))
                        return
                    
                    try:
                        if len(tokens) == 4:
                            msg_id = int(tokens[3])
                            self._set_response('text/html')
                            self.wfile.write(bytearray(planes_handler.getPlaneRouteById(plane_name,msg_id),"UTF-8"))
                            return
                        if len(tokens) == 5:
                            self._set_response('application/json')
                            msg_id = int(tokens[3])
                            self.wfile.write(bytearray(planes_handler.getPlaneRouteJSONById(plane_name,msg_id),"UTF-8"))
                            return
                    except:
                        print("Not ID "+ tokens[3])
                
    return WebServer