import tornado.ioloop
import tornado.web
import pygame 
import os
from threading import Thread

__all__ = ['Arbaweb']

class FileHandler(tornado.web.StaticFileHandler):
    def parse_url_path(self, url_path):
        if not url_path or url_path.endswith('/'):
            url_path = url_path + 'gui.html'
        return url_path

class KeyHandler(tornado.web.RequestHandler):
    _KEY_LOOKUP = {
        "up_p1":   pygame.K_UP,
        "down_p1": pygame.K_DOWN,
        "right_p1":pygame.K_RIGHT,
        "left_p1": pygame.K_LEFT,
        'right_p2': pygame.K_f,
        'left_p2':  pygame.K_s,
        'up_p2':    pygame.K_e,
        'down_p2':  pygame.K_c
    }
    def get(self,*args, **kwargs):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header("Content-type", "text/html")
        (urlkey,type) = self.request.path.split("/")[2:4]
        if (urlkey in self._KEY_LOOKUP) and (type in ['up','down']): #Generate python game event
            if (type=='down'):
                type = pygame.KEYDOWN
            else:
                type = pygame.KEYUP
            pygame.event.post(pygame.event.Event(type,
                        key=self._KEY_LOOKUP[urlkey],
                        unicode=urlkey,
                        scancode=None))

class Arbaweb(Thread):
    def make_app(self):
        return tornado.web.Application([
            (r"/key/.*", KeyHandler),
            (r"/(.*)", tornado.web.StaticFileHandler, {'path': os.path.join(os.path.dirname(os.path.abspath(__file__)),"arbawebgui"),"default_filename": 'gui.html'}),
        ])
    
    def run_tornado(self):
        app = self.make_app()
        app.listen(8000)
        self.ioloop.start()
        print 'running tornado... listening on port 8080'
    
    def __init__(self, arbalet, server='127.0.0.1', port=80, rate=30, autorun=True):
        self.ioloop= tornado.ioloop.IOLoop.instance()
        thread = Thread(target=self.run_tornado)
        thread.daemon = True
        thread.start()
        
    def close(self):
        tornado.ioloop.IOLoop.current().stop()