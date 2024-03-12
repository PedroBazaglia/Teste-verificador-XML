import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog

def encontrar_linha_tag_servidor(arquivo_xml):
    with open(arquivo_xml, 'r') as arquivo:
        linhas = arquivo.readlines()
        for numero_linha, linha in enumerate(linhas, start=1):
            if '<servidor>' in linha:
                return numero_linha
    return None

def listar_elementos(elemento, resultado, caminho=''):
    # Adiciona o elemento à lista
    caminho_atual = caminho + '/' + elemento.tag
    resultado.append(caminho_atual)

    # Adiciona os atributos do elemento à lista
    atributos = elemento.attrib
    for atributo in atributos:
        resultado.append(f'{caminho_atual}/@{atributo}')

    # Recursivamente chama a função para cada filho
    for filho in elemento:
        listar_elementos(filho, resultado, caminho_atual)

def selecionar_arquivo(mensagem):
    root = tk.Tk()
    root.withdraw()  # Oculta a janela principal

    # Abre a janela de seleção de arquivo
    arquivo_xml = filedialog.askopenfilename(title=mensagem, filetypes=[("Arquivos XML", "*.xml")])

    if arquivo_xml:
        return arquivo_xml
    else:
        print("Nenhum arquivo selecionado.")
        return None

def comparar_documentos(arquivo_producao, arquivo_modelo):
    # Parseia os documentos XML
    tree_producao = ET.parse(arquivo_producao)
    raiz_producao = tree_producao.getroot()

    tree_modelo = ET.parse(arquivo_modelo)
    raiz_modelo = tree_modelo.getroot()

    # Lista os elementos de cada documento
    elementos_producao = []
    listar_elementos(raiz_producao, elementos_producao)

    elementos_modelo = []
    listar_elementos(raiz_modelo, elementos_modelo)

    # Compara os elementos e identifica os faltantes
    elementos_faltantes = set(elementos_modelo) - set(elementos_producao)

    # Se houver elementos faltantes, imprime-os
    if elementos_faltantes:
        print("Elementos faltantes no documento de produção:")
        for elemento in elementos_faltantes:
            print(elemento)
        
        # Encontra a linha onde a tag <servidor> está presente no arquivo de produção
        linha_servidor_producao = encontrar_linha_tag_servidor(arquivo_producao)
        if linha_servidor_producao:
            print(f"A tag 'servidor' está presente na linha {linha_servidor_producao} do arquivo de produção.")
    else:
        print("Nenhum elemento faltante encontrado.")

def main():
    # Seleciona o arquivo XML de produção
    arquivo_xml_producao = selecionar_arquivo("Selecione o arquivo XML de Produção")

    # Se um arquivo de produção for selecionado, prossiga
    if arquivo_xml_producao:
        # Seleciona o arquivo XML de modelo
        arquivo_xml_modelo = selecionar_arquivo("Selecione o arquivo XML de Modelo")

        # Se um arquivo de modelo for selecionado, prossiga
        if arquivo_xml_modelo:
            comparar_documentos(arquivo_xml_producao, arquivo_xml_modelo)

if __name__ == "__main__":
    main()