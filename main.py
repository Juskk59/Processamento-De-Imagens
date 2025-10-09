"""
Arquivo principal - Inicia o sistema MVC
"""

from view import View
from controller import Controller
from model import Model

if __name__ == "__main__":
    # Cria os componentes do MVC
    view = View()
    controller = Controller()
    model = Model()
    
    # Conecta os componentes
    controller.set_view(view)
    controller.set_model(model)
    
    view.set_controller(controller)
    model.set_controller(controller)
    
    # Inicia a interface
    view.run()