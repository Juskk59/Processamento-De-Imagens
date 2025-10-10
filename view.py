import tkinter as tk
from tkinter import filedialog, messagebox
import cv2 as cv
import numpy as np


class View:
    def __init__(self):
        self.controller = None
        
        # Janela principal
        self.root = tk.Tk()
        self.root.title("Remocao de Fundo - K-means")
        self.root.geometry("1200x800")
        
        # Imagem e escala
        self.imagem_original = None
        self.imagem_tk = None
        self.escala = 1.0
        
        # Pontos de objeto e fundo
        self.pontos_objeto = []
        self.pontos_fundo = []
        
        # Modo de seleção
        self.modo_objeto = tk.IntVar(value=1)
        self.modo_fundo = tk.IntVar(value=0)
        
        # Resultados
        self.imagem_objeto_resultado = None
        self.imagem_fundo_resultado = None
        self.imagem_erosao_resultado = None
        self.imagem_dilatacao_resultado = None
        
        # Monta interface
        self.desenhar_interface()
    
    def desenhar_interface(self):
        # Frame superior com botões
        frame_controles = tk.Frame(self.root, bg="#2c3e50", height=100)
        frame_controles.pack(side=tk.TOP, fill=tk.X)
        
        # Botão carregar imagem
        btn_carregar = tk.Button(frame_controles, text="Carregar Imagem", command=self.carregar_imagem, bg="#3498db", fg="white", font=("Arial", 12, "bold"), padx=20, pady=10)
        btn_carregar.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Checkboxes de seleção
        frame_modo = tk.Frame(frame_controles, bg="#2c3e50")
        frame_modo.pack(side=tk.LEFT, padx=20)
        
        tk.Label(frame_modo, text="Modo de Selecao:", bg="#2c3e50", fg="white", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        
        chk_objeto = tk.Checkbutton(frame_modo, text="Marcar Objeto (Verde)", variable=self.modo_objeto, command=lambda: self.alternar_modo("objeto"), bg="#2c3e50", fg="white", selectcolor="#27ae60", font=("Arial", 10))
        chk_objeto.pack(anchor=tk.W)
        
        chk_fundo = tk.Checkbutton(frame_modo, text="Marcar Fundo (Vermelho)", variable=self.modo_fundo, command=lambda: self.alternar_modo("fundo"), bg="#2c3e50", fg="white", selectcolor="#e74c3c", font=("Arial", 10))
        chk_fundo.pack(anchor=tk.W)
        
        # Botões processar, limpar e salvar
        btn_processar = tk.Button(frame_controles, text="Processar Imagem", command=self.processar_imagem, bg="#27ae60", fg="white", font=("Arial", 12, "bold"), padx=20, pady=10)
        btn_processar.pack(side=tk.LEFT, padx=10, pady=10)
        
        btn_limpar = tk.Button(frame_controles, text="Limpar Selecoes", command=self.limpar_selecoes, bg="#e74c3c", fg="white", font=("Arial", 12, "bold"), padx=20, pady=10)
        btn_limpar.pack(side=tk.LEFT, padx=10, pady=10)
        
        btn_salvar = tk.Button(frame_controles, text="Salvar Resultados", command=self.salvar_resultados, bg="#9b59b6", fg="white", font=("Arial", 12, "bold"), padx=20, pady=10)
        btn_salvar.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Canvas para imagem
        frame_canvas = tk.Frame(self.root, bg="#ecf0f1")
        frame_canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.canvas = tk.Canvas(frame_canvas, bg="#bdc3c7", cursor="crosshair")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.clique_mouse)
        
        # Status
        self.label_status = tk.Label(self.root, text="Carregue uma imagem para comecar", bg="#34495e", fg="white", font=("Arial", 10), anchor=tk.W, padx=10)
        self.label_status.pack(side=tk.BOTTOM, fill=tk.X)
    
    def alternar_modo(self, modo_clicado):
        # Garante só um modo ativo
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
        # Atualiza texto de status
        modo = "OBJETO (Verde)" if self.modo_objeto.get() == 1 else "FUNDO (Vermelho)"
        texto = f"Modo: {modo} | Pontos Objeto: {len(self.pontos_objeto)} | Pontos Fundo: {len(self.pontos_fundo)}"
        self.label_status.config(text=texto)
    
    def carregar_imagem(self):
        # Abre imagem
        arquivo = filedialog.askopenfilename(title="Selecione uma imagem", filetypes=[("Imagens", "*.jpg *.jpeg *.png *.bmp")])
        
        if arquivo:
            self.imagem_original = cv.imread(arquivo)
            if self.imagem_original is None:
                messagebox.showerror("Erro", "Nao foi possivel carregar a imagem")
                return
            self.imagem_original = cv.cvtColor(self.imagem_original, cv.COLOR_BGR2RGB)
            self.limpar_selecoes()
            self.exibir_imagem(self.imagem_original)
            self.label_status.config(text=f"Imagem carregada: {arquivo}")
    
    def exibir_imagem(self, imagem):
        # Mostra imagem no canvas
        canvas_width = self.canvas.winfo_width() or 1000
        canvas_height = self.canvas.winfo_height() or 600
        
        altura_img, largura_img = imagem.shape[:2]
        escala_w = canvas_width / largura_img
        escala_h = canvas_height / altura_img
        self.escala = min(escala_w, escala_h, 1.0)
        
        nova_largura = int(largura_img * self.escala)
        nova_altura = int(altura_img * self.escala)
        imagem_redimensionada = cv.resize(imagem, (nova_largura, nova_altura))
        
        imagem_bgr = cv.cvtColor(imagem_redimensionada, cv.COLOR_RGB2BGR)
        sucesso, buffer = cv.imencode('.ppm', imagem_bgr)
        
        if sucesso:
            self.imagem_tk = tk.PhotoImage(data=buffer.tobytes())
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.imagem_tk)
            self.redesenhar_pontos()
    
    def clique_mouse(self, event):
        # Marca ponto de objeto ou fundo
        if self.imagem_original is None:
            return
        x_original = int(event.x / self.escala)
        y_original = int(event.y / self.escala)
        
        if self.modo_objeto.get() == 1:
            self.pontos_objeto.append((x_original, y_original))
            raio = 5
            self.canvas.create_oval(event.x - raio, event.y - raio, event.x + raio, event.y + raio, fill="green", outline="white", width=2, tags="ponto_objeto")
        else:
            self.pontos_fundo.append((x_original, y_original))
            raio = 5
            self.canvas.create_oval(event.x - raio, event.y - raio, event.x + raio, event.y + raio, fill="red", outline="white", width=2, tags="ponto_fundo")
        
        self.atualizar_status()
    
    def redesenhar_pontos(self):
        # Redesenha todos os pontos
        for x, y in self.pontos_objeto:
            x_canvas = int(x * self.escala)
            y_canvas = int(y * self.escala)
            raio = 5
            self.canvas.create_oval(x_canvas - raio, y_canvas - raio, x_canvas + raio, y_canvas + raio, fill="green", outline="white", width=2, tags="ponto_objeto")
        
        for x, y in self.pontos_fundo:
            x_canvas = int(x * self.escala)
            y_canvas = int(y * self.escala)
            raio = 5
            self.canvas.create_oval(x_canvas - raio, y_canvas - raio, x_canvas + raio, y_canvas + raio, fill="red", outline="white", width=2, tags="ponto_fundo")
    
    def limpar_selecoes(self):
        # Limpa todos os pontos
        self.pontos_objeto = []
        self.pontos_fundo = []
        self.canvas.delete("ponto_objeto")
        self.canvas.delete("ponto_fundo")
        self.atualizar_status()
    
    def processar_imagem(self):
        # Envia imagem e pontos para o controller
        if self.imagem_original is None:
            messagebox.showwarning("Aviso", "Carregue uma imagem primeiro")
            return
        if len(self.pontos_objeto) == 0 or len(self.pontos_fundo) == 0:
            messagebox.showwarning("Aviso", "Marque pelo menos um ponto de objeto e um de fundo")
            return
        self.label_status.config(text="Processando imagem...")
        self.root.update()
        self.controller.processar(self.imagem_original, self.pontos_objeto, self.pontos_fundo)
    
    def exibir_resultado(self, imagem_objeto, imagem_fundo, imagem_erosao, imagem_dilatacao):
        # Mostra janela com resultados
        self.imagem_objeto_resultado = imagem_objeto
        self.imagem_fundo_resultado = imagem_fundo
        self.imagem_erosao_resultado = imagem_erosao
        self.imagem_dilatacao_resultado = imagem_dilatacao
        
        janela_resultado = tk.Toplevel(self.root)
        janela_resultado.title("Resultados da Remocao de Fundo")
        janela_resultado.geometry("1400x900")
        
        # Frames para imagens
        frame_superior = tk.Frame(janela_resultado)
        frame_superior.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        frame_objeto = tk.Frame(frame_superior); frame_objeto.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        tk.Label(frame_objeto, text="Objeto Extraido", font=("Arial", 14, "bold")).pack()
        canvas_objeto = tk.Canvas(frame_objeto, bg="#bdc3c7"); canvas_objeto.pack(fill=tk.BOTH, expand=True)
        
        frame_fundo = tk.Frame(frame_superior); frame_fundo.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        tk.Label(frame_fundo, text="Fundo Extraido", font=("Arial", 14, "bold")).pack()
        canvas_fundo = tk.Canvas(frame_fundo, bg="#bdc3c7"); canvas_fundo.pack(fill=tk.BOTH, expand=True)
        
        frame_inferior = tk.Frame(janela_resultado); frame_inferior.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=5, pady=5)
        frame_erosao = tk.Frame(frame_inferior); frame_erosao.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        tk.Label(frame_erosao, text="Erosao", font=("Arial", 14, "bold")).pack()
        canvas_erosao = tk.Canvas(frame_erosao, bg="#bdc3c7"); canvas_erosao.pack(fill=tk.BOTH, expand=True)
        
        frame_dilatacao = tk.Frame(frame_inferior); frame_dilatacao.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        tk.Label(frame_dilatacao, text="Dilatacao", font=("Arial", 14, "bold")).pack()
        canvas_dilatacao = tk.Canvas(frame_dilatacao, bg="#bdc3c7"); canvas_dilatacao.pack(fill=tk.BOTH, expand=True)
        
        # Exibe imagens
        self.exibir_em_canvas(canvas_objeto, imagem_objeto)
        self.exibir_em_canvas(canvas_fundo, imagem_fundo)
        self.exibir_em_canvas(canvas_erosao, imagem_erosao)
        self.exibir_em_canvas(canvas_dilatacao, imagem_dilatacao)
        
        self.label_status.config(text="Processamento concluido!")
    
    def exibir_em_canvas(self, canvas, imagem):
        # Mostra imagem em canvas específico
        canvas.update()
        canvas_width = canvas.winfo_width() or 350
        canvas_height = canvas.winfo_height() or 400
        
        altura_img, largura_img = imagem.shape[:2]
        escala_w = canvas_width / largura_img
        escala_h = canvas_height / altura_img
        escala = min(escala_w, escala_h, 1.0)
        
        nova_largura = int(largura_img * escala)
        nova_altura = int(altura_img * escala)
        imagem_redimensionada = cv.resize(imagem, (nova_largura, nova_altura))
        
        imagem_bgr = cv.cvtColor(imagem_redimensionada, cv.COLOR_RGB2BGR)
        sucesso, buffer = cv.imencode('.ppm', imagem_bgr)
        
        if sucesso:
            imagem_tk = tk.PhotoImage(data=buffer.tobytes())
            canvas.imagem_tk = imagem_tk
            canvas.create_image(0, 0, anchor=tk.NW, image=imagem_tk)
    
    def salvar_resultados(self):
        # Salva imagens
        if self.imagem_objeto_resultado is None:
            messagebox.showwarning("Aviso", "Processe uma imagem primeiro")
            return
        
        for nome, img in [("Objeto", self.imagem_objeto_resultado), ("Fundo", self.imagem_fundo_resultado), ("Erosao", self.imagem_erosao_resultado), ("Dilatacao", self.imagem_dilatacao_resultado)]:
            arquivo = filedialog.asksaveasfilename(title=f"Salvar Imagem {nome}", defaultextension=".png", filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")])
            if arquivo:
                cv.imwrite(arquivo, cv.cvtColor(img, cv.COLOR_RGB2BGR))
        
        messagebox.showinfo("Sucesso", "Imagens salvas com sucesso!")
        self.label_status.config(text="Resultados salvos com sucesso!")
    
    def set_controller(self, controller):
        # Define controller
        self.controller = controller
    
    def run(self):
        # Inicia GUI
        self.root.mainloop()
