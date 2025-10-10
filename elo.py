class Elo:
    def __init__(self):
        # Guarda o próximo elo da cadeia
        self.proximo = None
    
    def processar(self, dados):
        # Método que cada elo específico vai sobrescrever
        return dados
    
    def executar(self, dados):
        # Processa os dados deste elo
        dados = self.processar(dados)
        
        # Passa os dados para o próximo elo (se existir)
        if self.proximo is not None:
            return self.proximo.executar(dados)
        
        # Se for o último elo, retorna o resultado final
        return dados
