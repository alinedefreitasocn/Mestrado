# -*- coding: utf-8 -*-
"""
Utilizando os dados enviados pela marinha para obter as constantes harmonicas
para Salinopolis.
O arquivo 20520000720101195530121955ALT contem a serie mais longa, com
aproximadamente um ano
"""
# Analise Harmonica Mare Salinopolis

import pandas as pd
import os
import wx
from pytides.tide import Tide #IMPORTAR PACOTE PYTIDE
# instalado com o pip install pytides
import matplotlib.pyplot as plt
import numpy as np

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


filename, pathname = get_path('*')

"Lendo arquivo de mare"
# Juntando data em uma unica coluna
# Detalhe que o dataparse precisa do padrão %Y %m %d separado por espacos
# indicando que cada variavel esta em uma coluna diferente
df = pd.read_csv(filename,
                 delimiter=';',
                 skiprows=11,
                 header=0,
                 usecols=[1],
                 index_col=0)

arqname = filename[filename.rfind('\\') + 1 : -4] # encontra o ultimo indice
# igual a \\

"""
####################################
HORARIO DOS DADOS: HORARIO PAPA

Wiki:
Para interlocutores, foi convencionada uma letra e um nome para cada
meridiano. O sistema pode funcionar mesmo em condições adversas de transmissão
de rádio. A letra J (Juliet), representa a hora do observador e a Linha
Internacional de data fica entre o M e o Y.
P	Papa	UTC − 3 horas
"""

# df['nivel(cm)'] = df['nivel(mm)']/10.   # passando para metros
# df['nivel(m)'] = df['nivel(mm)']/100.   # passando para metros
df['nivel(cm)'].plot()
plt.savefig(pathname + '\\' + arqname + '.png')

# removendo a media da serie
# df['nivel_0_(m)'] = df['nivel(m)'] - df['nivel(m)'].mean()
df['nivel(cm)'] = df['nivel(cm)'] - df['nivel(cm)'].mean()
df['nivel(m)'] = df['nivel(cm)']/100.

# Tabela da Femar esta em centimetros
tide = Tide.decompose(df['nivel(m)'], pd.to_datetime(df.index))

# CONTRUINDO TABELA DAS CONSTANTES HARMONICAS
constituent = [c.name for c in tide.model['constituent']]
ddf = pd.DataFrame(tide.model, index=constituent).drop('constituent', axis=1)
ddf.sort('amplitude', ascending=False).head(10)
ddf.to_csv(path_or_buf=pathname + '\\constantes_harmonicas_cm.csv')

#############################################
# FORM NUMBER : CLASSIFICACAO DA MARE
print('Form number %s, the tide is %s.' %
      (tide.form_number()[0], tide.classify()))

dates = pd.date_range(start='2011-07-01', end='2011-07-30', freq='60T')
# determinar eixo temporal e freq.

hours = np.cumsum(np.r_[0, [t.total_seconds() / 3600.0
                            for t in np.diff(dates.to_pydatetime())]])

times = Tide._times(dates[0], hours)

# prediction = Series(tide.at(times) + nivel.mean(), index=dates)
# previsao da mare para o tempo dado
mare = pd.Series(tide.at(times) + df['nivel(m)'].mean(), index=dates)
mare.index = mare.index.tz_localize(tz='America/Fortaleza')

"***************************************************************************"
"*                                                                         *"
"*            LENDO O ARQUIVO DE PREVISAO DA MARINHA                       *"
"*                                                                         *"
"***************************************************************************"
filemare, pathmare = get_path('*.csv')

"Lendo arquivo de mare"
# Juntando data em uma unica coluna
# Detalhe que o dataparse precisa do padrão %Y %m %d separado por espacos
# indicando que cada variavel esta em uma coluna diferente

maremodelo = pd.read_csv(filemare,
                          sep=';',
                          header=0,
                          na_values='NaN',
                          squeeze=True,
                          index_col=0)
maremodelo.index = pd.to_datetime(maremodelo.index, dayfirst=True)

# Dados defasados
maremodelo.index = maremodelo.index.tz_localize(tz='utc')
maremodelo.index = maremodelo.index.tz_convert('America/Fortaleza')

plt.figure(figsize=[15,6])
mare.plot(label=u'Previsão Ttide')
maremodelo.plot(label=u'Resultado Modelo')
plt.ylim([-4,4])
plt.legend()

plt.ylabel(u'Amplitude Maré (m)')
plt.title(u'Previsões maré 2016')
plt.savefig(pathname + '\\previsoes2016.png')


#
#mare_sem_media = mare_sem_media/100
#
#plt.figure()
#mare_sem_media.plot()
#
#plt.figure()
#ax1 = plt.subplot(321)
#plt.plot(mare_sem_media[mare_sem_media.index.day == 24])
#ax1.set_xlim(['2017-07-24', '2017-07-25'])
#ax1.set_ylim([-2.5, 2.5])
#ax1.set_ylabel('Amplitude (m)')
#ax1.set_xticks(pd.date_range(start='2017-07-24', end='2017-07-25', freq='30T'))
#plt.setp(ax1.get_xticklabels(), visible=False)
#ax1.set_title('24/07/2017', size=9)
#ax1.grid()
#
#ax3 = plt.subplot(323)
#plt.plot(mare_sem_media[mare_sem_media.index.day == 25])
#ax3.set_xlim(['2017-07-25', '2017-07-26'])
#ax3.set_ylim([-2.5, 2.5])
#ax3.set_ylabel('Amplitude (m)')
#ax3.set_xticks(pd.date_range(start='2017-07-25', end='2017-07-26', freq='30T'))
#plt.setp(ax3.get_xticklabels(), visible=False)
#ax3.set_title('25/07/2017', size=9)
#ax3.grid()
#
#ax5 = plt.subplot(325)
#plt.plot(mare_sem_media[mare_sem_media.index.day == 26])
#plt.xlim(['2017-07-26', '2017-07-27'])
#ax5.set_ylabel('Amplitude (m)')
#ax5.set_ylim([-2.5, 2.5])
#plt.setp(ax5.get_xticklabels(), visible=True)
#ax5.set_xticks(pd.date_range(start='2017-07-26', end='2017-07-27', freq='30T'))
#ax5.set_xticklabels(['0:00', ' ', ' ', ' ', ' ', ' ',
#                     '3:00',  ' ', ' ', ' ', ' ', ' ',
#                     '6:00', ' ', ' ', ' ', ' ', ' ',
#                     '9:00', ' ', ' ', ' ', ' ', ' ',
#                     '12:00',' ', ' ', ' ', ' ', ' ',
#                     '15:00',  ' ', ' ', ' ', ' ', ' ',
#                     '18:00', ' ', ' ', ' ', ' ', ' ',
#                     '21:00',  ' ', ' ', ' ', ' ', ' ',
#                    '24:00'], size=9)
#ax5.set_title('26/07/2017', size=9)
#ax5.grid()
#
#ax2 = plt.subplot(322)
#plt.plot(mare_sem_media[mare_sem_media.index.day == 27])
#plt.xlim(['2017-07-27', '2017-07-28'])
#ax2.set_ylim([-2.5, 2.5])
#ax2.set_ylabel('Amplitude (m)')
#ax2.set_xticks(pd.date_range(start='2017-07-27', end='2017-07-28', freq='30T'))
#plt.setp(ax2.get_xticklabels(), visible=False)
#ax2.set_title('27/07/2017', size=9)
#ax2.grid()
#
#ax4 = plt.subplot(324)
#plt.plot(mare_sem_media[mare_sem_media.index.day == 28])
#plt.xlim(['2017-07-28', '2017-07-29'])
#ax4.set_ylim([-2.5, 2.5])
#ax4.set_ylabel('Amplitude (m)')
#ax4.set_xticks(pd.date_range(start='2017-07-28', end='2017-07-29', freq='30T'))
#plt.setp(ax4.get_xticklabels(), visible=False)
#ax4.set_title('28/07/2017', size=9)
#plt.grid()
#
#ax6 = plt.subplot(326)
#plt.plot(mare_sem_media[mare_sem_media.index.day == 29])
#plt.xlim(['2017-07-29', '2017-07-30'])
#ax6.set_ylim([-2.5, 2.5])
#ax6.set_ylabel('Amplitude (m)')
#plt.setp(ax6.get_xticklabels(), visible=True)
#ax6.set_xticks(pd.date_range(start='2017-07-29', end='2017-07-30', freq='30T'))
#ax6.set_xticklabels(['0:00', ' ', ' ', ' ', ' ', ' ',
#                     '3:00',  ' ', ' ', ' ', ' ', ' ',
#                     '6:00', ' ', ' ', ' ', ' ', ' ',
#                     '9:00', ' ', ' ', ' ', ' ', ' ',
#                     '12:00',' ', ' ', ' ', ' ', ' ',
#                     '15:00',  ' ', ' ', ' ', ' ', ' ',
#                     '18:00', ' ', ' ', ' ', ' ', ' ',
#                     '21:00',  ' ', ' ', ' ', ' ', ' ',
#                    '24:00'], size=9)
#ax6.set_title('29/07/2017', size=9)
#plt.grid()
#
#
#
