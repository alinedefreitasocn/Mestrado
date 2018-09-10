# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 17:32:12 2017
ANALISE DOS DADOS DE VENTO PARA
ESTACAO SALINOPOLIS - INMET
@author: Aline Lemos de Freitas
alfreitas.ocn@gmail.com
"""
import pandas as pd
import numpy as np
import wx
from pandas import Series, DataFrame, Panel
#import datetime
import matplotlib.pyplot as plt
from windrose import WindroseAxes
import matplotlib as mpl
#import os
from matplotlib import colors as mcolors
from collections import OrderedDict
import seaborn as sns


# A quick way to create new windrose axes #,radialaxis='%'
def new_axes():
    fig = plt.figure(figsize=(13, 8), dpi=80, facecolor='w', edgecolor='w')
    rect = [0.1, 0.1, 0.8, 0.8]
    ax = WindroseAxes(fig, rect, axisbg='w')
    fig.add_axes(ax)
    return ax


# ...and adjust the legend box
def set_legend(ax):
    l = ax.legend(borderaxespad=-0.10, bbox_to_anchor=[-0.1, 0.5],
                  loc='centerleft', title="m/s")
    plt.setp(l.get_texts(), fontsize=20)


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


#label_size = 18
#fontsize = 16

mpl.rcParams['xtick.labelsize'] = 18
mpl.rcParams['ytick.labelsize'] = 18
fontsize = 18
figsize = [13, 6]
label_size = 18

meses_label = OrderedDict([('Jan', 1), ('Fev', 2), ('Mar', 3),
                           ('Abr', 4), ('Mai', 5), ('Jun', 6),
                           ('Jul', 7), ('Ago', 8), ('Set', 9),
                           ('Out', 10), ('Nov', 11), ('Dez', 12)])

months_label = OrderedDict([('Jan', 1), ('Feb', 2), ('Mar', 3),
                           ('Apr', 4), ('May', 5), ('Jun', 6),
                           ('Jul', 7), ('Aug', 8), ('Sep', 9),
                           ('Oct', 10), ('Nov', 11), ('Dec', 12)])

index = np.arange(2,13,2)
cores = sns.color_palette(palette="viridis", n_colors=15)
esquema_cores2 = sns.color_palette("husl", 8)
esquema_cores3 = sns.cubehelix_palette(8, start=.5, rot=-.60)
esq4 = ['#666666', '#a6761d', '#66a61e', '#7570b3',
        '#e7298a', '#e6ab02', '#d95f02', '#1d9e99']
esq5 = ['#B2D430', '#476268', '#FFC30F', '#B31E6F',
         '#EE5A5A', '#22EAAA', '#E20049',
        '#F79F24']
esq6 = ['#3694A1', '#86712D', '#CCAC66', '#94DB9B',
         '#FFD1DF', '#9FAADF', '#D47DCE', '#B03B8F']
esquema_cores5 = sns.color_palette(esq6)

"*************************************************************"
"*                                                           *"
"*                 LEITURA DO ARQUIVO                        *"
"*                                                           *"
"*************************************************************"
# escolhendo o arquivo de entrada
print('ESCOLHA O ARQUIVO DE VENTO REESCRITO DO INMET')
filename, pathname = get_path('reescrito*.csv')

"Lendo arquivo do INMET"
# Juntando data em uma unica coluna
# Detalhe que o dataparse precisa do padrão %Y %m %d separado por espacos
# indicando que cada variavel esta em uma coluna diferente
dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
dados = pd.read_csv(filename, sep=',',
                    header=0,
                    na_values='NaN',
                    parse_dates=['datahora'],
                    date_parser=dateparse,
                    squeeze=True,
                    index_col=0)
"""
Corrigindo o horario de UTC para local nos dados horarios do INMET
Although GMT and UTC share the same current time in practice,
there is a basic difference between the two:
GMT is a time zone officially used in some European and African
countries. The time can be displayed using both the 24-hour format
(0 - 24) or the 12-hour format (1 - 12 am/pm).
UTC is not a time zone, but a time standard that is the basis for
civil time and time zones worldwide. This means that no country or
territory officially uses UTC as a local time.
"""
dados.index = dados.index.tz_localize(tz='utc')
dados.index = dados.index.tz_convert('America/Fortaleza')

knots = dados.Velvento * 1.94384
dados['knots'] = knots


"*************************************************************"
"*                                                           *"
"*                 SERIE COMPLETA VENTO                      *"
"*                                                           *"
"*************************************************************"

#if grafico == 1:


fig, [ax1, ax2] = plt.subplots(2,1, figsize=[13, 6])

ax1.plot(dados.Velvento, label='Intensidade', color=cores[1])
ax1.set_ylabel(u'Velocidade do vento (m/s)', size=fontsize-2)
ax2.plot(dados.Ventodir, color=cores[7], label=u'Direção')
ax2.yaxis.tick_right()
ax2.yaxis.set_label_position("right")
ax2.set_ylabel(u'Direção do vento (graus)', size=fontsize-2)
ax2.tick_params('y')
ax2.set_xlabel('Dias', size=fontsize-2)


"****************************************************************************"
"*                                                                          *"
"*        separando periodos seco, chuvoso e de transicao                   *"
"*                  de acordo com o grafico da ANA                          *"
"*                                                                          *"
"****************************************************************************"
"Meses de chuva de jan a mai"
periodo_chuvoso = dados[dados.index.month < 6]

"Meses de Transicao (Jun, Jul e Dez)"
periodo_transicao = dados[dados.index.month == 6]
periodo_transicao = periodo_transicao.append(dados
                                             [dados.index.month == 7])
periodo_transicao = periodo_transicao.append(dados
                                             [dados.index.month == 12])

"Meses secos de Ago a Nov"
periodo_seco = pd.DataFrame()
for i in np.arange(8, 12, 1):
    pmes = dados[dados.index.month == i]
    periodo_seco = periodo_seco.append(pmes)

"*************************************************************"
"*                                                           *"
"*                 ANALISE VENTO                             *"
"*          MEDIAS MENSAIS INTENSIDADE                       *"
"*                                                           *"
"*************************************************************"
media_vento_mensal = dados.groupby(dados.index.month).mean()
std_vento_mensal = dados.groupby(dados.index.month).std()
quantil10_vento = dados.groupby(dados.index.month).quantile(q=0.10)
quantil25_vento = dados.groupby(dados.index.month).quantile(q=0.25)
quantil75_vento = dados.groupby(dados.index.month).quantile(q=0.75)
quantil90_vento = dados.groupby(dados.index.month).quantile(q=0.90)

"Plotando figuras"

plt.plot(media_vento_mensal.Velvento, color= cores[7], alpha=0.8)
plt.fill_between(x=media_vento_mensal.index, y1=quantil10_vento.Velvento,
                 y2=quantil90_vento.Velvento, interpolate=True,
                 color=cores[8], linestyle='--', alpha=0.3) #'#b1c4dd',
plt.fill_between(x=media_vento_mensal.index, y1=quantil25_vento.Velvento,
                 y2=quantil75_vento.Velvento, interpolate=True,
                 color=cores[8], linestyle='--', alpha=0.6) #'#95b5df'
#plt.title(u'Intensidade do vento')
plt.xlabel(u'', size=fontsize)
plt.xticks(index, ('Feb', 'Apr', 'Jun', 'Aug','Oct', 'Dec'), size=fontsize)
plt.ylabel('Wind speed (m/s)', size=fontsize)
plt.ylim([0,6])
plt.xlim([1,12])
plt.savefig(pathname + '\\ingles_media_int_vento_mensal.png', format='png', dpi=1200)


"*************************************************************"
"*                                                           *"
"*             SEPARANDO DADOS POR DIRECAO                   *"
"*      E CALCULANDO A DISTRIBUICAO DE FREQUENCIA            *"
"*                   POR HORA DO DIA                         *"
"*                                                           *"
"*************************************************************"
#==============================================================================
# gera uma variavel com index duplo. O primeiro eh a hora e o segundo a direcao
direcao_count_hora = dados.groupby([dados.index.hour,
                                         'Direcao']).size()
# transforma num dataframe 2D com as horas nas linhas e as
# direcoes nas colunas
direcao_freq_hora = direcao_count_hora.unstack(level = 0)
# divide cada contagem de direcao pela contagem de pontos
# naquela hora
direcao_freq_hora = direcao_freq_hora/direcao_freq_hora.sum()
direcao_freq_hora.to_csv(path_or_buf=pathname + '\\frequencia_direcao_hora.csv')
direcao_freq_hora = direcao_freq_hora.transpose()


ax = direcao_freq_hora.plot(kind = 'bar',
                            rot = True,
                            stacked = True,
                            color=(esquema_cores5),
                            figsize=figsize)
#fig.set_size_inches(figsize)
ax.legend(loc='upper center',
            ncol=8,
            bbox_to_anchor=(0.5, 1.1),
            fancybox=True,
            fontsize=fontsize-4)
ax.set_ylim([0,1])
ax.set_yticklabels([0, 20, 40, 60, 80, 100])
ax.set_ylabel(u'Frequency (%)', size=18)
ax.set_xlabel(u'Hours', size=18)
plt.savefig(pathname + '\\ingles_frequencia_direcao.png',
            format='png',
            dpi=1200)

"*************************************************************"
"*                                                           *"
"*             DISTRIBUICAO DA INTENSIDADE                   *"
"*                   POR HORA DO DIA                         *"
"*                                                           *"
"*************************************************************"
horario = dados.Velvento.groupby(dados.index.hour).aggregate('mean')

#fig.set_size_inches(figsize)

ax = dados.boxplot(column=['Velvento'],
                    by=dados.index.hour,
                    sym='',
                    figsize=figsize,
                    fontsize=fontsize
                    )
ax.set_xlabel('Hours', size=fontsize)
ax.set_ylabel('Wind speed (m/s)', size=fontsize)
ax.set_title('')
plt.suptitle('')
plt.savefig(pathname + '\\ingles_intensidade_vento_hora.png',
            format='png',
            dpi=1200)

"*************************************************************"
"*                                                           *"
"*       DISTRIBUICAO DA INTENSIDADE POR DIRECAO             *"
"*               AO LONGO DE TODA A SERIE                    *"
"*                                                           *"
"*************************************************************"
#direcoes = dados.Velvento.groupby(dados.Direcao).mean()

ax = dados.boxplot(column=['Velvento'],
                    by=dados.Direcao,
                    sym='*',
                    figsize=figsize,
                    fontsize=18)
ax.set_xlabel(u'Wind Direction', size=fontsize)
ax.set_ylabel('Wind speed (m/s)', size=fontsize)
ax.set_title('')
plt.suptitle(u'', size=fontsize+1)
plt.savefig(pathname + '\\ingles_intensidade_vento_direcao.png',
            format='png',
            dpi=1200)

"*************************************************************"
"*                                                           *"
"*          DISTRIBUICAO DA INTENSIDADE E DIRECAO            *"
"*                    AO LONGO DO ANO                        *"
"*                                                           *"
"*************************************************************"
# Direcao ao longo do ano
direcao_count_mes = dados.groupby([dados.index.month,
                                         'Direcao']).size()
# transforma num dataframe 2D com as horas nas linhas e as
# direcoes nas colunas
direcao_f_mes = direcao_count_mes.unstack(level = 0)
# divide cada contagem de direcao pela contagem de pontos
# naquela hora
direcao_freq_mes = direcao_f_mes/direcao_f_mes.sum()
direcao_freq_mes.to_csv(path_or_buf=pathname + '\\frequencia_direcao_mes.csv')
direcao_freq_mes = direcao_freq_mes.transpose()


ax = direcao_freq_mes.plot(kind = 'bar',
                            rot = True,
                            stacked = True,
                            color=(esquema_cores5),
                            figsize=figsize,
                            fontsize=18)
ax.legend(loc='upper center',
            ncol=8,
            bbox_to_anchor=(0.5, 1.1),
            fancybox=True,
            fontsize=fontsize-4)
ax.set_ylim([0,1])
ax.set_yticklabels([0, 20, 40, 60, 80, 100])
ax.set_xticklabels(months_label.keys())
ax.set_ylabel(u'Frequency (%)', size=fontsize)
ax.set_xlabel(u'', size=fontsize)
plt.savefig(pathname + '\\ingles_frequencia_direcao_mensal.png',
            format='png',
            dpi=1200)

# Intensidade ao longo do ano
ax = dados.boxplot(column=['knots'],
                    by=dados.index.month,
                    sym='*',
                    figsize=figsize,
                    fontsize=fontsize)
ax.set_xlabel(u' ', size=fontsize)
ax.set_xticklabels(months_label.keys())
ax.set_ylabel('Wind speed (knots)', size=fontsize)
ax.set_title('')
plt.suptitle(u' ', size=fontsize+1)
plt.savefig(pathname + '\\ingles_intensidade_vento_mensal.png',
            format='png',
            dpi=1200)

"*************************************************************"
"*                                                           *"
"*            ROSA DOS VENTOS POR PERIODO SAZONAL            *"
"*          SEGUINDO A MESMA DIVISAO DA CHUVA (SECO,         *"
"*                   CHUVOSO E TRANSICAO)                    *"
"*                                                           *"
"*************************************************************"

"""
ROSA DOS VENTOS PARA TODA A SERIE

"""

mpl.rcParams['xtick.labelsize'] = label_size
mpl.rcParams['ytick.labelsize'] = label_size
ax = new_axes()
ax.bar(dados.Ventodir, dados.Velvento, normed=True, opening=0.8,
       edgecolor='white')
#ax.set_rlim(0,82) # Nao funcionou...
plt.title('Intensidade e direcao do vento - 2016')
set_legend(ax)
plt.savefig(pathname + '\\windrose_anual.png',
            format='png',
            dpi=1200)



ax = new_axes()

ax.bar(periodo_chuvoso.Ventodir, periodo_chuvoso.Velvento, normed=True, opening=0.8,
       edgecolor='white')
#ax.set_rlim(0,82)
plt.title('Intensidade e direcao do vento - Periodo chuvoso')
set_legend(ax)
plt.savefig(pathname + '\\windrose_chuvoso.png',
            format='png',
            dpi=1200)


ax = new_axes()

ax.bar(periodo_seco.Ventodir, periodo_seco.Velvento, normed=True, opening=0.8,
       edgecolor='white')
#ax.set_rlim(0,82)
plt.title('Intensidade e direcao do vento - Periodo seco')
set_legend(ax)
plt.savefig(pathname + '\\windrose_seco.png',
            format='png',
            dpi=1200)
