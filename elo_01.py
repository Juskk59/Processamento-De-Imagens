"""
Elo 01 - Redimensionamento da imagem
Reduz o tamanho se a imagem for muito grande
"""

import cv2 as cv
from elo import Elo


class Elo_01(Elo):
    def processar(self, dados):
        """Redimensiona a imagem se necessario"""
        
        imagem = dados["imagem"]
        
        # Verifica se a imagem existe
        if imagem is None:
            print("Elo_01: ERRO - Imagem nao encontrada")
            return dados
        
        # Pega as dimensoes da imagem
        altura, largura = imagem.shape[:2]
        
        # Define o tamanho maximo (800 pixels)
        max_dimensao = 800
        
        # Se a imagem for muito grande, redimensiona
        if altura > max_dimensao or largura > max_dimensao:
            # Calcula a escala de reducao
            escala = max_dimensao / max(altura, largura)
            
            # Calcula as novas dimensoes
            nova_largura = int(largura * escala)
            nova_altura = int(altura * escala)
            
            # Redimensiona a imagem
            dados["imagem"] = cv.resize(
                imagem,
                (nova_largura, nova_altura),
                interpolation=cv.INTER_AREA
            )
            
            # Guarda a escala para ajustar os pontos depois
            dados["escala"] = escala
            
            print(f"Elo_01: Imagem redimensionada de {largura}x{altura} para {nova_largura}x{nova_altura}")
        else:
            # Mantem tamanho original
            dados["escala"] = 1.0
            print(f"Elo_01: Imagem mantida no tamanho original {largura}x{altura}")
        
        return dados