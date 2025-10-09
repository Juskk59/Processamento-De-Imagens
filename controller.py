"""
Controller - Intermediário entre View e Model
Recebe comandos da interface e repassa para o processamento
"""

class Controller:
    def __init__(self):
        self.model = None
        self.view = None
    
    def set_view(self, view):
        """Define a view"""
        self.view = view
    
    def set_model(self, model):
        """Define o model"""
        self.model = model
    
    def processar(self, imagem_original, pontos_objeto, pontos_fundo):
        """
        Recebe dados da interface e envia para processamento
        
        Parametros:
            imagem_original: imagem carregada pelo usuario
            pontos_objeto: lista de pontos marcados como objeto
            pontos_fundo: lista de pontos marcados como fundo
        """
        if self.model:
            self.model.start_processing(imagem_original, pontos_objeto, pontos_fundo)
    
    def exibir_resultados(self, imagem_objeto, imagem_fundo, imagem_erosao, imagem_dilatacao):
        """
        Recebe resultados do model e atualiza a interface
        
        Parametros:
            imagem_objeto: imagem do objeto extraido
            imagem_fundo: imagem do fundo extraido
            imagem_erosao: imagem apos erosao
            imagem_dilatacao: imagem apos dilatacao
        """
        if self.view:
            self.view.exibir_resultado(imagem_objeto, imagem_fundo, imagem_erosao, imagem_dilatacao)