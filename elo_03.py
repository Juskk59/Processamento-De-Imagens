"""
Elo 03 - Criacao da mascara
Cria mascara binaria separando objeto e fundo
"""

import numpy as np
from elo import Elo


class Elo_03(Elo):
    def processar(self, dados):
        """Cria a mascara a partir dos clusters do K-means"""
        
        imagem = dados["imagem"]
        pontos_objeto = dados["pontos_objeto"]
        pontos_fundo = dados["pontos_fundo"]
        labels = dados["labels"]
        centroids = dados["centroids"]
        
        altura, largura = imagem.shape[:2]
        num_clusters = len(centroids)
        
        # Identifica quais clusters pertencem ao objeto e ao fundo
        clusters_objeto = set()
        clusters_fundo = set()
        
        # Para cada ponto marcado como objeto
        for x, y in pontos_objeto:
            if 0 <= y < altura and 0 <= x < largura:
                cluster_id = labels[y, x]
                clusters_objeto.add(cluster_id)
        
        # Para cada ponto marcado como fundo
        for x, y in pontos_fundo:
            if 0 <= y < altura and 0 <= x < largura:
                cluster_id = labels[y, x]
                clusters_fundo.add(cluster_id)
        
        # Remove clusters que aparecem em ambos
        # (prioriza objeto)
        clusters_fundo = clusters_fundo - clusters_objeto
        
        print(f"Elo_03: {len(clusters_objeto)} clusters de objeto, {len(clusters_fundo)} clusters de fundo")
        
        # Calcula a cor media dos clusters de objeto e fundo
        cor_media_objeto = None
        cor_media_fundo = None
        
        if len(clusters_objeto) > 0:
            cores_obj = centroids[list(clusters_objeto)]
            cor_media_objeto = np.mean(cores_obj, axis=0)
        
        if len(clusters_fundo) > 0:
            cores_bg = centroids[list(clusters_fundo)]
            cor_media_fundo = np.mean(cores_bg, axis=0)
        
        # Cria a mascara (branco = objeto, preto = fundo)
        mascara = np.zeros((altura, largura), dtype=np.uint8)
        
        # Para cada cluster
        for cluster_id in range(num_clusters):
            cor_cluster = centroids[cluster_id]
            
            if cluster_id in clusters_objeto:
                # Cluster de objeto - pinta de branco
                mascara[labels == cluster_id] = 255
            
            elif cluster_id in clusters_fundo:
                # Cluster de fundo - pinta de preto
                mascara[labels == cluster_id] = 0
            
            else:
                # Cluster nao marcado - classifica pela distancia
                if cor_media_objeto is not None and cor_media_fundo is not None:
                    # Calcula distancia para objeto e fundo
                    dist_obj = np.linalg.norm(cor_cluster - cor_media_objeto)
                    dist_bg = np.linalg.norm(cor_cluster - cor_media_fundo)
                    
                    # Escolhe o mais proximo
                    if dist_obj < dist_bg:
                        mascara[labels == cluster_id] = 255
                    else:
                        mascara[labels == cluster_id] = 0
                
                elif cor_media_objeto is not None:
                    # So tem objeto marcado
                    dist_obj = np.linalg.norm(cor_cluster - cor_media_objeto)
                    
                    # Calcula threshold baseado nos clusters de objeto
                    distancias_obj = [
                        np.linalg.norm(centroids[cid] - cor_media_objeto)
                        for cid in clusters_objeto
                    ]
                    threshold = np.mean(distancias_obj) * 1.5
                    
                    if dist_obj < threshold:
                        mascara[labels == cluster_id] = 255
                    else:
                        mascara[labels == cluster_id] = 0
                else:
                    # Sem referencia - considera fundo
                    mascara[labels == cluster_id] = 0
        
        dados["mascara"] = mascara
        print("Elo_03: Mascara criada com sucesso")
        
        return dados