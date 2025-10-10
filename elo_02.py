# Elo 02 - Segmentação com K-means

import cv2 as cv
import numpy as np
from sklearn.cluster import KMeans
from elo import Elo

class Elo_02(Elo):
    def processar(self, dados):
        # Aplica K-means para agrupar pixels parecidos
        imagem = dados["imagem"]
        pontos_objeto = dados["pontos_objeto"]
        pontos_fundo = dados["pontos_fundo"]
        escala = dados["escala"]
        
        # Ajusta pontos se a imagem foi redimensionada
        if escala != 1.0:
            pontos_objeto = [(int(x * escala), int(y * escala)) for x, y in pontos_objeto]
            pontos_fundo = [(int(x * escala), int(y * escala)) for x, y in pontos_fundo]
            dados["pontos_objeto"] = pontos_objeto
            dados["pontos_fundo"] = pontos_fundo
        
        altura, largura = imagem.shape[:2]
        pixels = imagem.reshape(-1, 3).astype(np.float32)
        
        num_clusters = 15
        print(f"Elo_02: Executando K-means com {num_clusters} clusters...")
        
        # Roda o K-means
        kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init=10, max_iter=300)
        kmeans.fit(pixels)
        
        # Salva os grupos e as cores médias
        dados["labels"] = kmeans.labels_.reshape(altura, largura)
        dados["centroids"] = kmeans.cluster_centers_
        
        print("Elo_02: K-means concluído")
        return dados
