"""Strategy system module."""

from strategy.movimentsDecider import Attacker, Defender, Goalkeeper, Midfielder, MovimentsDecider
from statics.static_classes import world

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
        self.dynamicPossession = True
        self.step = 0.005

    def plan(self):
        """Toplevel planner which contains all the deciders of the system."""
        # TODO: VERIFICATION TEST FOR THE WORLD STATE

        # # Fuzzy
        # self.tactic = self.firstLvlDec.plan(self.world)
        # self.decider.setParams(world)
        # self.decider.setFormation(world)
        # self.targets = self.decider.updateTargets()
        
        self.decider.setFormation()
        print(self.decider.listEntity)
        
        if self.dynamicPossession:
            self.decider.updadeHost()
        else:
            self.decider.calcPath()

        self.targets = []
        for robot in world.robots:
            robot.discretize(self.step)
            self.targets.append(robot.nextStep())

    def get_targets(self):
        """Getter of each robot target planned."""
        return self.targets, self.spin
