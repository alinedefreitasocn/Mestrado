# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 17:32:12 2017
ANALISE DOS DADOS DE VENTO
Dados fornecidos pelo BNDO ja reescrito para o formato de
dados horarios por linha.

Adicionando uma coluna de direcao aos dados


@author: Aline Lemos de Freitas
email: alfreitas.ocn@gmail.com
"""
import pandas as pd
import wx
from pandas import Series, DataFrame, Panel

# Para selecionar o arquivo de analise
def get_path(wildcard):
    app = wx.App(None)
    style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
    dialog = wx.FileDialog(None, 'Open', wildcard=wildcard, style=style)
    if dialog.ShowModal() == wx.ID_OK:
        path = dialog.GetPath()
        direc = dialog.GetDirectory()
        # f = dialog.GetFilename()
    else:
        path = None
    dialog.Destroy()
    return path, direc

"*************************************************************"
"*                                                           *"
"*                 LEITURA DO ARQUIVO                        *"
"*                                                           *"
"*************************************************************"
# escolhendo o arquivo de entrada
print('ESCOLHA O ARQUIVO DO INMET')
filename, pathname = get_path('*')

"Lendo arquivo do INMET"
# Juntando data em uma unica coluna
# Detalhe que o dataparse precisa do padrão %Y %m %d separado por espacos
# indicando que cada variavel esta em uma coluna diferente
dados = pd.read_excel(filename, header=0, skipinitialspace=True,
                    na_values='NULL')
horas = range(24)
df = pd.DataFrame(columns = ['Data', 'Hora', 'Velvento', 'Ventodir'])
for i in dados.index:
    for j in horas:
        velvento = dados[dados.index == i]['velvento'+str(j)][0]
        ventodir = dados[dados.index == i]['ventodir'+str(j)][0]
        #l = [i, j, velvento, ventodir]
        df = df.append({"Data": i,
                        "Hora":  j,
                        "Velvento": velvento,
                        "Ventodir": ventodir
                        }, ignore_index=True)
        #dataframe.append(l)
df.to_csv(path_or_buf=pathname + '\\reescrito.csv')




"Fazendo para chuva tbm"
dados = pd.read_excel(filename, header=0, skipinitialspace=True,
                    na_values='NULL')
horas = range(24)
df = pd.DataFrame(columns = ['Data', 'Hora', 'chuva'])
for i in dados.index:
    for j in horas:
        chuva = dados[dados.index == i]['PRECIPITACAO'+str(j)][0]
        #l = [i, j, velvento, ventodir]
        df = df.append({"Data": i,
                        "Hora":  j,
                        "chuva": chuva,
                        }, ignore_index=True)
        #dataframe.append(l)
df.to_csv(path_or_buf=pathname + '\\reescrito_chuva.csv')