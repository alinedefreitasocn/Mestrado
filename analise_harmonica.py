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

# Tabela da Femar esta em centimetros
tide = Tide.decompose(df['nivel(cm)'], df.index.to_datetime())

# CONTRUINDO TABELA DAS CONSTANTES HARMONICAS
constituent = [c.name for c in tide.model['constituent']]
ddf = pd.DataFrame(tide.model, index=constituent).drop('constituent', axis=1)
ddf.sort('amplitude', ascending=False).head(10)
ddf.to_csv(path_or_buf=pathname + '\\constantes_harmonicas_cm.csv')

#############################################
# FORM NUMBER : CLASSIFICACAO DA MARE
print('Form number %s, the tide is %s.' %
      (tide.form_number()[0], tide.classify()))

dates = pd.date_range(start='2010-01-01', end='2011-12-31', freq='60T')
# determinar eixo temporal e freq.

hours = np.cumsum(np.r_[0, [t.total_seconds() / 3600.0
                            for t in np.diff(dates.to_pydatetime())]])

times = Tide._times(dates[0], hours)

# prediction = Series(tide.at(times) + nivel.mean(), index=dates)
# previsao da mare para o tempo dado
mare = pd.Series(tide.at(times) + df['nivel(cm)'].mean(), index=dates)


"***************************************************************************"
"*                                                                         *"
"*            LENDO O ARQUIVO DE PREVISAO DA MARINHA                       *"
"*                                                                         *"
"***************************************************************************"
filemare, pathmare = get_path('*')

"Lendo arquivo de mare"
# Juntando data em uma unica coluna
# Detalhe que o dataparse precisa do padrão %Y %m %d separado por espacos
# indicando que cada variavel esta em uma coluna diferente
dateparse = lambda x: pd.datetime.strptime(x, '%Y %m %d %H')
maremarinha = pd.read_csv(filemare,
                          sep=';',
                          header=0,
                          na_values='NaN',
                          parse_dates={'datahora': ['Ano', 'Mes', 'Dia',
                                                    'Hora']},
                          date_parser=dateparse,
                          squeeze=True,
                          index_col=0)
maremarinha2016 = maremarinha[maremarinha.index.year == 2016]

NM_marinha = 274.6   # CM
NM_serie = ddf.amplitude['Z0']  # CM
dif_NM = NM_serie - NM_marinha   # CM


# esse calculo da diferenca ta maluco....
#dif_mare = []
#for i in maremarinha2016.index:
#    m1 = mare.values[mare.index == i]
#    m2 = maremarinha2016.values[maremarinha2016.index == i]
#    d = abs(m1) - abs(m2)
#    dif_mare.append(d)
#plt.plot(dif_mare)
#plt.title('Dif Previsao Ttide e previsao Marinha')
#plt.ylabel(u'Diferença (cm)')
#plt.savefig(pathname + '\\difeenca_previsao.png')

# Tirando a media, as duas series ficam iguais!!! =)))
mare_sem_media = mare - mare.mean()
marinha_sem_media = maremarinha2016 - maremarinha2016.mean()

plt.figure(figsize=[15,6])
marinha_sem_media.plot(style='--', label='Previsao Marinha')
mare_sem_media.plot(style='o', label='Previsao Ttide')
plt.legend()
plt.ylim([-350, 350])
plt.title(u'Previsões around zero')
plt.ylabel(u'Amplitude de maré (cm)')
plt.savefig(pathname + '\\previsoes_sem_media2016.png')


fig = plt.figure(1)
# We define a fake subplot that is in fact only the plot.
plot = fig.add_subplot(111)
plot.tick_params(labelsize=14)
plt.ylabel('Water Level (m)', fontsize=14)




plt.figure(figsize=[15,6])
maremarinha2016.plot(label=u'Previsão Marinha')
mare.plot(label=u'Previsão Ttide')
plt.legend()
plt.ylim([-100, 1000])
plt.ylabel(u'Amplitude Maré (cm)')
plt.title(u'Previsões maré 2016')
plt.savefig(pathname + '\\previsoes2016.png')


#df['nivel(m)']=df['nivel(m)']-df['nivel(m)'].mean()
#df['tide']=df['tide']-df['tide'].mean()
#dd['filt_tide']=dd['nivel(m)']-dd['tide']
#
##fig2, ax2 = plt.subplots(figsize=(20, 10))
#fig2=plt.subplots(figsize=(20, 10))
#ax2=dd['nivel(m)'].plot(color='b',label='Observed data')
#ax2=dd['tide'].plot(color='r',label='Tide')
#ax2=dd['filt_tide'].plot(marker='*',color='k',linewidth=3,label='[data] - [tide]')
#ax2.legend(loc='best')
#fig.savefig(path+'ILHAFISCAL_2009_data_tide.png', dpi=100)
mare_sem_media = mare_sem_media/100

plt.figure()
mare_sem_media.plot()

plt.figure()
ax1 = plt.subplot(321)
plt.plot(mare_sem_media[mare_sem_media.index.day == 24])
ax1.set_xlim(['2017-07-24', '2017-07-25'])
ax1.set_ylim([-2.5, 2.5])
ax1.set_ylabel('Amplitude (m)')
ax1.set_xticks(pd.date_range(start='2017-07-24', end='2017-07-25', freq='30T'))
plt.setp(ax1.get_xticklabels(), visible=False)
ax1.set_title('24/07/2017', size=9)
ax1.grid()

ax3 = plt.subplot(323)
plt.plot(mare_sem_media[mare_sem_media.index.day == 25])
ax3.set_xlim(['2017-07-25', '2017-07-26'])
ax3.set_ylim([-2.5, 2.5])
ax3.set_ylabel('Amplitude (m)')
ax3.set_xticks(pd.date_range(start='2017-07-25', end='2017-07-26', freq='30T'))
plt.setp(ax3.get_xticklabels(), visible=False)
ax3.set_title('25/07/2017', size=9)
ax3.grid()

ax5 = plt.subplot(325)
plt.plot(mare_sem_media[mare_sem_media.index.day == 26])
plt.xlim(['2017-07-26', '2017-07-27'])
ax5.set_ylabel('Amplitude (m)')
ax5.set_ylim([-2.5, 2.5])
plt.setp(ax5.get_xticklabels(), visible=True)
ax5.set_xticks(pd.date_range(start='2017-07-26', end='2017-07-27', freq='30T'))
ax5.set_xticklabels(['0:00', ' ', ' ', ' ', ' ', ' ',
                     '3:00',  ' ', ' ', ' ', ' ', ' ',
                     '6:00', ' ', ' ', ' ', ' ', ' ',
                     '9:00', ' ', ' ', ' ', ' ', ' ',
                     '12:00',' ', ' ', ' ', ' ', ' ',
                     '15:00',  ' ', ' ', ' ', ' ', ' ',
                     '18:00', ' ', ' ', ' ', ' ', ' ',
                     '21:00',  ' ', ' ', ' ', ' ', ' ',
                    '24:00'], size=9)
ax5.set_title('26/07/2017', size=9)
ax5.grid()

ax2 = plt.subplot(322)
plt.plot(mare_sem_media[mare_sem_media.index.day == 27])
plt.xlim(['2017-07-27', '2017-07-28'])
ax2.set_ylim([-2.5, 2.5])
ax2.set_ylabel('Amplitude (m)')
ax2.set_xticks(pd.date_range(start='2017-07-27', end='2017-07-28', freq='30T'))
plt.setp(ax2.get_xticklabels(), visible=False)
ax2.set_title('27/07/2017', size=9)
ax2.grid()

ax4 = plt.subplot(324)
plt.plot(mare_sem_media[mare_sem_media.index.day == 28])
plt.xlim(['2017-07-28', '2017-07-29'])
ax4.set_ylim([-2.5, 2.5])
ax4.set_ylabel('Amplitude (m)')
ax4.set_xticks(pd.date_range(start='2017-07-28', end='2017-07-29', freq='30T'))
plt.setp(ax4.get_xticklabels(), visible=False)
ax4.set_title('28/07/2017', size=9)
plt.grid()

ax6 = plt.subplot(326)
plt.plot(mare_sem_media[mare_sem_media.index.day == 29])
plt.xlim(['2017-07-29', '2017-07-30'])
ax6.set_ylim([-2.5, 2.5])
ax6.set_ylabel('Amplitude (m)')
plt.setp(ax6.get_xticklabels(), visible=True)
ax6.set_xticks(pd.date_range(start='2017-07-29', end='2017-07-30', freq='30T'))
ax6.set_xticklabels(['0:00', ' ', ' ', ' ', ' ', ' ',
                     '3:00',  ' ', ' ', ' ', ' ', ' ',
                     '6:00', ' ', ' ', ' ', ' ', ' ',
                     '9:00', ' ', ' ', ' ', ' ', ' ',
                     '12:00',' ', ' ', ' ', ' ', ' ',
                     '15:00',  ' ', ' ', ' ', ' ', ' ',
                     '18:00', ' ', ' ', ' ', ' ', ' ',
                     '21:00',  ' ', ' ', ' ', ' ', ' ',
                    '24:00'], size=9)
ax6.set_title('29/07/2017', size=9)
plt.grid()



"***************************************************************************"
"*                                                                         *"
"*                  Previsao de mare para o periodo das                    *"
"*                     imagens de satelite (2013-2017)                     *"
"*                                                                         *"
"***************************************************************************"
#  As imagens sao de 13hrs (todo as vezes o satelite passa na mesma hora)
# porem esse horario esta em GMT. Logo, devemos subtrair

dates = pd.date_range(start='2013-01-01', end='2017-12-31', freq='60T')

# determinar eixo temporal e freq.

hours = np.cumsum(np.r_[0, [t.total_seconds() / 3600.0
                            for t in np.diff(dates.to_pydatetime())]])

times = Tide._times(dates[0], hours)

# prediction = Series(tide.at(times) + nivel.mean(), index=dates)
# previsao da mare para o tempo dado
mare = pd.Series(tide.at(times) + df['nivel(cm)'].mean(),
                 index=dates, name='nivel(cm)')

########################################################
# tirando o Nivel Referencia e passando para metros
######################################################
mare_NR = (mare - 334.140911172)/100
mare_NR.index = dates
mare_sm = mare - mare.mean()
mare_sm.index = dates

# pegando soh os valores as 13hrs
mare10hrs = mare[mare.index.hour == 10]
mare10hrs.to_csv(path=pathname + '\\mare_10hrs.csv')
# pegando todos os valores abaixo de zero
mare10hrs_negativo = mare10hrs[mare10hrs.values < 0]
mare10hrs_negativo.to_csv(path=pathname + '\\mare10horas_neg.csv')
mare_abaixo_125 = mare10hrs[mare10hrs.values < -125]
mare_abaixo_125.to_csv(path=pathname + '\\mare125.csv')
mare_abaixo_150 = mare10hrs[mare10hrs.values < -150]
mare_abaixo_150.to_csv(path=pathname + '\\mare150.csv')
mare_abaixo_160 = mare10hrs[mare10hrs.values < -160]
mare_abaixo_160.to_csv(path=pathname + '\\mare160.csv')
mare_abaixo_168 = mare10hrs[mare10hrs.values < -168]
mare_abaixo_168.to_csv(path=pathname + '\\mare168.csv')