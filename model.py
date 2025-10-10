# Model - Gerencia o processamento de imagens usando a cadeia de elos

from elo_01 import Elo_01
from elo_02 import Elo_02
from elo_03 import Elo_03
from elo_04 import Elo_04
from elo_05 import Elo_05

class Model:
    def __init__(self):
        self.controller = None
        
        # Cria os elos da cadeia (cada um faz uma etapa do processo)
        self.elo1 = Elo_01()  
        self.elo2 = Elo_02()  
        self.elo3 = Elo_03()  
        self.elo4 = Elo_04()  
        self.elo5 = Elo_05()  
        
        # Liga os elos em sequência
        self.elo1.proximo = self.elo2
        self.elo2.proximo = self.elo3
        self.elo3.proximo = self.elo4
        self.elo4.proximo = self.elo5
    
    def set_controller(self, controller):
        # Define o controller para enviar os resultados depois
        self.controller = controller
    
    def start_processing(self, imagem_original, pontos_objeto, pontos_fundo):
        # Inicia o processamento passando a imagem e os pontos marcados
        dados = {
            "imagem": imagem_original.copy(),
            "pontos_objeto": pontos_objeto,
            "pontos_fundo": pontos_fundo,
            "escala": 1.0,
            "labels": None,
            "centroids": None,
            "mascara": None,
            "imagem_objeto": None,
            "imagem_fundo": None,
            "imagem_erosao": None,
            "imagem_dilatacao": None
        }
        
        # Começa o fluxo no primeiro elo
        resultado = self.elo1.executar(dados)
        
        # Mostra os resultados finais na interface
        if self.controller:
            self.controller.exibir_resultados(
                resultado["imagem_objeto"],
                resultado["imagem_fundo"],
                resultado["imagem_erosao"],
                resultado["imagem_dilatacao"]
            )
