class StackManager:
    def __init__(self, agent):
        self.agent = agent
        self.base = None
        self.strats = []
    
    def setBaseStrategy(self, strat):
        self.base = strat
        self.agent.push(strat)
    
    def addStrat(self, strat, condition):
        if condition:
            self.strats.append(strat)
    
    def chooseStrat(self):
        if len(self.agent.stack) < 2 and len(self.strats) > 0:
            return self.strats[0]
        else:
            return None
    
    def updateStack(self):
        s = self.chooseStrat()
        if s is not None:
            self.agent.push(s)
        self.clearStrats()
    
    def clearStrats(self):
        self.strats.clear()



class Strat:
    def __init__(self, fun, condition):
        self.fun = fun
        self.condition = condition