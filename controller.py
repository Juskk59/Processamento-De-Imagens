# Controller - Faz a ponte entre View e Model

class Controller:
    def __init__(self):
        self.model = None
        self.view = None
    
    def set_view(self, view):
        # Define a interface
        self.view = view
    
    def set_model(self, model):
        # Define o model de processamento
        self.model = model
    
    def processar(self, imagem_original, pontos_objeto, pontos_fundo):
        # Envia a imagem e os pontos para o model processar
        if self.model:
            self.model.start_processing(imagem_original, pontos_objeto, pontos_fundo)
    
    def exibir_resultados(self, imagem_objeto, imagem_fundo, imagem_erosao, imagem_dilatacao):
        # Recebe o resultado do model e mostra na view
        if self.view:
            self.view.exibir_resultado(imagem_objeto, imagem_fundo, imagem_erosao, imagem_dilatacao)
