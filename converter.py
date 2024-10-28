# -*- coding: utf-8 -*-
import codecs
import Tkinter as tk
import tkMessageBox
import Tkinter as tk
import tkMessageBox
import subprocess


def transformar_codigo():
    codigo_python3 = text_area.get("1.0", tk.END).strip()

    if not codigo_python3:
        tkMessageBox.showwarning("Aviso", "Digite um código em Python 3.")
        return

    with codecs.open("codigo_python3.py", "w", encoding="utf-8") as file:
        file.write(codigo_python3)


    try:
        # Chamar um processo externo para fazer a conversão do código Python 3 para Python 2
        subprocess.call(["2to3", "-n", "-W", "-o", ".", "codigo_python3.py"])

        # Ler o código Python 2 convertido a partir do arquivo gerado pelo 2to3
        with open("codigo_python3.py", "r") as file:
            codigo_python2 = file.read()

        # Copiar o código Python 2 para a área de transferência
        root.clipboard_clear()
        root.clipboard_append(codigo_python2)
        root.update()

        tkMessageBox.showinfo("Sucesso", "Código transformado com sucesso!\n\nCódigo Python 2 copiado para a área de transferência.")
    except Exception as e:
        tkMessageBox.showerror("Erro", "Ocorreu um erro ao transformar o código:\n\n{}".format(str(e)))

    # Remover o arquivo temporário
    subprocess.call(["del", "codigo_python3.py"])


# Cria a janela principal
root = tk.Tk()
root.title("Conversor de Código Python 3 para Python 2")

# Cria a área de texto para digitar o código em Python 3
text_area = tk.Text(root, width=60, height=10)
text_area.pack(pady=10)

# Cria o botão "Transformar"
transform_button = tk.Button(root, text="Transformar", command=transformar_codigo)
transform_button.pack()

# Inicia o loop principal da aplicação
root.mainloop()

