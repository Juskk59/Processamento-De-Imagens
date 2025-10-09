"""
Model - Gerencia o processamento de imagens
Coordena a cadeia de responsabilidade dos elos
"""

from elo_01 import Elo_01
from elo_02 import Elo_02
from elo_03 import Elo_03
from elo_04 import Elo_04
from elo_05 import Elo_05


class Model:
    def __init__(self):
        self.controller = None
        
        # Cria os elos da cadeia de responsabilidade
        self.elo1 = Elo_01()  # Redimensionamento
        self.elo2 = Elo_02()  # Segmentacao K-means
        self.elo3 = Elo_03()  # Criacao da mascara
        self.elo4 = Elo_04()  # Refinamento (erosao e dilatacao)
        self.elo5 = Elo_05()  # Separacao final (objeto e fundo)
        
        # Liga os elos em sequencia
        self.elo1.proximo = self.elo2
        self.elo2.proximo = self.elo3
        self.elo3.proximo = self.elo4
        self.elo4.proximo = self.elo5
    
    def set_controller(self, controller):
        """Define o controller"""
        self.controller = controller
    
    def start_processing(self, imagem_original, pontos_objeto, pontos_fundo):
        """
        Inicia o processamento atraves da cadeia de elos
        
        Parametros:
            imagem_original: imagem em formato numpy array (RGB)
            pontos_objeto: lista de tuplas (x, y) dos pontos do objeto
            pontos_fundo: lista de tuplas (x, y) dos pontos do fundo
        """
        # Monta o dicionario com os dados iniciais
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
        
        # Inicia a cadeia de processamento no primeiro elo
        resultado = self.elo1.executar(dados)
        
        # Envia os resultados para o controller
        if self.controller:
            self.controller.exibir_resultados(
                resultado["imagem_objeto"],
                resultado["imagem_fundo"],
                resultado["imagem_erosao"],
                resultado["imagem_dilatacao"]
            )