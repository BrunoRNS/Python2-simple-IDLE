# -*- coding: utf-8 -*-
import subprocess
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def atualizar_dependencias():
    subprocess.call(["pip", "install", "-U", "Pillow", "Pygments", "pygame", "psutil", "send2trash", "keyboard"])

def instalar_dependencias():
    subprocess.call(["pip", "install", "Pillow-6.2.2-cp27-cp27m-win32.whl", "Pygments", "pygame", "psutil", "send2trash", "keyboard"])

tentativas = 3  # Número máximo de tentativas
tentativa_atual = 1

while tentativa_atual <= tentativas:
    try:
        from distutils.core import setup
        import distutils.spawn
        import re
        import codecs
        import time
        import pygments.lexers
        from pygments.lexers import PythonLexer
        from pygments import highlight
        from pygments.formatters import TerminalFormatter
        import pygame
        import Tkinter as tk
        import ttk
        from PIL import Image, ImageTk, ImageDraw
        import os
        import tkSimpleDialog
        import tkMessageBox
        import tkFileDialog
        import shutil
        import tempfile
        import platform
        import psutil
        from send2trash import send2trash
        import keyboard


        # Se chegou até aqui, todas as importações foram bem-sucedidas
        break;

    except ImportError as e: 
        print("Error importing modules: ", str(e))
        instalar_dependencias()

    except ImportWarning as w:
        print("Warning importing modules: ", str(w))
        atualizar_dependencias()

    tentativa_atual += 1


encoding = 'utf-8'
# Pasta temporária para os arquivos do Cython
temp_folder = tempfile.mkdtemp()
python_lexer = PythonLexer()
nome_jogo = None
jogo_aberto = False


def recarregar_pagina():
   salvar_arquivos_jogo();
   root.destroy();
   subprocess.call(["python", "main.py"])

def detectar_combinacao_teclas(event=None):
    if keyboard.is_pressed('ctrl') and keyboard.is_pressed('shift'):
        # Pause de 1 a 3 segundos
        time.sleep(1)  # Aguarde 1 segundo
        while True:
          if keyboard.is_pressed('pause'):  # Verifique se a tecla pause está pressionada
             time.sleep(2)  # Aguarde mais 2 segundos
          else:
             if keyboard.is_pressed('v') and keyboard.is_pressed('f') and keyboard.is_pressed('b') and keyboard.is_pressed('c'):
                # Combinação de teclas detectada, chame a função de recarregar
                recarregar_pagina()
                break;
             else:
                return;


def destacar_sintaxe(event=None):
    global python_code_text
    codigo = python_code_text.get("1.0", tk.END)  # Obter o código do widget de texto

    # Limpar tags existentes
    python_code_text.tag_delete("syntax")
    python_code_text.tag_delete("error")

    palavras_chave = ["def", "if","break", "continue", "pass", "else", "elif", "type", "class", '(', ')', '*args', "**kwargs", 'try', 'except', 'as', '=', ':', '.', "'", '"']
    inicio = "1.0"
    while True:
        # Encontrar a próxima palavra
        inicio_palavra = python_code_text.search("\\b\\w+\\b", inicio, stopindex=tk.END, regexp=True)
        if not inicio_palavra:
            break
        
        # Obter a próxima palavra encontrada
        palavra = python_code_text.get(inicio_palavra, inicio_palavra + "+wordend")

        # Verificar a cor da palavra
        tag_name = "syntax"
        if palavra.startswith(("'", '"')):
            python_code_text.tag_configure("string_syntax", foreground="orange")
            tag_name = "string_syntax"
        elif re.match('^-?\\d+\\.?\\d*$', palavra):
            python_code_text.tag_configure("number_syntax", foreground="yellow")
            tag_name = "number_syntax"

        # Aplicar a tag na palavra encontrada
        python_code_text.tag_add(tag_name, inicio_palavra, inicio_palavra + "+%dc" % len(palavra))
        
        # Procurar a próxima palavra a partir do final da palavra atual
        inicio = inicio_palavra + "+%dc" % len(palavra)

    # Definir cores para as tags
    python_code_text.tag_configure("syntax", foreground="yellow green")
    python_code_text.tag_configure("error", background="red", foreground="white")

    
def tirar_espacos_inuteis(texto):
   caracteres_indesejados = ['\\ufeff', '´', '╗', '┐', '\\u00a8', '\\u2551', '\\u2550']
    
   for char in caracteres_indesejados:
        texto = texto.replace(char, '')
        
   return texto;
    


def exibir_informacoes():
    # Uso da CPU
    cpu_percent = psutil.cpu_percent()
    cpu_label.config(text="CPU: {}%".format(cpu_percent))

    # Verifica se nome_jogo está definido
    if nome_jogo:
        # Peso da pasta
        folder_size = get_folder_size(nome_jogo)
        folder_label.config(text="Game's folder size: {} bytes".format(folder_size))
    else:
        folder_label.config(text="Folder's size: N/A")

    # Atualiza as informações a cada 1 segundo
    root.after(1000, exibir_informacoes)


# Função para calcular o peso da pasta
def get_folder_size(folder):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size


def criar_jogo():
    global nome_jogo
    nome_jogo = tkSimpleDialog.askstring("Create game", "Whrite down the game's name:")
    if nome_jogo:
        path = os.path.join("C:\\", nome_jogo)
        print("Game's path: ", path) 
        try:
            os.makedirs(path);
        except OSError:
            tkMessageBox.showwarning("Game already existing", "The game folder already exists.");
            return


        main_code = "# main code: "

        with open(os.path.join(path, "main_{}.py".format(nome_jogo)), "w") as f:
            f.write(main_code)
        
        subprocess.Popen(["virtualenv", os.path.join(path, nome_jogo)])
        
        tkMessageBox.showinfo("Game created", "The game's files were created successfully")
        
        global jogo_aberto
        jogo_aberto = True

        atualizar_botao_salvar()
        
def executar_comando(codigo):
    global result_text
    tirar_espacos_inuteis(codigo)
    try:
        # Execute o código Python fornecido usando o interpretador Python
        processo = subprocess.Popen(['python', '-c', codigo], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        saida, erro = processo.communicate()
        result_text.insert(tk.END, saida)
        result_text.insert(tk.END, erro)
    except Exception as e:
        # Se ocorrer um erro, exiba a mensagem de erro no widget result_text
        result_text.insert(tk.END, "An error was found in your code:")
        result_text.insert(tk.END, str(e))
    finally:
        codigo = """
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
""" + codigo
        exec(codigo);

    result_text.see(tk.END)
    result_text.update()
    
def abrir_jogo():
    global jogo_aberto
    if os.listdir(temp_folder):
        # Alterar as permissões dos arquivos da pasta temp_folder para permitir a edição
        for root, dirs, files in os.walk(temp_folder):
            for file in files:
                file_path = os.path.join(root, file)
                os.chmod(file_path, 0o666)  # Permissões para leitura e escrita

    pasta_jogo = tkFileDialog.askdirectory(title="Open game")
    if pasta_jogo:
        global nome_jogo;
        nome_jogo = os.path.basename(pasta_jogo)
        print("Selected game: ", pasta_jogo)
        jogo_aberto = True
        atualizar_botao_salvar()
        atualizar_nome_jogo(nome_jogo)
    global python_code_text;
    caminho_arquivo = r"C:\\{}\\main_{}.py".format(nome_jogo, nome_jogo)
    with open(caminho_arquivo, "r") as arquivo:
       conteudo = arquivo.read()
    python_code_text.insert(tk.END, conteudo)


def sair_do_jogo():
    global temp_folder, jogo_aberto;
    
    if not jogo_aberto:
        tkMessageBox.showwarning("No game open", "There's no game to close.")
        return

    for root, dirs, files in os.walk(temp_folder):
        for file in files:
            file_path = os.path.join(root, file)
            os.chmod(file_path, 0o444)  # Permissões de leitura para o arquivo
            
    global nome_jogo;
    nome_jogo = None
    atualizar_nome_jogo(nome_jogo);
    jogo_aberto = False
    temp_folder = tempfile.mkdtemp()
    
    salvar_arquivos_jogo()
    fechar_jogo()
    tkMessageBox.showinfo("End Game", "Game successfully closed.")
    
    
def atualizar_botao_salvar():
    global nome_jogo, salvar_button;
    if nome_jogo:
        salvar_button.pack()
    else:
        salvar_button.pack_forget()


def salvar_arquivos_jogo():
    global nome_jogo;
    
    code = python_code_text.get("1.0", tk.END).strip()
    
    caminho_arquivo = "C:\\{}\\main_{}.py".format(nome_jogo, nome_jogo)
    
    with codecs.open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
       arquivo.write(code)
       tkMessageBox.showinfo("Saving...", "Game saved!")


def fechar_jogo():
    global jogo_aberto
    jogo_aberto = False
    global nome_jogo
    nome_jogo = None

def delete_jogo():
    pasta_jogo = tkFileDialog.askdirectory(title="Select the folder of the game to delete.")
    if pasta_jogo:
        try:
            lixeira_path = r"C:\$Recycle.Bin"  # Caminho para a pasta da lixeira no Windows
            shutil.move(pasta_jogo, lixeira_path)
            tkMessageBox.showinfo("Game deleted", "The game was deleted successfully")
        except Exception as e:
            tkMessageBox.showerror("Error deleting the game: ", str(e))

root = tk.Tk()
root.title("IDE for python games!!")

def verificar_dimensoes_tela():
    global largura_tela, altura_tela
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()

    # Agendando a próxima verificação após 1 segundo
    root.after(1000, verificar_dimensoes_tela)

# Define as dimensões da janela
verificar_dimensoes_tela()
largura = largura_tela 
altura = altura_tela 

frame = tk.Frame(root, width=largura, height=altura)
frame.place(x=0, y=0)

# Preenche a primeira metade do frame com a cor azul
blue_rectangle = tk.Canvas(frame, width=largura // 2, height=altura, bg="blue")
blue_rectangle.place(x=0, y=0, anchor="nw")

# Preenche a segunda metade do frame com a cor verde
green_rectangle = tk.Canvas(frame, width=largura // 2, height=altura, bg="green")
green_rectangle.place(x=largura // 2, y=0, anchor="nw")

# Cria um frame para os botões
botoes_frame = tk.Frame(root)
botoes_frame.pack(side=tk.TOP, pady=10)

nome_jogo_label = tk.Label(botoes_frame, text="Name of the game: {}".format(nome_jogo))
nome_jogo_label.pack(anchor="nw")

cpu_label = tk.Label(botoes_frame, text="CPU: ")
cpu_label.pack(anchor=tk.NE)

# Rótulo para exibir o peso da pasta
folder_label = tk.Label(botoes_frame, text="Game's folder size: ")
folder_label.pack(anchor=tk.NE)

def atualizar_nome_jogo(nome_jogo):
    nome_jogo_label.config(text="Name of the game: {}".format(nome_jogo))


atualizar_nome_jogo(nome_jogo)
exibir_informacoes()

criar_jogo_button = ttk.Button(botoes_frame, text="Create Game", style="RaisedButton.TButton", cursor="hand2", command=criar_jogo)
criar_jogo_button.pack(side=tk.LEFT, padx=10)

abrir_jogo_button = ttk.Button(botoes_frame, text="Open Game", style="RaisedButton.TButton", cursor="hand2", command=abrir_jogo)
abrir_jogo_button.pack(side=tk.LEFT, padx=10)

delete_button = ttk.Button(botoes_frame, text="Delete Game", style="RaisedButton.TButton", cursor="hand2", command=delete_jogo)
delete_button.pack(side=tk.LEFT, padx=10)

sair_jogo_button = ttk.Button(botoes_frame, text="Close Game", style="RaisedButton.TButton", cursor="hand2", command=sair_do_jogo)
sair_jogo_button.pack(side=tk.LEFT, padx=10)

salvar_button = ttk.Button(botoes_frame, text="Save Game", style="RaisedButton.TButton", cursor="hand2", command=salvar_arquivos_jogo)
salvar_button.pack(side=tk.LEFT, padx=10)

# Posiciona o notebook acima dos botões
notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True)

# Aba do código Python
python_code_tab = tk.Frame(notebook)
python_code_tab.configure(bg="black")
notebook.add(python_code_tab, text="Python Code")


# Aba do resultado
result_tab = tk.Frame(notebook)
result_tab.configure(bg="black")
notebook.add(result_tab, text="Result")

python_code_text = tk.Text(python_code_tab, width=80, height=25)
python_code_text.pack()


result_text = tk.Text(result_tab, width=80, height=25)
result_text.pack()


def run_python_code():
    global nome_jogo, jogo_aberto;
    
    if not jogo_aberto:
        tkMessageBox.showwarning("No game open", "No game is currently open.")
        return
        
    code = python_code_text.get("1.0", tk.END).strip()  # Obtenha o código do widget de texto e remova espaços em branco extras
    caminho_arquivo = "C:\\{}\\main_{}.py".format(nome_jogo, nome_jogo)

    with codecs.open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
       arquivo.write(code)
       
    executar_comando(code)

def open_image_to_code():
    try:
        subprocess.Popen(["python", "imagePyConv.py"], universal_newlines=True)
    except Exception as e:
        tkMessageBox.showerror("Error opening image to code", str(e))

def open_py3_to_py2():
    try:
        subprocess.Popen(["python", "converter.py"], universal_newlines=True)
    except Exception as e:
        tkMessageBox.showerror("Error opening conversor of Py3 to Py2", str(e))
        
image_to_code_tab = tk.Frame(notebook)
notebook.add(image_to_code_tab, text="Image to Code")

# Botão para abrir o programa de imagem para código
open_image_button = tk.Button(image_to_code_tab, text="Open Image to code", command=open_image_to_code)
open_image_button.pack()

# Aba para conversor Py3 para Py2
py3_to_py2_tab = tk.Frame(notebook)
notebook.add(py3_to_py2_tab, text="Py3 to Py2")

# Botão para abrir o programa de conversor Py3 para Py2
open_py3_to_py2_button = tk.Button(py3_to_py2_tab, text="Open Py3 to Py2", command=open_py3_to_py2)
open_py3_to_py2_button.pack()

python_run_button = tk.Button(python_code_tab, text="Run Python", command=run_python_code)
python_run_button.pack()


def exit_application():
    global running
    root.destroy()
    running = False
        


exit_tab = tk.Frame(notebook)
notebook.add(exit_tab, text="Exit")

exit_button = tk.Button(exit_tab, text="Exit", command=exit_application)
exit_button.pack()

running = True

while running:
    destacar_sintaxe()
    detectar_combinacao_teclas()
    root.update()

root.mainloop()
