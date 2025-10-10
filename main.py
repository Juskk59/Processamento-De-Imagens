# Arquivo principal - Inicia o sistema MVC

from view import View
from controller import Controller
from model import Model

if __name__ == "__main__":
    view = View()
    controller = Controller()
    model = Model()
    
    controller.set_view(view)
    controller.set_model(model)
    view.set_controller(controller)
    model.set_controller(controller)
    
    view.run()
