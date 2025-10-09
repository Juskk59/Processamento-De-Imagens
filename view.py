"""
View - Interface grafica do sistema
Responsavel por toda interacao com o usuario
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import cv2 as cv
import numpy as np


class View:
    def __init__(self):
        self.controller = None
        
        # Cria a janela principal
        self.root = tk.Tk()
        self.root.title("Remocao de Fundo - K-means")
        self.root.geometry("1200x800")
        
        # Variaveis para armazenar a imagem
        self.imagem_original = None
        self.imagem_tk = None
        self.escala = 1.0
        
        # Listas para guardar os pontos clicados
        self.pontos_objeto = []
        self.pontos_fundo = []
        
        # Controla o modo de selecao (objeto ou fundo)
        self.modo_objeto = tk.IntVar(value=1)
        self.modo_fundo = tk.IntVar(value=0)
        
        # Variaveis para guardar resultados
        self.imagem_objeto_resultado = None
        self.imagem_fundo_resultado = None
        self.imagem_erosao_resultado = None
        self.imagem_dilatacao_resultado = None
        
        # Constroi a interface
        self.desenhar_interface()
    
    def desenhar_interface(self):
        """Cria todos os elementos da interface"""
        
        # Frame superior - controles
        frame_controles = tk.Frame(self.root, bg="#2c3e50", height=100)
        frame_controles.pack(side=tk.TOP, fill=tk.X)
        
        # Botao para carregar imagem
        btn_carregar = tk.Button(
            frame_controles,
            text="Carregar Imagem",
            command=self.carregar_imagem,
            bg="#3498db",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10
        )
        btn_carregar.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Frame para checkboxes
        frame_modo = tk.Frame(frame_controles, bg="#2c3e50")
        frame_modo.pack(side=tk.LEFT, padx=20)
        
        tk.Label(
            frame_modo,
            text="Modo de Selecao:",
            bg="#2c3e50",
            fg="white",
            font=("Arial", 10, "bold")
        ).pack(anchor=tk.W)
        
        # Checkbox para objeto
        chk_objeto = tk.Checkbutton(
            frame_modo,
            text="Marcar Objeto (Verde)",
            variable=self.modo_objeto,
            command=lambda: self.alternar_modo("objeto"),
            bg="#2c3e50",
            fg="white",
            selectcolor="#27ae60",
            font=("Arial", 10)
        )
        chk_objeto.pack(anchor=tk.W)
        
        # Checkbox para fundo
        chk_fundo = tk.Checkbutton(
            frame_modo,
            text="Marcar Fundo (Vermelho)",
            variable=self.modo_fundo,
            command=lambda: self.alternar_modo("fundo"),
            bg="#2c3e50",
            fg="white",
            selectcolor="#e74c3c",
            font=("Arial", 10)
        )
        chk_fundo.pack(anchor=tk.W)
        
        # Botao para processar
        btn_processar = tk.Button(
            frame_controles,
            text="Processar Imagem",
            command=self.processar_imagem,
            bg="#27ae60",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10
        )
        btn_processar.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Botao para limpar
        btn_limpar = tk.Button(
            frame_controles,
            text="Limpar Selecoes",
            command=self.limpar_selecoes,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10
        )
        btn_limpar.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Botao para salvar
        btn_salvar = tk.Button(
            frame_controles,
            text="Salvar Resultados",
            command=self.salvar_resultados,
            bg="#9b59b6",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10
        )
        btn_salvar.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Frame para o canvas
        frame_canvas = tk.Frame(self.root, bg="#ecf0f1")
        frame_canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Canvas para exibir a imagem
        self.canvas = tk.Canvas(frame_canvas, bg="#bdc3c7", cursor="crosshair")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.clique_mouse)
        
        # Label de status
        self.label_status = tk.Label(
            self.root,
            text="Carregue uma imagem para comecar",
            bg="#34495e",
            fg="white",
            font=("Arial", 10),
            anchor=tk.W,
            padx=10
        )
        self.label_status.pack(side=tk.BOTTOM, fill=tk.X)
    
    def alternar_modo(self, modo_clicado):
        """Garante que apenas um checkbox fica marcado"""
        if modo_clicado == "objeto":
            if self.modo_objeto.get() == 1:
                self.modo_fundo.set(0)
            else:
                if self.modo_fundo.get() == 0:
                    self.modo_objeto.set(1)
        else:
            if self.modo_fundo.get() == 1:
                self.modo_objeto.set(0)
            else:
                if self.modo_objeto.get() == 0:
                    self.modo_fundo.set(1)
        
        self.atualizar_status()
    
    def atualizar_status(self):
        """Atualiza a barra de status"""
        modo = "OBJETO (Verde)" if self.modo_objeto.get() == 1 else "FUNDO (Vermelho)"
        texto = f"Modo: {modo} | Pontos Objeto: {len(self.pontos_objeto)} | Pontos Fundo: {len(self.pontos_fundo)}"
        self.label_status.config(text=texto)
    
    def carregar_imagem(self):
        """Abre uma imagem do computador"""
        arquivo = filedialog.askopenfilename(
            title="Selecione uma imagem",
            filetypes=[("Imagens", "*.jpg *.jpeg *.png *.bmp")]
        )
        
        if arquivo:
            # Le a imagem com OpenCV
            self.imagem_original = cv.imread(arquivo)
            
            if self.imagem_original is None:
                messagebox.showerror("Erro", "Nao foi possivel carregar a imagem")
                return
            
            # Converte de BGR para RGB
            self.imagem_original = cv.cvtColor(self.imagem_original, cv.COLOR_BGR2RGB)
            
            # Limpa selecoes anteriores
            self.limpar_selecoes()
            
            # Exibe a imagem
            self.exibir_imagem(self.imagem_original)
            
            self.label_status.config(text=f"Imagem carregada: {arquivo}")
    
    def exibir_imagem(self, imagem):
        """Exibe a imagem no canvas"""
        # Pega dimensoes do canvas
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Valores padrao se canvas nao foi renderizado
        if canvas_width <= 1:
            canvas_width = 1000
        if canvas_height <= 1:
            canvas_height = 600
        
        # Calcula escala para ajustar ao canvas
        altura_img, largura_img = imagem.shape[:2]
        escala_w = canvas_width / largura_img
        escala_h = canvas_height / altura_img
        self.escala = min(escala_w, escala_h, 1.0)
        
        # Redimensiona
        nova_largura = int(largura_img * self.escala)
        nova_altura = int(altura_img * self.escala)
        imagem_redimensionada = cv.resize(imagem, (nova_largura, nova_altura))
        
        # Converte para formato Tkinter usando PPM
        imagem_bgr = cv.cvtColor(imagem_redimensionada, cv.COLOR_RGB2BGR)
        sucesso, buffer = cv.imencode('.ppm', imagem_bgr)
        
        if sucesso:
            self.imagem_tk = tk.PhotoImage(data=buffer.tobytes())
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.imagem_tk)
            
            # Redesenha os pontos marcados
            self.redesenhar_pontos()
    
    def clique_mouse(self, event):
        """Trata o clique do mouse no canvas"""
        if self.imagem_original is None:
            return
        
        # Converte coordenadas para a imagem original
        x_original = int(event.x / self.escala)
        y_original = int(event.y / self.escala)
        
        # Verifica qual modo esta ativo
        if self.modo_objeto.get() == 1:
            # Adiciona ponto de objeto
            self.pontos_objeto.append((x_original, y_original))
            
            # Desenha ponto verde
            raio = 5
            self.canvas.create_oval(
                event.x - raio, event.y - raio,
                event.x + raio, event.y + raio,
                fill="green", outline="white", width=2, tags="ponto_objeto"
            )
        else:
            # Adiciona ponto de fundo
            self.pontos_fundo.append((x_original, y_original))
            
            # Desenha ponto vermelho
            raio = 5
            self.canvas.create_oval(
                event.x - raio, event.y - raio,
                event.x + raio, event.y + raio,
                fill="red", outline="white", width=2, tags="ponto_fundo"
            )
        
        self.atualizar_status()
    
    def redesenhar_pontos(self):
        """Redesenha todos os pontos marcados"""
        # Pontos de objeto (verde)
        for x, y in self.pontos_objeto:
            x_canvas = int(x * self.escala)
            y_canvas = int(y * self.escala)
            raio = 5
            self.canvas.create_oval(
                x_canvas - raio, y_canvas - raio,
                x_canvas + raio, y_canvas + raio,
                fill="green", outline="white", width=2, tags="ponto_objeto"
            )
        
        # Pontos de fundo (vermelho)
        for x, y in self.pontos_fundo:
            x_canvas = int(x * self.escala)
            y_canvas = int(y * self.escala)
            raio = 5
            self.canvas.create_oval(
                x_canvas - raio, y_canvas - raio,
                x_canvas + raio, y_canvas + raio,
                fill="red", outline="white", width=2, tags="ponto_fundo"
            )
    
    def limpar_selecoes(self):
        """Remove todas as marcacoes"""
        self.pontos_objeto = []
        self.pontos_fundo = []
        self.canvas.delete("ponto_objeto")
        self.canvas.delete("ponto_fundo")
        self.atualizar_status()
    
    def processar_imagem(self):
        """Chama o controller para processar a imagem"""
        if self.imagem_original is None:
            messagebox.showwarning("Aviso", "Carregue uma imagem primeiro")
            return
        
        if len(self.pontos_objeto) == 0 or len(self.pontos_fundo) == 0:
            messagebox.showwarning("Aviso", "Marque pelo menos um ponto de objeto e um de fundo")
            return
        
        self.label_status.config(text="Processando imagem...")
        self.root.update()
        
        # Chama o controller
        self.controller.processar(
            self.imagem_original,
            self.pontos_objeto,
            self.pontos_fundo
        )
    
    def exibir_resultado(self, imagem_objeto, imagem_fundo, imagem_erosao, imagem_dilatacao):
        """Cria janela com os resultados"""
        # Guarda os resultados
        self.imagem_objeto_resultado = imagem_objeto
        self.imagem_fundo_resultado = imagem_fundo
        self.imagem_erosao_resultado = imagem_erosao
        self.imagem_dilatacao_resultado = imagem_dilatacao
        
        # Cria nova janela
        janela_resultado = tk.Toplevel(self.root)
        janela_resultado.title("Resultados da Remocao de Fundo")
        janela_resultado.geometry("1400x900")
        
        # Frame superior - objeto e fundo
        frame_superior = tk.Frame(janela_resultado)
        frame_superior.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Frame do objeto
        frame_objeto = tk.Frame(frame_superior)
        frame_objeto.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        tk.Label(frame_objeto, text="Objeto Extraido", font=("Arial", 14, "bold")).pack()
        
        canvas_objeto = tk.Canvas(frame_objeto, bg="#bdc3c7")
        canvas_objeto.pack(fill=tk.BOTH, expand=True)
        
        # Frame do fundo
        frame_fundo = tk.Frame(frame_superior)
        frame_fundo.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        tk.Label(frame_fundo, text="Fundo Extraido", font=("Arial", 14, "bold")).pack()
        
        canvas_fundo = tk.Canvas(frame_fundo, bg="#bdc3c7")
        canvas_fundo.pack(fill=tk.BOTH, expand=True)
        
        # Frame inferior - erosao e dilatacao
        frame_inferior = tk.Frame(janela_resultado)
        frame_inferior.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Frame da erosao
        frame_erosao = tk.Frame(frame_inferior)
        frame_erosao.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        tk.Label(frame_erosao, text="Erosao", font=("Arial", 14, "bold")).pack()
        
        canvas_erosao = tk.Canvas(frame_erosao, bg="#bdc3c7")
        canvas_erosao.pack(fill=tk.BOTH, expand=True)
        
        # Frame da dilatacao
        frame_dilatacao = tk.Frame(frame_inferior)
        frame_dilatacao.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        tk.Label(frame_dilatacao, text="Dilatacao", font=("Arial", 14, "bold")).pack()
        
        canvas_dilatacao = tk.Canvas(frame_dilatacao, bg="#bdc3c7")
        canvas_dilatacao.pack(fill=tk.BOTH, expand=True)
        
        # Exibe as imagens
        self.exibir_em_canvas(canvas_objeto, imagem_objeto)
        self.exibir_em_canvas(canvas_fundo, imagem_fundo)
        self.exibir_em_canvas(canvas_erosao, imagem_erosao)
        self.exibir_em_canvas(canvas_dilatacao, imagem_dilatacao)
        
        self.label_status.config(text="Processamento concluido!")
    
    def exibir_em_canvas(self, canvas, imagem):
        """Exibe uma imagem em um canvas especifico"""
        canvas.update()
        
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        
        if canvas_width <= 1:
            canvas_width = 350
        if canvas_height <= 1:
            canvas_height = 400
        
        # Calcula escala
        altura_img, largura_img = imagem.shape[:2]
        escala_w = canvas_width / largura_img
        escala_h = canvas_height / altura_img
        escala = min(escala_w, escala_h, 1.0)
        
        # Redimensiona
        nova_largura = int(largura_img * escala)
        nova_altura = int(altura_img * escala)
        imagem_redimensionada = cv.resize(imagem, (nova_largura, nova_altura))
        
        # Converte para Tkinter usando PPM
        imagem_bgr = cv.cvtColor(imagem_redimensionada, cv.COLOR_RGB2BGR)
        sucesso, buffer = cv.imencode('.ppm', imagem_bgr)
        
        if sucesso:
            imagem_tk = tk.PhotoImage(data=buffer.tobytes())
            # Guarda referencia para evitar garbage collection
            canvas.imagem_tk = imagem_tk
            canvas.create_image(0, 0, anchor=tk.NW, image=imagem_tk)
    
    def salvar_resultados(self):
        """Salva as 4 imagens resultantes"""
        if self.imagem_objeto_resultado is None:
            messagebox.showwarning("Aviso", "Processe uma imagem primeiro")
            return
        
        # Salva objeto
        arquivo = filedialog.asksaveasfilename(
            title="Salvar Imagem do Objeto",
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")]
        )
        if arquivo:
            img = cv.cvtColor(self.imagem_objeto_resultado, cv.COLOR_RGB2BGR)
            cv.imwrite(arquivo, img)
        
        # Salva fundo
        arquivo = filedialog.asksaveasfilename(
            title="Salvar Imagem do Fundo",
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")]
        )
        if arquivo:
            img = cv.cvtColor(self.imagem_fundo_resultado, cv.COLOR_RGB2BGR)
            cv.imwrite(arquivo, img)
        
        # Salva erosao
        arquivo = filedialog.asksaveasfilename(
            title="Salvar Imagem com Erosao",
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")]
        )
        if arquivo:
            img = cv.cvtColor(self.imagem_erosao_resultado, cv.COLOR_RGB2BGR)
            cv.imwrite(arquivo, img)
        
        # Salva dilatacao
        arquivo = filedialog.asksaveasfilename(
            title="Salvar Imagem com Dilatacao",
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")]
        )
        if arquivo:
            img = cv.cvtColor(self.imagem_dilatacao_resultado, cv.COLOR_RGB2BGR)
            cv.imwrite(arquivo, img)
        
        messagebox.showinfo("Sucesso", "Imagens salvas com sucesso!")
        self.label_status.config(text="Resultados salvos com sucesso!")
    
    def set_controller(self, controller):
        """Define o controller"""
        self.controller = controller
    
    def run(self):
        """Inicia a interface grafica"""
        self.root.mainloop()