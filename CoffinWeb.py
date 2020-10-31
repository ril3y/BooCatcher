from random import randint
import random
from time import sleep,asctime
from quart import Quart, websocket, render_template_string, render_template, send_file, redirect, url_for, request
from colors import *
from quart import Response
import os
import functools

class CoffinWebServer(Quart):

    def __init__(self,name):
        print("[#] Starting Web Server")
        super(CoffinWebServer, self).__init__(name)
        self.route('/')(self.hello)
    
    async def hello(self):
        print('Index Requested')
        # anObj = dict(a=456, b='abc')
        # pub.sendMessage('rootTopic', arg1=55555, arg2=anObj)
        # pub.sendMessage('ws', message = dict(msg="Client connected") )
        images = os.listdir(os.path.join(self.static_folder, "images"))
        print('self.static_folder is ' + str(self.static_folder))
        return await render_template('index.html', title='Boo Catcher!',images=images, time=asctime()  )
        
    '''

    @app.route(self, "/video.mp4")
    async def auto_video():
        # Automatically respond to the request
        return await send_file("../video/motion.h264", conditional=True)


    @app.route(self, '/random_strip/<int:delay>', methods=['POST'])
    async def random_strip( delay):
        pass
        # pub.sendMessage('rootTopic', arg1=55555, arg2=anObj)



    @app.websocket(self, '/ws')
    async def ws():
        while True:
            data = await websocket.receive()
            await websocket.send(data)
            print("ws data " + data)

    @app.route(self, '/leds', methods=['GET', 'POST'])
    async def leds():
        print("LED Button pushed")
        anObj = dict(a=456, b='abc')
        # pub.sendMessage('LED', arg1=55555, arg2=anObj)
        return("nothing")

    @app.route(self, '/set_color', methods=['POST'])
    async def set_color():
        data = await request.get_data()

        print("set color Button pushed " + data)
        anObj = dict(a=456, b='abc')
        # pub.sendMessage('LED', arg1=55555, arg2=BLUE)
        return("nothing")

    '''


if __name__ == "__main__":
    CoffinWebServer(__name__).run(host= '0.0.0.0')
