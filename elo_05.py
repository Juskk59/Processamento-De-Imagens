"""
Elo 05 - Separacao final
Separa a imagem em objeto e fundo usando a mascara refinada
"""

import cv2 as cv
import numpy as np
from elo import Elo


class Elo_05(Elo):
    def processar(self, dados):
        """Separa objeto e fundo da imagem"""
        
        imagem = dados["imagem"]
        mascara = dados["mascara"]
        
        if mascara is None:
            print("Elo_05: ERRO - Mascara nao encontrada")
            return dados
        
        # Suaviza a mascara para transicoes mais naturais
        mascara_suave = cv.GaussianBlur(mascara, (3, 3), 0)
        
        # === EXTRAI O OBJETO ===
        # Converte mascara para 3 canais (RGB)
        mascara_3canais = cv.cvtColor(mascara_suave, cv.COLOR_GRAY2BGR)
        
        # Normaliza (de 0-255 para 0-1)
        mascara_norm = mascara_3canais.astype(float) / 255.0
        
        # Cria fundo branco
        fundo_branco = np.ones_like(imagem) * 255
        
        # Extrai objeto: mantem pixels onde mascara = branco
        # Onde mascara = preto, coloca fundo branco
        imagem_objeto = (imagem.astype(float) * mascara_norm).astype(np.uint8)
        imagem_objeto = (imagem_objeto.astype(float) + 
                        fundo_branco.astype(float) * (1 - mascara_norm)).astype(np.uint8)
        
        # === EXTRAI O FUNDO ===
        # Inverte a mascara (branco vira preto, preto vira branco)
        mascara_invertida = cv.bitwise_not(mascara_suave)
        
        # Converte para 3 canais
        mascara_inv_3canais = cv.cvtColor(mascara_invertida, cv.COLOR_GRAY2BGR)
        
        # Normaliza
        mascara_inv_norm = mascara_inv_3canais.astype(float) / 255.0
        
        # Extrai fundo: mantem pixels onde mascara invertida = branco
        # Onde mascara invertida = preto (era objeto), coloca branco
        imagem_fundo = (imagem.astype(float) * mascara_inv_norm).astype(np.uint8)
        imagem_fundo = (imagem_fundo.astype(float) + 
                       fundo_branco.astype(float) * (1 - mascara_inv_norm)).astype(np.uint8)
        
        # Guarda os resultados
        dados["imagem_objeto"] = imagem_objeto
        dados["imagem_fundo"] = imagem_fundo
        
        print("Elo_05: Objeto e fundo separados com sucesso")
        
        return dados