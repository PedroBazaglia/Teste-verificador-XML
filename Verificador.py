import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog
from tkinter.ttk import Progressbar
import xml.etree.ElementTree as ET
import threading

def obter_estrutura_servidor(elemento):
    estrutura = {}
    if elemento is not None:
        for atributo in elemento.attrib:
            estrutura[atributo] = None  # Definindo o valor como None
    return estrutura

def obter_nome_servidor(elemento):
    return elemento.attrib.get('nome', 'Nome não encontrado')  # Retorna o nome do servidor ou uma mensagem padrão se não for encontrado

def comparar_estrutura_servidores(modelo, producao , output_text, progress_bar):
    # Função para comparar a estrutura dos servidores
    output_text.insert(tk.END, "Comparando estrutura dos servidores...\n")
    output_text.insert(tk.END, "-----------------------------------------------------\n")
    output_text.update()


    tree_modelo = ET.parse(modelo)
    raiz_modelo = tree_modelo.getroot()

    encontrou_servidor_modelo = False
    for servidor_modelo in raiz_modelo.iter('servidor'):
        estrutura_modelo = obter_estrutura_servidor(servidor_modelo)
        encontrou_servidor_modelo = True

    if not encontrou_servidor_modelo:
        print("Tag <servidor> não encontrada no XML de modelo.")
        return

    tree_producao = ET.parse(producao)
    raiz_producao = tree_producao.getroot()

    for servidor_producao in raiz_producao.iter('servidor'):
        nome_servidor_producao = obter_nome_servidor(servidor_producao)
        estrutura_producao = obter_estrutura_servidor(servidor_producao)
        output_text.insert(tk.END, f"Comparando servidor '{nome_servidor_producao}': \n")
        for atributo in estrutura_modelo:
            if atributo not in estrutura_producao:
                output_text.insert(tk.END, f"Atributo '{atributo}' presente no modelo está ausente na produção. \n")
        for atributo in estrutura_producao:
            if atributo not in estrutura_modelo:
                output_text.insert(tk.END, f"Atributo '{atributo}' presente na produção está ausente no modelo. \n")

def selecionar_arquivo():
    arquivo_xml = filedialog.askopenfilename(title="Selecione o arquivo XML", filetypes=[("Arquivos XML", "*.xml")])
    return arquivo_xml

def comparar_arquivos(output_text, progress_bar):
    output_text.delete(1.0, tk.END)  # Limpar qualquer texto anterior
    arquivo_xml_modelo = selecionar_arquivo()
    if not arquivo_xml_modelo:
        return

    arquivo_xml_producao = selecionar_arquivo()
    if not arquivo_xml_producao:
        return

    # Iniciar uma thread para executar a comparação, permitindo que a interface gráfica permaneça responsiva
    threading.Thread(target=comparar_estrutura_servidores, args=(arquivo_xml_modelo, arquivo_xml_producao, output_text, progress_bar)).start()


def main():
    # Seleciona o arquivo XML de modelo
    arquivo_xml_modelo = selecionar_arquivo("Selecione o arquivo XML de Modelo")
    if not arquivo_xml_modelo:
        return

    # Seleciona o arquivo XML de produção
    arquivo_xml_producao = selecionar_arquivo("Selecione o arquivo XML de Produção")
    if not arquivo_xml_producao:
        return

    # Realiza a comparação entre os servidores dos XMLs
    comparar_estrutura_servidores(arquivo_xml_modelo, arquivo_xml_producao)

# Criar a janela principal
root = tk.Tk()
root.title("Comparador de Estrutura XML")

# Botão para iniciar a comparação
btn_comparar = tk.Button(root, text="Comparar Arquivos XML", command=lambda: comparar_arquivos(output_text, progress_bar))
btn_comparar.pack(pady=10)

# Widget de texto para exibir mensagens
output_text = tk.Text(root, wrap="word")
output_text.pack()

# Barra de progresso
progress_bar = Progressbar(root, orient=tk.HORIZONTAL, length=200, mode='indeterminate')
progress_bar.pack(pady=10)

# Iniciar o loop da interface gráfica
root.mainloop()