# Elo 01 - Redimensionamento da imagem

import cv2 as cv
from elo import Elo

class Elo_01(Elo):
    def processar(self, dados):
        # Redimensiona a imagem se for muito grande
        imagem = dados["imagem"]
        
        if imagem is None:
            print("Elo_01: ERRO - Imagem nao encontrada")
            return dados
        
        altura, largura = imagem.shape[:2]
        max_dimensao = 800
        
        # Se passar de 800px, reduz mantendo proporção
        if altura > max_dimensao or largura > max_dimensao:
            escala = max_dimensao / max(altura, largura)
            nova_largura = int(largura * escala)
            nova_altura = int(altura * escala)
            
            dados["imagem"] = cv.resize(imagem, (nova_largura, nova_altura), interpolation=cv.INTER_AREA)
            dados["escala"] = escala
            
            print(f"Elo_01: Redimensionada de {largura}x{altura} para {nova_largura}x{nova_altura}")
        else:
            dados["escala"] = 1.0
            print(f"Elo_01: Mantida no tamanho original {largura}x{altura}")
        
        return dados
