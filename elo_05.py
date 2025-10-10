#Elo 05 - Separa a imagem em objeto e fundo usando a máscara

import cv2 as cv
import numpy as np
from elo import Elo

class Elo_05(Elo):
    def processar(self, dados):
        #Separa objeto e fundo da imagem

        imagem = dados["imagem"]
        mascara = dados["mascara"]

        if mascara is None:
            print("Elo_05: ERRO - Máscara não encontrada")
            return dados

        # Suaviza a máscara
        mascara_suave = cv.GaussianBlur(mascara, (3, 3), 0)

        # Extrai objeto
        mascara_3canais = cv.cvtColor(mascara_suave, cv.COLOR_GRAY2BGR)
        mascara_norm = mascara_3canais.astype(float) / 255.0
        fundo_branco = np.ones_like(imagem) * 255
        imagem_objeto = (imagem.astype(float) * mascara_norm).astype(np.uint8)
        imagem_objeto = (imagem_objeto.astype(float) + 
                        fundo_branco.astype(float) * (1 - mascara_norm)).astype(np.uint8)

        # Extrai fundo
        mascara_invertida = cv.bitwise_not(mascara_suave)
        mascara_inv_3canais = cv.cvtColor(mascara_invertida, cv.COLOR_GRAY2BGR)
        mascara_inv_norm = mascara_inv_3canais.astype(float) / 255.0
        imagem_fundo = (imagem.astype(float) * mascara_inv_norm).astype(np.uint8)
        imagem_fundo = (imagem_fundo.astype(float) + 
                       fundo_branco.astype(float) * (1 - mascara_inv_norm)).astype(np.uint8)

        # Salva resultados
        dados["imagem_objeto"] = imagem_objeto
        dados["imagem_fundo"] = imagem_fundo

        print("Elo_05: Objeto e fundo separados")

        return dados
