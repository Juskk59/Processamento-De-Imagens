# Elo 04 - Refinamento da máscara (erosão e dilatação)

import cv2 as cv
import numpy as np
from elo import Elo

class Elo_04(Elo):
    def processar(self, dados):
        # Refina a máscara e cria versões com erosão e dilatação
        mascara = dados["mascara"]
        imagem = dados["imagem"]
        
        if mascara is None:
            print("Elo_04: ERRO - Mascara nao encontrada")
            return dados
        
        # Garante que a máscara é binária
        _, mascara = cv.threshold(mascara, 127, 255, cv.THRESH_BINARY)
        
        # Kernels para operações morfológicas
        kernel_pequeno = np.ones((3, 3), np.uint8)
        kernel_medio = np.ones((5, 5), np.uint8)
        
        # Remove ruídos e fecha buracos
        mascara = cv.morphologyEx(mascara, cv.MORPH_OPEN, kernel_pequeno, iterations=2)
        mascara = cv.morphologyEx(mascara, cv.MORPH_CLOSE, kernel_medio, iterations=2)
        
        # === Erosão (diminui objeto) ===
        mascara_erosao = cv.erode(mascara, kernel_medio, iterations=3)
        dados["imagem_erosao"] = self.aplicar_mascara(imagem, mascara_erosao)
        
        # === Dilatação (aumenta objeto) ===
        mascara_dilatacao = cv.dilate(mascara, kernel_medio, iterations=3)
        dados["imagem_dilatacao"] = self.aplicar_mascara(imagem, mascara_dilatacao)
        
        # Suaviza bordas da máscara principal
        mascara = cv.dilate(mascara, kernel_pequeno, iterations=1)
        mascara = cv.erode(mascara, kernel_pequeno, iterations=1)
        mascara = cv.GaussianBlur(mascara, (5, 5), 0)
        _, mascara = cv.threshold(mascara, 127, 255, cv.THRESH_BINARY)
        
        dados["mascara"] = mascara
        print("Elo_04: Máscara refinada, erosão e dilatação criadas")
        
        return dados
    
    def aplicar_mascara(self, imagem, mascara):
        # Aplica a máscara na imagem com fundo branco
        mascara_suave = cv.GaussianBlur(mascara, (3, 3), 0)
        mascara_3canais = cv.cvtColor(mascara_suave, cv.COLOR_GRAY2BGR)
        mascara_norm = mascara_3canais.astype(float) / 255.0
        
        fundo_branco = np.ones_like(imagem) * 255
        resultado = (imagem.astype(float) * mascara_norm + 
                     fundo_branco.astype(float) * (1 - mascara_norm)).astype(np.uint8)
        
        return resultado
