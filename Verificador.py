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

def obter_matricula_servidor(elemento):
    return elemento.attrib.get('matricula', 'Matricula não encontrada')  # Retorna o nome do servidor ou uma mensagem padrão se não for encontrado

def comparar_estrutura_servidores(modelo, producao, output_text, progress_bar, label_erros):

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

    total_servidores_producao = len(list(raiz_producao.iter('servidor')))
    progresso = 0
    total_erros = 0  # Contador para o número total de erros encontrados

    for servidor_producao in raiz_producao.iter('servidor'):
        nome_servidor_producao = obter_nome_servidor(servidor_producao)
        matricula_servidor_producao = obter_matricula_servidor(servidor_producao)
        estrutura_producao = obter_estrutura_servidor(servidor_producao)
        num_erros_servidor = 0  # Contador para o número de erros para o servidor atual
        output_text.insert(tk.END, f"Servidor '{nome_servidor_producao}' '{matricula_servidor_producao}': \n")
        for atributo in estrutura_modelo:
            if atributo not in estrutura_producao:
                output_text.insert(tk.END, f"Atributo '{atributo}' presente no modelo está ausente na produção. \n")
                num_erros_servidor += 1
        for atributo in estrutura_producao:
            if atributo not in estrutura_modelo:
                output_text.insert(tk.END, f"Atributo '{atributo}' presente na produção está ausente no modelo. \n")
                num_erros_servidor += 1
        if num_erros_servidor > 0:
            output_text.insert(tk.END, "-----------------------------------------------------\n")
            total_erros += 1
        else:
            # Se não houver erros para este servidor, remova a última linha em branco
            output_text.delete("end-2l", tk.END)
            output_text.insert(tk.END, "\n")  # Adicione uma nova linha


        # Atualizar o valor da barra de progresso
        progresso += 100 / total_servidores_producao
        progress_bar['value'] = progresso
        root.update_idletasks()  # Atualizar a interface gráfica para refletir a mudança
    
    # Definir o valor da barra de progresso como 100 após a conclusão da comparação
    progress_bar['value'] = 100

    # Exibir o total de erros encontrados
    label_erros.config(text=f"Total de erros: {total_erros}")

def selecionar_arquivo():
    arquivo_xml = filedialog.askopenfilename(title="Selecione o arquivo XML", filetypes=[("Arquivos XML", "*.xml")])
    return arquivo_xml

def comparar_arquivos(output_text, progress_bar, label_erros):
    output_text.delete(1.0, tk.END)  # Limpar qualquer texto anterior
    arquivo_xml_modelo = "conf/modelo.xml"
    if not arquivo_xml_modelo:
        return

    arquivo_xml_producao = selecionar_arquivo()
    if not arquivo_xml_producao:
        return

     # Definir o valor inicial da barra de progresso como 0
    progress_bar['value'] = 0
    root.update_idletasks()  # Atualizar a interface gráfica para refletir a mudança

    # Iniciar uma thread para executar a comparação, permitindo que a interface gráfica permaneça responsiva
    threading.Thread(target=comparar_estrutura_servidores, args=(arquivo_xml_modelo, arquivo_xml_producao, output_text, progress_bar, label_erros)).start()

# Criar a janela principal
root = tk.Tk()
root.title("Comparador de Estrutura XML")

# Botão para iniciar a comparação
btn_comparar = tk.Button(root, text="Comparar Arquivos XML", command=lambda: comparar_arquivos(output_text, progress_bar, label_erros))
btn_comparar.pack(pady=10)

# Criar uma frame para conter a caixa de texto e a barra de rolagem
frame_texto = tk.Frame(root)
frame_texto.pack(fill="both", expand=True)

# Widget de texto para exibir mensagens
output_text = tk.Text(frame_texto, width='100')
output_text.pack(side="left", fill="both", expand=True)

# Criar uma barra de rolagem vertical
scrollbar = tk.Scrollbar(frame_texto, orient="vertical", command=output_text.yview)
scrollbar.pack(side="right", fill="y")

# Vincular a barra de rolagem ao widget de texto
output_text.config(yscrollcommand=scrollbar.set)

# Criar uma frame para conter a caixa de texto e a barra de rolagem
frame_Status = tk.Frame(root)
frame_Status.pack(fill="both", expand=True)

# Barra de progresso
progress_bar = Progressbar(frame_Status, orient=tk.HORIZONTAL, length=200, mode='determinate')

# Label para exibir o total de erros
label_erros = tk.Label(frame_Status, text="Total de erros: 0")
label_erros.pack()

progress_bar.pack(pady=10)

# Iniciar o loop da interface gráfica
root.mainloop()