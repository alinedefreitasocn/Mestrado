# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 13:09:57 2017

@author: Aline L

Aline, na verdade as rotinas são linhas de comando,...

O - para observação e
M - para resultado do modelo. 
Se tiver duvidas coloque o help [nome da funçao]
talvez seja mais fácil que tentar modificar ;)


S.Omean(ii,j) = nanmean(DM.(OPT.varname));
            S.Ostd(ii,j)  = nanstd(DM.(OPT.varname));

            S.Mmean(ii,j) = nanmean(model);
            S.Mstd(ii,j)  = nanstd(model);
            S.absuRMSE(ii,j) = sqrt(nanmean(((model-S.Mmean(ii,j))-(DM.(OPT.varname)-S.Omean(ii,j))).^2));
            S.uRMSE(ii,j) = sign(S.Mstd(ii,j)-S.Ostd(ii,j))*sqrt(nanmean(((model-S.Mmean(ii,j))-(DM.(OPT.varname)-S.Omean(ii,j))).^2));
            S.RMSE(ii,j)  = sqrt(nanmean((model-DM.(OPT.varname)).^2));
            S.R2(ii,j)    = ((nansum((model-S.Mmean(ii,j)).*(DM.(OPT.varname)-S.Omean(ii,j)))./(length(model)-1))/(S.Mstd(ii,j)*S.Ostd(ii,j)))^2;
            
            S.bias(ii,j)  = S.Mmean(ii,j)-S.Omean(ii,j);
"""

import pandas as pd
import numpy as np
import wx
import matplotlib.pyplot as plt

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



'''
            LENDO ARQUIVO DE PREVISAO
            PERIODO DE 01/07 A 31/07
''' 

filenamet, pathnamet = get_path('*')

"Lendo arquivo de mare"
# Juntando data em uma unica coluna
# Detalhe que o dataparse precisa do padrão %Y %m %d separado por espacos
# indicando que cada variavel esta em uma coluna diferente
ttide = pd.read_csv(filenamet,
                 delimiter=';',
                 header=None,
                 index_col=0,
                 names=['nivel(m)'])

ttide.index = pd.to_datetime(ttide.index)
ttide.index = ttide.index.tz_localize(tz='America/Fortaleza')

'''
            LENDO O RESULTADO DO MODELO
                  10 CM MAIS RASO
             PERIODO DE 01/07 A 31/07
''' 
filename10cm, pathnamem = get_path('*')

modelo10cm = pd.read_csv(filename10cm,
                         delimiter=';',
                         header=0,
                         index_col=0)

modelo10cm.index = pd.to_datetime(modelo10cm.index, dayfirst=True)
modelo10cm.index = modelo10cm.index.tz_localize(tz='utc')
modelo10cm.index = modelo10cm.index.tz_convert('America/Fortaleza')


'''
            LENDO O RESULTADO DO MODELO
                  50 CM MAIS RASO
             PERIODO DE 01/07 A 31/07
''' 
filename50cm, pathname50cm = get_path('*')

modelo50cm = pd.read_csv(filename50cm,
                         delimiter=';',
                         header=0,
                         index_col=0)

modelo50cm.index = pd.to_datetime(modelo50cm.index, dayfirst=True)
modelo50cm.index = modelo50cm.index.tz_localize(tz='utc')
modelo50cm.index = modelo50cm.index.tz_convert('America/Fortaleza')

plt.figure()
plt.plot(ttide, label=u'Previsão Ttide', style='.')
plt.plot(modelo10cm, label=u'Resultado do modelo - 10cm mais raso')
plt.plot(modelo50cm, label=u'Resultado do modelo - 50cm mais raso')




