"""
    Arbalet - ARduino-BAsed LEd Table

    Arbalet client
    Client for controlling Arbalet over the network

    Copyright 2015 Yoan Mollard - Arbalet project - http://github.com/arbalet-project
    License: GPL version 3 http://www.gnu.org/licenses/gpl.html
"""

import BaseHTTPServer
import pygame 
from threading import Thread
from . rate import Rate

__all__ = ['Arbaweb']


class MyServer(BaseHTTPServer.HTTPServer):
    def run(self, variable):
        try:
            self.RequestHandlerClass.arbalet = variable 
            BaseHTTPServer.HTTPServer.serve_forever(self)
            self.serve_forever(self)
        except KeyboardInterrupt:
            pass
        finally:
            # Clean-up server (close socket, etc.)
            self.socket.close()
            self.server_close()



class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    arbalet=None
    _KEY_LOOKUP = {
        "up": pygame.K_UP,
        "down": pygame.K_DOWN,
        "right": pygame.K_RIGHT,
        "left": pygame.K_LEFT
        }
    
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/htm")
        s.send_header('Access-Control-Allow-Origin', '*')
        s.end_headers()
    def do_GET(s):

        """Respond to a GET request."""
        s.send_response(200)
        s.send_header('Access-Control-Allow-Origin', '*')
        s.send_header("Content-type", "text/html")
        s.end_headers()
        # If someone went to "http://something.somewhere.net/foo/bar/",
        # then s.path equals "/foo/bar/".
        if (s.path == "/"):
            f=open(r'C:\Users\bourgur\source\repos\Arbalet\arbwebgui\gui.html',"r")
            s.wfile.write(f.read())
            f.close()

        if (s.path == "/dist/nipple.js"):
            f=open(r'C:\Users\bourgur\source\repos\Arbalet\arbwebgui\dist\nipple.js',"r")
            s.wfile.write(f.read())
            f.close()

        if (s.path.startswith("/key/")):
            (urlkey,type) = s.path.split('/')[2:4]
            if (urlkey in s._KEY_LOOKUP) and (type in ['up','down']):
                if (type=='down'):
                    type = pygame.KEYDOWN
                else:
                    type = pygame.KEYUP
                with s.arbalet.sdl_lock:
                    pygame.event.post(pygame.event.Event(type,
                                key=s._KEY_LOOKUP[urlkey],
                                unicode=urlkey, 
                                scancode=None))
                    print("sent key %s type %s" % (urlkey,type))

class Arbaweb(Thread):
    def __init__(self, arbalet, server='127.0.0.1', port=80, rate=30, autorun=True):
        Thread.__init__(self)
        self.autorun = True
        self.server = server
        self.port = port

        self.running = True
        self.rate = Rate(rate)
        self.arbalet = arbalet



        # Network-related attributes
        if autorun:
            self.start()

    def close(self):
        self.running = False

    def run(self):

        self.httpd = MyServer((self.server, self.port), MyHandler)
        thread = Thread(None, self.httpd.run,args=(self.arbalet,))
        thread.start()
        #self.httpd.serve_forever(self.arbalet)
        while self.running:
            pass


            #self.send_model()
            #self.receive_touch()
            #self.rate.sleep()
        self.httpd.socket.close()
        self.httpd.server_close()


