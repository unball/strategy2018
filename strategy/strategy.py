"""Strategy system module."""

from strategy.movimentsDecider import Attacker, Defender, Goalkeeper, Midfielder, MovimentsDecider
from statics.static_classes import world
from vision.pixel2metric import meters2pixel

import cv2
import numpy as np

def error():
    """Print the standard error message for STRATEGY scope."""
    print("\nSTRATEGY ERROR:")


class Strategy(object):
    """Class docstring."""

    def __init__(self):
        """Init method."""
        self.coach = None
        self.tactic = None
        self.decider = MovimentsDecider()
        self.targets = []
        self.spin = [0,0,0]
        self.step = 0.005

    def plan(self):
        """Toplevel planner which contains all the deciders of the system."""
        # TODO: VERIFICATION TEST FOR THE WORLD STATE

        # # Fuzzy
        # self.tactic = self.firstLvlDec.plan(self.world)
        # self.decider.setParams(world)
        # self.decider.setFormation(world)
        # self.targets = self.decider.updateTargets()
        
        #self.decider.setFormation()
        
        #if self.dynamicPossession:
        self.decider.updadeHost()
#        else:
#            self.decider.calcPath()

        self.targets = []
        for robot in world.robots:
            robot.discretize(self.step)
            self.targets.append(robot.nextStep())
            
    def setTurningRadius(self, radius):
        self.decider.turning_radius = radius
    
    def composeUIframe(self):
        height, width = (520,640)
        frame = np.zeros((height,width,3), np.uint8)
        
        delta_p,_ = meters2pixel((self.decider.delta,0), (height,width))
        delta_n,_ = meters2pixel((-self.decider.delta,0), (height,width))
        cv2.line(frame, (delta_p,0), (delta_p,height), (150,150,150), 1)
        cv2.line(frame, (delta_n,0), (delta_n,height), (150,150,150), 1)
        
        for robot in world.robots:
            if robot.pos[0] is not None and robot.pos[1] is not None:
                position = meters2pixel(robot.pos, (height,width))
                rect = (position,(25,25),robot.th)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                cv2.drawContours(frame,[box],0,(0,255,0),2)
                if robot.entity is not None:
                    cv2.putText(frame, str(robot.entity)[0], (int(position[0])-10, int(position[1])+10), cv2.FONT_HERSHEY_TRIPLEX, 1, (255,255,255))
                
                robot.discretize(0.01)
                if len(robot.trajectory) > 0:
                    #print(np.array([meters2pixel(x, (height,width)) for x in robot.trajectory[0]]))
                    cv2.polylines(frame,[np.array([meters2pixel(x, (height,width)) for x in robot.trajectory[0]])],False,(255,255,255),1)
        
        bola = world.ball
        ballpos = meters2pixel(bola.pos, (height,width))
        cv2.circle(frame, ballpos, 5, (255,0,0), -1)
        
        return frame
    
    def get_targets(self):
        """Getter of each robot target planned."""
        return self.targets, self.spin
