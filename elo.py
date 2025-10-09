"""
Elo - Classe base para a cadeia de responsabilidade
Cada elo processa uma parte e passa para o proximo
"""

class Elo:
    def __init__(self):
        # Proximo elo da cadeia
        self.proximo = None
    
    def processar(self, dados):
        """
        Metodo que cada elo deve implementar
        Recebe os dados, processa e retorna
        """
        # Cada elo filho vai sobrescrever este metodo
        return dados
    
    def executar(self, dados):
        """
        Executa o processamento deste elo e passa para o proximo
        """
        # Processa os dados neste elo
        dados = self.processar(dados)
        
        # Se existe proximo elo, passa os dados
        if self.proximo is not None:
            return self.proximo.executar(dados)
        
        # Se nao tem proximo, retorna o resultado
        return dados