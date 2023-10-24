#!/usr/bin/env python3

import asyncio
import json
import logging
import websockets
import os
import sys


if os.name == "posix" and sys.platform == "linux":
    import shuttercontrol
    print("Real-Mode...")
else:
    import shuttercontroldummy as shuttercontrol
    print("Dummy-Mode...")

import time
import random
import threading

from http.server import HTTPServer, CGIHTTPRequestHandler
import socketserver

import abc


class SutterDeviceControl:

    def __init__(self, device):
        self.device = device
        self.isWindRainAuto = False
        self.isSunAuto = False
        self.windLevel = 100
        self.itsRaining = False
        self.sunLevel = 50
        self._observers = set()
        self._subject_state = None

    def get_windRainAutoState(self):
        return self.isWindRainAuto

    def get_sunAutoState(self):
        return self.isSunAuto

    def get_wind_level(self):
        return self.windLevel

    def get_rain_state(self):
        self.itsRaining = self.device.isItRaining()
        return self.itsRaining

    def get_sun_level(self):
        return self.sunLevel

    def do_shutter_sud_in(self):
        self.device.shutterSouthIn()
        print("do_shutter_sud_in")

    def do_shutter_sud_out(self):
        self.device.shutterSouthOut()
        print("do_shutter_sud_out")

    def do_shutter_west_up(self):
        self.device.shutterWestUp()
        print("do_shutter_west_up")

    def do_shutter_west_down(self):
        self.device.shutterWestDown()
        print("do_shutter_west_down")

    def set_wind_rain_auto(self):
        self.isWindRainAuto = not self.isWindRainAuto
        print("set_wind_rain_auto")
        print(self.isWindRainAuto)

    def set_sun_auto(self):
        self.isSunAuto = not self.isSunAuto
        print("set_sun_auto")
        print(self.isSunAuto)


    """
    Know its observers. Any number of Observer objects may observe a
    subject.
    Send a notification to its observers when its state changes.
    """
    def attach(self, observer):
        observer._subject = self
        self._observers.add(observer)

    def detach(self, observer):
        observer._subject = None
        self._observers.discard(observer)

    def _notify(self):
        for observer in self._observers:
            observer.update(self._subject_state)

    @property
    def subject_state(self):
        return self._subject_state

    @subject_state.setter
    def subject_state(self, arg):
        self._subject_state = arg
        self._notify()

#logging.basicConfig()

class Observer(metaclass=abc.ABCMeta):
    """
    Define an updating interface for objects that should be notified of
    changes in a subject.
    """

    def __init__(self):
        self._subject = None
        self._observer_state = None

    @abc.abstractmethod
    def update(self, arg):
        pass

class WsWebsocket(Observer):

    def __init__(self, deviceControl):
        self.deviceControl = deviceControl
        self.USERS = set()
        self.loop = None

    def update(self, arg):
        self._observer_state = arg
        print("Observer infomiert, message: " + str(arg))
        if str(arg) == "END":
            future = asyncio.run_coroutine_threadsafe(self.coro_func_end(), self.loop)
        else:
            future = asyncio.run_coroutine_threadsafe(self.coro_func(), self.loop)
        result = future.result()
        print(result)

    async def coro_func(self):
        await self.notify_wind_level()
        await self.rain_event()
        await self.notify_sun_level()
        return "DONE"

    async def coro_func_end(self):
        await self.notify_wind_level()
        await self.rain_event()
        await self.notify_sun_level()
        return "DONE"

    def set_event_loop(self, loop):
        self.loop = loop

    def users_event(self):
        return json.dumps({"type": "users", "count": len(self.USERS)})

    def windRainAuto_event(self):
        return json.dumps({"type": "windAuto", "value": self.deviceControl.get_windRainAutoState()})

    def sunAuto_event(self):
        return json.dumps({"type": "sunAuto", "value": self.deviceControl.get_sunAutoState()})

    def wind_level_event(self):
        return json.dumps({"type": "windLevel", "value": self.deviceControl.get_wind_level()})

    def rain_event(self):
        return json.dumps({"type": "rain", "value": self.deviceControl.get_rain_state()})

    def sun_level_event(self):
        return json.dumps({"type": "sunLevel", "value": self.deviceControl.get_sun_level()})

    async def notify_users(self):
        if self.USERS:  # asyncio.wait doesn't accept an empty list
            message = self.users_event()
            await asyncio.wait([user.send(message) for user in self.USERS])

    async def notify_windRainAuto(self):
        if self.USERS:  # asyncio.wait doesn't accept an empty list
            message = self.windRainAuto_event()
            await asyncio.wait([user.send(message) for user in self.USERS])

    async def notify_sunAuto(self):
        if self.USERS:  # asyncio.wait doesn't accept an empty list
            message = self.sunAuto_event()
            await asyncio.wait([user.send(message) for user in self.USERS])

    async def notify_wind_level(self):
        if self.USERS:  # asyncio.wait doesn't accept an empty list
            message = self.wind_level_event()
            await asyncio.wait([user.send(message) for user in self.USERS])

    async def notify_rain(self):
        if self.USERS:  # asyncio.wait doesn't accept an empty list
            message = self.rain_event()
            await asyncio.wait([user.send(message) for user in self.USERS])

    async def notify_sun_level(self):
        if self.USERS:  # asyncio.wait doesn't accept an empty list
            message = self.sun_level_event()
            await asyncio.wait([user.send(message) for user in self.USERS])

    async def register(self, websocket):
        self.USERS.add(websocket)
        await self.notify_users()
        await self.notify_windRainAuto()
        await self.notify_sunAuto()
        await self.notify_wind_level()
        await self.notify_rain()
        await self.notify_sun_level()

    async def unregister(self, websocket):
        self.USERS.remove(websocket)
        await self.notify_users()

    async def counter(self, websocket, path):
        # register(websocket) sends user_event() to websocket
        await self.register(websocket)
        try:
            #await websocket.send(self.state_event())
            async for message in websocket:
                data = json.loads(message)

                if data["action"] == "btnStoSudEin":
                    self.deviceControl.do_shutter_sud_in()
                    print("btnStoSudEin")

                elif data["action"] == "btnStoSudAus":
                    self.deviceControl.do_shutter_sud_out()
                    print("btnStoSudAus")

                elif data["action"] == "btnStoWestAuf":
                    self.deviceControl.do_shutter_west_up()
                    print("btnStoWestAuf")

                elif data["action"] == "btnStoWestAb":
                    self.deviceControl.do_shutter_west_down()
                    print("btnStoWestAb")

                elif data["action"] == "btnWindRegAuto":
                    self.deviceControl.set_wind_rain_auto()
                    print("btnWindRegAuto")
                    await self.notify_windRainAuto()

                elif data["action"] == "btnSunAuto":
                    self.deviceControl.set_sun_auto()
                    print("btnSunAuto")
                    await self.notify_sunAuto()

                else:
                    #logging.error("unsupported event: {}", data)
                    print("unsupported event: {}", data)
        finally:
            await self.unregister(websocket)


class HttpServerWorker:
    def run(self):
        '''Start a simple webserver serving path on port'''
        print("Start HttpServer ...")
        os.chdir('./wwwroot/')
        httpd = HTTPServer(('', 80), CGIHTTPRequestHandler)
        httpd.serve_forever()
        print("End HttpServer ...")


def main():
    # Start the server in a new thread
    httpServerWorker = HttpServerWorker()
    httpThread = threading.Thread(target=httpServerWorker.run)
    httpThread.setDaemon(True) # Set as a daemon so it will be killed once the main thread is dead.
    httpThread.start()

    control = shuttercontrol.Shuttercontrol()
    deviceControl = SutterDeviceControl(control)
    wsWebsocket = WsWebsocket(deviceControl)
    deviceControl.attach(wsWebsocket) # Observer verbinden

    print("Starte Websocket ...")
    start_server = websockets.serve(wsWebsocket.counter, "", 6789)
    asyncio.get_event_loop().run_until_complete(start_server)
    wsWebsocket.set_event_loop(asyncio.get_event_loop())
    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    main()
