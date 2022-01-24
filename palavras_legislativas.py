# Autor: João Sbaino
# Data: 24 Jan 2022

# Bibliotecas necessárias
from PyPDF2 import PdfFileReader as pfr
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np
import os



cwd = os.getcwd()
directorio = os.path.join(cwd, 'programas')


partidos = {'PS': 'Programa-Eleitoral-PS2022.pdf',
            'PSD': 'PSD Programa Eleitoral 2022 v4.pdf',
            'BE': 'Programa-sem-fotos-versão-impressao.pdf',
            'CDU': '2019_programa_eleitoral_pcp.pdf', 
            'CHG': 'PROGRAMA-POLÍTICO-CHEGA-2021.pdf',
            'IL': 'Iniciativa-Liberal-Programa-Eleitoral-2022.pdf',
            'CDS': 'programaeleitoral_legislativascds19.pdf',
            'PAN': 'PAN-Programa-Eleitoral-Legislativas-2022-2.pdf',
            'LVR': 'Programa_Eleitoral_2022.pdf'}

# Variável que aramazena as listas de palavras de cada partido
contagens = []

# Palavras mais comuns que não vão ser contabilizadas para a lista ou caractéres indesesjado
palavras_comuns = ['a', 'ante', 'após', 'até', 'com', 'contra', 'de', 
                   'desde', 'em', 'entre', 'para', 'perante', 'por' , 
                   'segundo', 'sem', 'sob', 'sobre', 'tras', 'como', 
                   'que', 'o', 'a', 'os', 'as', 'qual', 'quem', 'é', 
                   'está', 'onde', 'um', 'uma', 'onde', 'e', 'do', 'da', 
                   'dos', 'das', 'no', 'na', 'nos', 'nas', 'mais', 'ł', 
                   'à', 'às', 'ser', 'ou', 'sua', 'são', 'estão', 'não', 
                   'pelo', 'pela', 'ao', 'aos', 'se', 'forma', 'esta', 
                   'este', 'mas', 'através', 'também', 'bem', 'num', 'às', 'tem', 'maior', '-do', '-', 
                   'œ', '˛', '[]', '˙', '˚']

# Caractéres a remover
especiais = ['.', ',', ';', '?', '!', '(', ')', '%', '"', ':', '-ção']


# Número de palavras para a lista de cada partido
n_palavras = 10


# Armazena os programas eleitorais que foram lidos correctamente
bem_processado = []

# Processamento dos programas eleitorais
for partido in partidos:
    
    try:
        print('Tentando ler o ficheiro')
        # programa = directorio + partido + '/' + partidos[partido]        
        programa = os.path.join(directorio, partido, partidos[partido])
        print(programa + '...')
        
        pdf = pfr(programa)

    except Exception as excep:
        print('ERRO: ' + str(excep))
        print('Saltando para o proximo...')
        continue

    print('... Concluído! A processar...')
    num_pgs = pdf.getNumPages()

    texto = []
    # Preparação da contagem de palavras
    for ii in range(0, num_pgs):

        pg = pdf.getPage(ii)

        # Extrai o texto de cada página
        texto.append(pg.extractText())

    # Junta as strings todas numa só, separadas por espaços
    texto = ' '.join(texto)

    # Letras todas minúsculas, para país e País não serem palavras diferentes
    texto = texto.lower()

    # Remove caractéres especiais
    for simb in especiais:
        texto = texto.replace(simb, '')

    # Separa as linhas
    linhas = texto.splitlines()

    # Separa cada linha em palavras individuais
    palavras = []
    for frase in linhas:
        palavras.append(frase.split(' '))


    # Contagem de palavras
    contagem = Counter([p for palavra in palavras for p in palavra])

    # Limpa empty strings e palavras comuns
    del contagem['']

    for comum in palavras_comuns:
        try:
            del contagem[comum]
        except:    
            print('Palavra não encontrada, saltando para a próxima...')
            continue

    contagens.append(contagem)

    bem_processado.append(partido)



##############################
#--- Criação de gráficos --- #
##############################

cores = [(224./255, 31./255, 41./255), (240./255, 138./255, 0), (225./255, 10./255, 23./255),
         (0./255, 70./255, 142./255), (36./255, 34./255, 83./255), (0./255, 174./255, 239./255), 
         (0, 0.54, 0.83), (9./255, 100./255, 128./255), (163./255, 199./255, 96./255)]

zooming = [0.30, 0.1, 0.35, 0.25, 0.35, 0.35, 0.25, 0.13, 0.33]
y_pos = [0.75, 0.8, 0.85, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75]

#--- Gráficos individuais

for idx, cnt in enumerate(contagens):

    fig, ax = plt.subplots(figsize=(8.45, 8.45))


    # Logo do partido
    logo = directorio + '/' + bem_processado[idx] + '/' + 'logo' + bem_processado[idx] + '.png'
    img = mpimg.imread(logo)   


    mais_comuns = cnt.most_common(n_palavras)
    xx = []
    yy = []

    for par, val in mais_comuns:
        xx.append(par)
        yy.append(val)
    
    bar_plot = plt.bar(xx, yy, color = cores[idx])#
    plt.xticks([])

    def autolabel(rects):
        height_word = 0.02*rects.get_children()[0].get_height()
        for ii,rect in enumerate(bar_plot):
            
            ax.text(rect.get_x() + rect.get_width()/2., height_word,
                 xx[ii],
                 ha='center', va='bottom', rotation=90, c=(1., 1, 1.), weight='bold', fontsize='xx-large')

    autolabel(bar_plot)


    imagebox = OffsetImage(img, zoom=zooming[idx])
    ab = AnnotationBbox(imagebox, (.75, y_pos[idx]), frameon=False, xycoords='axes fraction')
    ax.add_artist(ab)

    plt.xticks(rotation=60)

    N = 5
    max_vals = list(range(0, 1000, 50))
    ymax = np.float64(yy[0])
    max_ind = np.where(max_vals >= ymax)[0]
    
    custom_ticks = np.linspace(0, max_vals[max_ind[0]], N, dtype=int)

    ax.set_yticks(custom_ticks)
    ax.set_yticklabels(custom_ticks)
    
    plt.ylabel('Número de palavras', size='xx-large')
    fig.tight_layout()

    fig_name = 'contagens_' + bem_processado[idx] + '.png'
    save_name = os.path.join(directorio[:-10], fig_name)
    plt.savefig(save_name)
    




