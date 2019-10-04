from states.state import State
from abc import ABC

from strategy.strategy import Strategy
from controllers.ssRegulator import ssRegulator
from controllers.ssRegulator import SpeedPair
from communication.radio_comm import RadioCommunicator
from statics import static_classes
from vision.mainVision.mainVision import MainVision
import time
from statics.static_classes import world
import numpy as np
import strategy.frameRenderer
import gui.mainWindow

class UiGameLoop(State):
    def __init__(self, thread):
        super().__init__(thread)
        self.__gameLoop = GameLoop(thread)

    def update(self):
        self.__gameLoop.update()
        strategy_frame = strategy.frameRenderer.strategyFrame((350,471), step=self.thread.strategySystem.step)
        gui.mainWindow.MainWindow().ui_frame("gameLoop").do_update_frame(strategy_frame)

class GameLoop(State):
    def __init__(self, thread):
        super().__init__(thread)

    def update(self):
        # Vision System
        t0 = time.time()
        self.thread.visionSystem.update()
        self.thread.strategySystem.plan()
        targets, spin = self.thread.strategySystem.get_targets()
        angle = np.arctan2(world.ball.pos[1]-world.robots[0].pos[1], world.ball.pos[0]-world.robots[0].pos[0])
        targets = [(world.ball.x,world.ball.y,angle),(0,0,0),(0,0,0)]
        velocities = self.thread.controlSystem.actuate(targets, static_classes.world)
        #print(velocities[0])


        if world.gameRunning is True:
            self.thread.radioComm.send(velocities)
        else:
            self.thread.radioComm.send([SpeedPair() for i in range(3)])
        #print(time.time()-t0)

#    def next_state(self):
#        pass

if __name__ == "__main__":
    pass
