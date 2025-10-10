# Elo 03 - Criação da máscara (objeto x fundo)

import numpy as np
from elo import Elo

class Elo_03(Elo):
    def processar(self, dados):
        # Cria a máscara a partir dos clusters do K-means
        imagem = dados["imagem"]
        pontos_objeto = dados["pontos_objeto"]
        pontos_fundo = dados["pontos_fundo"]
        labels = dados["labels"]
        centroids = dados["centroids"]
        
        altura, largura = imagem.shape[:2]
        num_clusters = len(centroids)
        
        clusters_objeto = set()
        clusters_fundo = set()
        
        # Marca quais clusters pertencem ao objeto e ao fundo
        for x, y in pontos_objeto:
            if 0 <= y < altura and 0 <= x < largura:
                clusters_objeto.add(labels[y, x])
        
        for x, y in pontos_fundo:
            if 0 <= y < altura and 0 <= x < largura:
                clusters_fundo.add(labels[y, x])
        
        # Evita duplicidade
        clusters_fundo = clusters_fundo - clusters_objeto
        print(f"Elo_03: {len(clusters_objeto)} clusters de objeto, {len(clusters_fundo)} de fundo")
        
        # Calcula cor média dos grupos
        cor_media_objeto = np.mean(centroids[list(clusters_objeto)], axis=0) if clusters_objeto else None
        cor_media_fundo = np.mean(centroids[list(clusters_fundo)], axis=0) if clusters_fundo else None
        
        # Cria máscara binária (255 = objeto, 0 = fundo)
        mascara = np.zeros((altura, largura), dtype=np.uint8)
        
        for cluster_id in range(num_clusters):
            cor_cluster = centroids[cluster_id]
            
            if cluster_id in clusters_objeto:
                mascara[labels == cluster_id] = 255
            elif cluster_id in clusters_fundo:
                mascara[labels == cluster_id] = 0
            else:
                # Decide pelo mais próximo (objeto ou fundo)
                if cor_media_objeto is not None and cor_media_fundo is not None:
                    dist_obj = np.linalg.norm(cor_cluster - cor_media_objeto)
                    dist_bg = np.linalg.norm(cor_cluster - cor_media_fundo)
                    mascara[labels == cluster_id] = 255 if dist_obj < dist_bg else 0
                elif cor_media_objeto is not None:
                    mascara[labels == cluster_id] = 255
                else:
                    mascara[labels == cluster_id] = 0
        
        dados["mascara"] = mascara
        print("Elo_03: Máscara criada com sucesso")
        return dados
