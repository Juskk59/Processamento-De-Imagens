"""
Elo 02 - Segmentacao com K-means
Agrupa pixels parecidos usando K-means
"""

import cv2 as cv
import numpy as np
from sklearn.cluster import KMeans
from elo import Elo


class Elo_02(Elo):
    def processar(self, dados):
        """Aplica K-means para segmentar a imagem"""
        
        imagem = dados["imagem"]
        pontos_objeto = dados["pontos_objeto"]
        pontos_fundo = dados["pontos_fundo"]
        escala = dados["escala"]
        
        # Ajusta as coordenadas dos pontos se a imagem foi redimensionada
        if escala != 1.0:
            pontos_objeto = [(int(x * escala), int(y * escala)) for x, y in pontos_objeto]
            pontos_fundo = [(int(x * escala), int(y * escala)) for x, y in pontos_fundo]
            dados["pontos_objeto"] = pontos_objeto
            dados["pontos_fundo"] = pontos_fundo
        
        # Pega as dimensoes
        altura, largura = imagem.shape[:2]
        
        # Transforma a imagem em uma lista de pixels
        # Cada pixel tem 3 valores (R, G, B)
        pixels = imagem.reshape(-1, 3).astype(np.float32)
        
        # Define quantos grupos queremos
        num_clusters = 15
        
        print(f"Elo_02: Executando K-means com {num_clusters} clusters...")
        
        # Aplica o K-means
        kmeans = KMeans(
            n_clusters=num_clusters,
            random_state=42,
            n_init=10,
            max_iter=300
        )
        kmeans.fit(pixels)
        
        # Pega os resultados
        # labels: qual grupo cada pixel pertence
        # centroids: cor media de cada grupo
        labels = kmeans.labels_.reshape(altura, largura)
        centroids = kmeans.cluster_centers_
        
        # Guarda os resultados para o proximo elo
        dados["labels"] = labels
        dados["centroids"] = centroids
        
        print("Elo_02: K-means concluido com sucesso")
        
        return dados