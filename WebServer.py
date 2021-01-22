from http.server import BaseHTTPRequestHandler, HTTPServer
from UDPHandler import UDPHandler
from os import curdir, sep
import json
import cgi
import ssl
from bcrypt import hashpw, gensalt
from tinydb import TinyDB, Query
from http import cookies
import random
import math
from uuid import uuid4
from threading import Timer

def MakeHandlerClassFromArgv(planes_handler):
    user_passwd = {}
    passwdDB = TinyDB('./passwordDB/passwdDB.json')
    tokens = {}
    timers = {}
    for line in passwdDB.all():
        username = line['u']
        passwd = line['p']
        user_passwd[username] = passwd

    def delete_token(token):
        del tokens[token]
        timers[token].cancel()
        del timers[token]

    def token_is_valid(token):
        if token in tokens:
            return True
        else :
            return False

    def login(username,passwd):
        print("User = "+str(type(username))+" passwd = "+str(type(passwd))+"\n")
        if username not in user_passwd:
            print("User does not exist\n")
            return False
        else:
            hashed_passwd = user_passwd[username]
            if hashpw(passwd.encode('utf-8'),hashed_passwd.encode('utf-8')).decode('utf-8') == hashed_passwd:
                return True
            else:
                return False

    def create(username,passwd):
        if username in user_passwd:
            print("Already exists\n")
            return False
        else:
            hashed = hashpw(passwd.encode('utf-8'), gensalt())
            user_passwd[username] = hashed.decode('utf-8')
            entry = {}
            entry['u'] = str(username)
            entry['p'] = hashed.decode('utf-8')
            passwdDB.insert(entry)
            return True

    class WebServer(BaseHTTPRequestHandler):
        def _set_response(self,content):
            self.send_response(200)
            self.send_header('Content-type', content)
            self.end_headers()

        def serveWithCookie(self):
            token = ''
            if "Cookie" in self.headers:
                cookie_string = self.headers.get('Cookie')
                c = cookies.SimpleCookie()
                c.load(cookie_string)
                for key, morsel in c.items():
                    if key == 'token':
                        token = morsel.value
            else:
                print("No cookie for you\n")
            
            if token_is_valid(token):
                if self.path=="/map.html":
                    f = open(curdir + sep + "HTML/map.html")
                    self._set_response('text/html')
                    self.wfile.write(bytearray(f.read(),"UTF-8"))
                    f.close()
                    return

                if self.path=="/last_h.html":
                    f = open(curdir + sep + "HTML/last_h.html")
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

                if '/flight' in self.path:
                    tokens = self.path.split('/')
                    flight_no = tokens[2]
                    print(flight_no)
                    self._set_response('application/json')
                    self.wfile.write(bytearray(planes_handler.getLastMessageByFlightNumber(flight_no),"UTF-8"))
                    return

                if '/plane' in self.path:
                    tokens = self.path.split('/')
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
            
            else:
                print("Bad token\n")
                self.send_response(301)
                self.send_header('Location','/')
                self.end_headers()

        def do_GET(self):
            print(self.path)
            if self.path=="/":
                f = open(curdir + sep + "HTML/index.html")
                self._set_response('text/html')
                self.wfile.write(bytearray(f.read(),"UTF-8"))
                f.close()
                return

            if self.path=="/create.html":
                self.path="/create.html"
                mimetype='text/html'
                f = open(curdir + sep + "HTML/create.html") 
                self.send_response(200)
                self.send_header('Content-type',mimetype)
                self.end_headers()
                self.wfile.write(bytearray(f.read(),"UTF-8"))
                f.close()
                return

            self.serveWithCookie()

        def do_POST(self):
            #==========================Login===========================
            if self.path=="/login":
                print("Login\n")
                form = cgi.FieldStorage(
                    fp=self.rfile, 
                    headers=self.headers,
                    environ={'REQUEST_METHOD':'POST',
                            'CONTENT_TYPE':self.headers['Content-Type'],
                })
                username = form["uname"].value
                if login(username, form["psw"].value):
                    print("HERE")
                    f = open(curdir + sep + "HTML/last_h.html")
                    mimetype='text/html'
                    c = cookies.SimpleCookie()
                    rand_token = uuid4()
                    tokens[str(rand_token)] = form["uname"].value
                    c['token'] = str(rand_token)
                    c['token']['expires'] = 3*60*60
                    t = Timer(3*60*60, delete_token,args = [str(rand_token)])
                    t.start()
                    timers[str(rand_token)] = t
                    self.send_response(200)
                    self.send_header('Set-Cookie',str(c)[12:])
                    self.send_header('Content-type',mimetype)
                    self.end_headers()
                    self.wfile.write(bytearray(f.read(),"UTF-8"))
                    f.close()
                else:
                    self.send_response(301)
                    self.send_header('Location','/')
                    self.end_headers()

            if self.path=="/create":
                form = cgi.FieldStorage(
                    fp=self.rfile, 
                    headers=self.headers,
                    environ={'REQUEST_METHOD':'POST',
                            'CONTENT_TYPE':self.headers['Content-Type'],
                })
                if create(form["uname"].value, form["psw"].value):
                    self.send_response(301)
                    self.send_header('Location','/')
                    self.end_headers()
                else:
                    self.send_response(301)
                    self.send_header('Location','/')
                    self.end_headers()   
    return WebServer