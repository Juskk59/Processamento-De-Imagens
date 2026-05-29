# Processamento de Imagens — Remoção de Fundo com K-means

Projeto acadêmico desenvolvido em **Python** com o objetivo de aplicar conceitos de **processamento digital de imagens** e **segmentação visual**.

A aplicação permite carregar uma imagem, selecionar manualmente pontos pertencentes ao objeto principal e ao fundo, e então realizar a separação entre ambos utilizando o algoritmo **K-means**. Após a segmentação, o sistema também gera variações utilizando operações morfológicas de **erosão** e **dilatação**.

## Funcionalidades

- Carregamento de imagens nos formatos JPG, JPEG, PNG e BMP;
- Interface gráfica para seleção dos pontos do objeto e do fundo;
- Marcação visual dos pontos selecionados;
- Segmentação da imagem utilizando **K-means**;
- Remoção e separação do fundo da imagem;
- Extração isolada do objeto principal;
- Aplicação de **erosão** para redução das bordas do objeto;
- Aplicação de **dilatação** para expansão das bordas do objeto;
- Visualização dos resultados em uma nova janela;
- Exportação das imagens processadas em PNG ou JPEG.

## Como funciona

O processamento é realizado em etapas:

1. A imagem é carregada pela interface.
2. O usuário marca pontos correspondentes ao **objeto** e ao **fundo**.
3. Caso necessário, a imagem é redimensionada para facilitar o processamento.
4. O algoritmo **K-means** agrupa os pixels da imagem por similaridade de cor.
5. Os pontos selecionados identificam quais grupos pertencem ao objeto e quais pertencem ao fundo.
6. Uma máscara binária é criada para separar o elemento principal do restante da imagem.
7. A máscara é refinada utilizando operações morfológicas.
8. O sistema gera os resultados finais:
   - Objeto extraído;
   - Fundo extraído;
   - Resultado com erosão;
   - Resultado com dilatação.

## Tecnologias utilizadas

- **Python**
- **Tkinter** — interface gráfica
- **OpenCV** — manipulação e processamento de imagens
- **NumPy** — operações com matrizes e pixels
- **Scikit-learn** — aplicação do algoritmo K-means

## Arquitetura do projeto

O projeto foi organizado utilizando o padrão **MVC (Model-View-Controller)** e uma cadeia de etapas responsáveis pelo processamento da imagem.

```text
Processamento-De-Imagens/
├── main.py          # Inicialização da aplicação
├── controller.py    # Comunicação entre interface e processamento
├── model.py         # Organização do fluxo de processamento
├── view.py          # Interface gráfica da aplicação
├── elo.py           # Classe base da cadeia de processamento
├── elo_01.py        # Redimensionamento da imagem
├── elo_02.py        # Segmentação utilizando K-means
├── elo_03.py        # Criação da máscara de objeto e fundo
├── elo_04.py        # Refinamento com erosão e dilatação
├── elo_05.py        # Separação final do objeto e do fundo
└── imgs/            # Imagens utilizadas no projeto
```

## Pré-requisitos

Antes de executar o projeto, é necessário possuir o **Python 3** instalado.

Instale as dependências necessárias:

```bash
pip install opencv-python numpy scikit-learn
```

> O Tkinter normalmente já acompanha a instalação padrão do Python. Caso não esteja disponível no sistema, será necessário instalá-lo separadamente.

## Como executar

Clone o repositório:

```bash
git clone https://github.com/Juskk59/Processamento-De-Imagens.git
```

Acesse a pasta do projeto:

```bash
cd Processamento-De-Imagens
```

Execute a aplicação:

```bash
python main.py
```

## Como utilizar

1. Clique em **Carregar Imagem** e selecione uma imagem do computador.
2. Utilize o modo **Marcar Objeto** para selecionar pontos pertencentes ao item que deseja preservar.
3. Utilize o modo **Marcar Fundo** para selecionar pontos pertencentes ao fundo da imagem.
4. Clique em **Processar Imagem**.
5. Visualize os resultados gerados:
   - Objeto extraído;
   - Fundo extraído;
   - Erosão;
   - Dilatação.
6. Clique em **Salvar Resultados** para exportar as imagens processadas.

## Conceitos aplicados

### Segmentação com K-means

O algoritmo K-means agrupa pixels com cores semelhantes em diferentes clusters. A partir dos pontos definidos manualmente pelo usuário, o sistema identifica quais agrupamentos representam o objeto principal e quais representam o fundo.

### Erosão

A erosão reduz as regiões brancas da máscara, diminuindo visualmente as bordas do objeto. Essa operação pode ser utilizada para remover pequenas imperfeições ou ruídos externos.

### Dilatação

A dilatação amplia as regiões brancas da máscara, expandindo as bordas do objeto. Essa operação pode ajudar a recuperar pequenas áreas que não foram completamente selecionadas na segmentação.

## Objetivo acadêmico

Este projeto foi desenvolvido como atividade acadêmica para explorar técnicas fundamentais de processamento de imagens, incluindo:

- Segmentação por agrupamento de cores;
- Construção e refinamento de máscaras;
- Operações morfológicas;
- Extração de objetos e remoção de fundo;
- Desenvolvimento de uma interface gráfica para interação com o processamento.

## Autor

Desenvolvido por **Julio** como projeto acadêmico de processamento de imagens.
