from model import Model
from view import View
from rep import Rep

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
   
    def run(self):
       ##file = self.view.selectFile()
       self.model.debugSetupWindow()
       barPoints = self.view.debugSelectPoints(self.model.video)
       reps, center = self.model.createTracker(barPoints)
       self.view.showClip(self.model.tracker, center, reps)
       self.model.calcPoints()
       self.view.showPath(reps[0])
        
    def debug(self):    
        pass

            
        
#start of program
controller = Controller(Model(), View())    
controller.run()
