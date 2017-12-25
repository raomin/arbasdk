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
        "up": pygame.K_UP,
        "down": pygame.K_DOWN,
        "right": pygame.K_RIGHT,
        "left": pygame.K_LEFT
    }
    def get(self,*args, **kwargs):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header("Content-type", "text/html")
        print(self.request.path)
        (urlkey,type) = self.request.path.split("/")[2:4]
        if (urlkey in self._KEY_LOOKUP) and (type in ['up','down']):
            if (type=='down'):
                type = pygame.KEYDOWN
            else:
                type = pygame.KEYUP
            pygame.event.post(pygame.event.Event(type,
                        key=self._KEY_LOOKUP[urlkey],
                        unicode=urlkey, 
                        scancode=None))
            print("sent key %s type %s" % (urlkey,type))



class Arbaweb(Thread):
    def make_app(self):
        print("launching webserver, root fs: "+ os.getcwd())

        return tornado.web.Application([
            (r"/key/.*", KeyHandler),
            (r"/(.*)", tornado.web.StaticFileHandler, {'path': os.path.join(os.getcwd(),"arbawebgui"),"default_filename": 'gui.html'}),
        ])
    def run_tornado(self):
        print 'running tornado...'
        app = self.make_app()
        app.listen(8000)
        self.ioloop.start()
    def __init__(self, arbalet, server='127.0.0.1', port=80, rate=30, autorun=True):
        self.ioloop= tornado.ioloop.IOLoop.instance()
        
        thread = Thread(target=self.run_tornado)
        thread.daemon = True
        thread.start()
        #self.daemon=True
        #self.start()
        
    def close(self):
        tornado.ioloop.IOLoop.current().stop()
