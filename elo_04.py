"""
Elo 04 - Refinamento e operacoes morfologicas
Refina a mascara e cria versoes com erosao e dilatacao
"""

import cv2 as cv
import numpy as np
from elo import Elo


class Elo_04(Elo):
    def processar(self, dados):
        """Refina a mascara e aplica operacoes morfologicas"""
        
        mascara = dados["mascara"]
        imagem = dados["imagem"]
        
        if mascara is None:
            print("Elo_04: ERRO - Mascara nao encontrada")
            return dados
        
        # Garante que a mascara e binaria (0 ou 255)
        _, mascara = cv.threshold(mascara, 127, 255, cv.THRESH_BINARY)
        
        # Cria os kernels (matrizes para as operacoes)
        kernel_pequeno = np.ones((3, 3), np.uint8)
        kernel_medio = np.ones((5, 5), np.uint8)
        
        # Remove ruido (pontos brancos isolados)
        mascara = cv.morphologyEx(mascara, cv.MORPH_OPEN, kernel_pequeno, iterations=2)
        
        # Fecha buracos (pontos pretos isolados)
        mascara = cv.morphologyEx(mascara, cv.MORPH_CLOSE, kernel_medio, iterations=2)
        
        # === CRIA VERSAO COM EROSAO ===
        # Erosao diminui o objeto (corroi as bordas)
        mascara_erosao = cv.erode(mascara, kernel_medio, iterations=3)
        
        # Aplica na imagem
        dados["imagem_erosao"] = self.aplicar_mascara(imagem, mascara_erosao)
        
        # === CRIA VERSAO COM DILATACAO ===
        # Dilatacao aumenta o objeto (expande as bordas)
        mascara_dilatacao = cv.dilate(mascara, kernel_medio, iterations=3)
        
        # Aplica na imagem
        dados["imagem_dilatacao"] = self.aplicar_mascara(imagem, mascara_dilatacao)
        
        # Suaviza as bordas da mascara principal
        mascara = cv.dilate(mascara, kernel_pequeno, iterations=1)
        mascara = cv.erode(mascara, kernel_pequeno, iterations=1)
        
        # Suavizacao final
        mascara = cv.GaussianBlur(mascara, (5, 5), 0)
        _, mascara = cv.threshold(mascara, 127, 255, cv.THRESH_BINARY)
        
        dados["mascara"] = mascara
        print("Elo_04: Mascara refinada, erosao e dilatacao criadas")
        
        return dados
    
    def aplicar_mascara(self, imagem, mascara):
        """
        Aplica uma mascara na imagem com fundo branco
        """
        # Suaviza a mascara
        mascara_suave = cv.GaussianBlur(mascara, (3, 3), 0)
        
        # Converte para 3 canais (RGB)
        mascara_3canais = cv.cvtColor(mascara_suave, cv.COLOR_GRAY2BGR)
        
        # Normaliza (de 0-255 para 0-1)
        mascara_norm = mascara_3canais.astype(float) / 255.0
        
        # Cria fundo branco
        fundo_branco = np.ones_like(imagem) * 255
        
        # Aplica: objeto onde mascara = branco, fundo branco onde mascara = preto
        resultado = (imagem.astype(float) * mascara_norm).astype(np.uint8)
        resultado = (resultado.astype(float) + 
                    fundo_branco.astype(float) * (1 - mascara_norm)).astype(np.uint8)
        
        return resultado