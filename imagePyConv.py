from PIL import Image
import pygame
import Tkinter as tk
import tkFileDialog
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def converter_imagem_png():
    # Abrir janela de seleção de arquivo
    root = tk.Tk()
    root.withdraw()
    caminho_arquivo = tkFileDialog.askopenfilename(filetypes=[("Imagens PNG", "*.png")])

    try:
        # Abrir a imagem PNG
        imagem = Image.open(caminho_arquivo)

        # Obter as dimensões da imagem
        largura, altura = imagem.size

        # Converter o caminho do arquivo para bytes usando a codificação correta
        caminho_bytes = caminho_arquivo.encode("utf-8")

        # Converter a imagem para um código Pygame ou Tkinter em Python 2
        codigo = "import pygame\n"
        codigo += "imagem = pygame.image.load('{}')".format(caminho_bytes)


        # Exibir informações da imagem
        print "Imagem convertida: {}".format(caminho_arquivo)
        print "Largura: {}px".format(largura)
        print "Altura: {}px".format(altura)
        print "Código gerado:"
        print codigo

        return codigo

    except IOError:
        print "Erro ao abrir a imagem: {}".format(caminho_arquivo)
        return None

codigo_gerado = converter_imagem_png()


