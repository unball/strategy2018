from threading import Thread, Event
import gui.frameRenderer
import cv2
import time
import vision.cameras
import statics.configFile
import gui.mainWindow
import states.main_menu
import states.game_loop
import states.config_strategy
import queue
from gui.guiMethod import guiMethod
from vision.mainVision.mainVision import MainVision
from strategy.strategy import Strategy
from controllers.ssRegulator import ssRegulator
from communication_system.radio_comm import RadioCommunicator

class GameThread():
    
    def __init__(self):
        # Private
        self._state = states.main_menu.MainMenu(self)
        self._events = queue.Queue()
        
        self._visionSystem = MainVision()
        self._strategySystem = Strategy()
        self._controlSystem = ssRegulator()
        self._radioComm = RadioCommunicator()
        
        
        self._loop_time = 0
        self._processing_time = 0
        
    def compute_average(self, v0, v, p=0.1):
        return v0*(1-p) + v*p
    
    @guiMethod
    def update_stats(self, processing_time, loop_time):
        self._loop_time = self.compute_average(self._loop_time, loop_time)
        self._processing_time = self.compute_average(self._processing_time, processing_time)
        gui.mainWindow.MainWindow().getObject("stats_label").set_text("Tempo de processamento: {:3.0f} ms\nTempo de loop: {:3.0f} ms".format(self._processing_time*1000, self._loop_time*1000))
    
    def set_state(self, stateName):
        if stateName == "mainMenu":
            self._state.request_state_change(states.main_menu.MainMenu(self))
        elif stateName == "gameLoop":
            self._state.request_state_change(states.main_menu.GameLoop(self))
        elif stateName == "configStrategy":
            self._state.request_state_change(states.config_strategy.ConfigStrategy(self))
        else:
            pass
    
    @property
    def visionSystem(self):
        return self._visionSystem
    
    @property
    def strategySystem(self):
        return self._strategySystem
    
    @property
    def controlSystem(self):
        return self._controlSystem
    
    @property
    def radioComm(self):
        return self._radioComm
    
    def stop(self):
        self._state.request_quit()
    
    def run(self):
        self.thread = Thread(target=self.__loop__)
        self.thread.start()
        
    def addEvent(self, method, *args):
        self._events.put({"method": method, "args": args})
    
    def runQueuedEvents(self):
        while not self._events.empty():
            try:
                event = self._events.get_nowait()
                event["method"](*event["args"])
            except:
                pass
        
    def __loop__(self):
        while True:
            loop_time = time.time()
            
            self.runQueuedEvents()
            self._state.update()
            if self._state.QuitRequested:
                break
            if self._state.StateChangeRequested:
                self._state = self._state.next_state()
                
            loop_time = time.time()-loop_time
            self.update_stats(0, loop_time)
            #time.sleep(1)
        
        
