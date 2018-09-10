# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 11:15:49 2017
Leitura e analise dos dados dados_inmeteorologicos de Salinopolis
@author: Aline
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

"""Adicionei essa variavel para poder observar as mudancas nas estatisticas se
considerassemos apenas volumes maiores de chuva.
descobri que o numero de dias de chuva por mes foi estimado com base nos
registros da ANA que ja tem uma variavel chamada dias de chuva. Nao sei qual
limite eles usam."""
lim_chuva = 2.5

grafico = input('Deseja gerar figuras? (sim = 1; nao = 0)     ')

"DEFININDO VARIAVEIS PADRAO"
current_palette = sns.color_palette()
sns.set_palette("PuBuGn_d")
sns.set_style("white")
sns.set_style("ticks")
sns.despine()
sns.set_context("poster")
cores = sns.color_palette(palette="PuBuGn_d", n_colors=15)
#cores = sns.cubehelix_palette(8, start=.5, rot=-.75, as_cmap=False)


label_size = 18
fontsize = 16

meses_label = OrderedDict([('Jan', 1), ('Fev', 2), ('Mar', 3),
                           ('Abr', 4), ('Mai', 5), ('Jun', 6),
                           ('Jul', 7), ('Ago', 8), ('Set', 9),
                           ('Out', 10), ('Nov', 11), ('Dez', 12)])

month_label = OrderedDict([('Jan', 1), ('Feb', 2), ('Mar', 3),
                           ('Apr', 4), ('May', 5), ('Jun', 6),
                           ('Jul', 7), ('Aug', 8), ('Sep', 9),
                           ('Oct', 10), ('Nov', 11), ('Dec', 12)])


"****************************************************************"
"*                                                              *"
"*                 LEITURA DOS ARQUIVOS                         *"
"*                                                              *"
"****************************************************************"
# escolhendo o arquivo de entrada
print('ESCOLHA O ARQUIVO DO INMET')
filename_INMET, pathname = get_path('*.csv')

"Lendo arquivo do INMET"
# Juntando data em uma unica coluna
# Detalhe que o dataparse precisa do padrão %Y %m %d separado por espacos
# indicando que cada variavel esta em uma coluna diferente
dateparse = lambda x: pd.datetime.strptime(x, '%Y %m %d %H')
dados_inmet = pd.read_csv(filename_INMET, sep=';', header=0, na_values='////',
                  parse_dates={'datahora': ['Ano', 'Mes', 'Dia', 'Hora']},
                  date_parser=dateparse, squeeze=True, index_col=0)

# usando apenas o ano de 2016 nas análises
dados_inmet = dados_inmet[dados_inmet.index.year < 2017]
dados_inmet = dados_inmet[dados_inmet.index.year > 2008]


print('ESCOLHA O ARQUIVO DA ANA')
filename_ANA, pathname_ANA = get_path('*.csv')

"Lendo arquivo da ANA"
dateparse = lambda x: pd.datetime.strptime(x, '%d/%m/%Y')
ANA = pd.read_csv(filename_ANA, sep=';', header=0, na_values='',
                  dayfirst=True, skiprows=13, parse_dates=[2],
                  date_parser=dateparse, index_col=2)

del(filename_ANA, pathname_ANA, filename_INMET)

# Dados da ANA estavam com entradas duplicadas...Uma linha eh dado
# consistido e o outro eh bruto. Selecionar as linhas dos brutos
# pq tem meses faltando nos consistidos.
# Daddos foram consistidos ate 2006-10-01
# Selecionando apenas os valores consistidos, quando existentes
ANA_consist = ANA[ANA.NivelConsistencia == 2]
# completando com os dados brutos nos registros onde nao houve
# consistencia
ANA_bruto = ANA[ANA.index > '2006-10-01']
ANA = ANA_consist.append(ANA_bruto)
# cortando o inicio e o final da serie onde os anos estavam
# incompletos
ANA = ANA[ANA.index.year < 2016]
ANA = ANA[ANA.index.year > 1977]

del(ANA_consist, ANA_bruto)

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
dados_inmet.index = dados_inmet.index.tz_localize(tz='utc')
dados_inmet.index = dados_inmet.index.tz_convert('America/Fortaleza')

'***********************************************************'
'*                                                         *'
'*                 Analise dos dados da ANA                *'
'*                  Serie completa da ANA                  *'
'*                                                         *'
'***********************************************************'
"""Variavel Total representa o total acumulado no mes"""
if grafico == 1:
    mpl.rcParams['xtick.labelsize'] = label_size
    mpl.rcParams['ytick.labelsize'] = label_size
    mpl.rcParams['font.size'] = label_size
    plt.figure(figsize=[13, 6])
    ANA.Total.plot()
    #plt.ylabel('Chuva Acumulada Mensal (mm)')
    plt.ylabel('Month rain sum (mm)')
    plt.xlabel('Years') #plt.xlabel('Anos')
    plt.savefig(pathname + '\\serie_completa_ANA_ingles.png', format='png', dpi=1200)
    #plt.savefig(pathname + '\\serie_completa_ANA.png', format='png', dpi=1200)

    plt.figure()
    # acumulado anual
    chuva_anual = ANA.Total.groupby(ANA.index.year).sum()
    media_chuva_anual = chuva_anual.mean()
    chuva_anual.plot(style='o-')
    plt.xlim([1978, 2015])
    plt.ylabel('Chuva acumulada anual (mm)')
    plt.xlabel('Anos')
    plt.annotate(u'Média anual: %.1f mm' % (media_chuva_anual), (1980, 1000))
    plt.savefig(pathname + '\\chuva_acumulada_anual.png', format='png', dpi=1200)

""""""
'***********************************************************'
'*                                                         *'
'*                 Analise dos dados da ANA                *'
'*        Medias mensais da ANA e comparacao com 2016      *'
'*                                                         *'
'***********************************************************'
# Agrupando os dados da ANA por mes e fazendo a media mensal.
# Estatistica para media mensal de chuva e de numero de dias de chuva

media_chuva_mensal = ANA.groupby(ANA.index.month).Total.mean()
std_chuva_mensal = ANA.groupby(ANA.index.month).Total.std()
media_dias_chuva = ANA.groupby(ANA.index.month).NumDiasDeChuva.mean()
quantile10_dias_chuva = ANA.groupby(ANA.index.month).NumDiasDeChuva.quantile(
                                                                        q=0.10)
quantile90_dias_chuva = ANA.groupby(ANA.index.month).NumDiasDeChuva.quantile(
                                                                        q=0.90)
quantile25_dias_chuva = ANA.groupby(ANA.index.month).NumDiasDeChuva.quantile(
                                                                        q=0.25)
quantile50_dias_chuva = ANA.groupby(ANA.index.month).NumDiasDeChuva.quantile(
                                                                        q=0.5)
quantile75_dias_chuva = ANA.groupby(ANA.index.month).NumDiasDeChuva.quantile(
                                                                        q=0.75)
std_dias_chuva = ANA.groupby(ANA.index.month).NumDiasDeChuva.std()

# media de chuva mensal dos dados do inmet (soh 2016)
chuva_mensal_INMET = dados_inmet.groupby(dados_inmet.index.month).chuva.sum()/8



if grafico == 1:
    "Plotando figuras"
    n_groups = 12
    fig, ax = plt.subplots(figsize=[13, 7])
    index = np.arange(1, n_groups+1)
    bar_width = 0.30
    opacity = 0.8

    plt.plot(media_dias_chuva, color= cores[2], alpha=0.8)
    plt.fill_between(x=media_dias_chuva.index, y1=quantile10_dias_chuva,
                     y2=quantile90_dias_chuva, interpolate=True,
                     color=cores[2], linestyle='--', alpha=0.3) #'#b1c4dd'
    plt.fill_between(x=media_dias_chuva.index, y1=quantile25_dias_chuva,
                     y2=quantile75_dias_chuva, interpolate=True,
                     color=cores[2], linestyle='--', alpha=0.6) #'#95b5df'
    #plt.title(u'Número médio de dias de chuva por mês')
    #plt.title(u'Mean number of rainy days')
    plt.xlabel(u'')
    plt.xticks(index, month_label.keys(), size=18)
    plt.ylabel('Mean number of rainy days', size=18)
    plt.ylim([0,31])
    plt.xlim([1,12])
    plt.savefig(pathname + '\\ingles_media_dias_chuva.png', format='png', dpi=1200)

    plt.figure(figsize=[13, 7])
    plt.errorbar(index, media_chuva_mensal, yerr=std_chuva_mensal, fmt='ok',
                 label=u'Standard Deviation')
    plt.plot(chuva_mensal_INMET, '--*', label='Mensal mean 2016',
                 color=sns.set_palette("PuBuGn_d", 2))
    #plt.plot(ana2016, '--*r', label='Media Mensal ANA: 2016')
    rects1 = plt.bar(index, media_chuva_mensal, bar_width, alpha=opacity,
                     label='Mensal mean: 1978 - 2015',
                     color=cores[11])
    plt.legend()
    plt.ylabel('Rain sum (mm)')
    plt.xticks(index, meses_label.keys())
    plt.ylim([0, 899])
    plt.savefig(pathname + '\\ingles_climatologia.png', format='png', dpi=1200)


"""CLIMATOLOGIA COLORIDO!!!!"""

index_chuvoso = np.arange(1,6,1)
media_chuvoso = media_chuva_mensal[media_chuva_mensal.index <6]
plt.bar(index_chuvoso,media_chuvoso, bar_width, alpha = opacity, label = 'Wet', color = 'navy') #cores[6])

mediaT = media_chuva_mensal[media_chuva_mensal.index == 6]
mediaT = mediaT.append(media_chuva_mensal[media_chuva_mensal.index == 7])
mediaT = mediaT.append(media_chuva_mensal[media_chuva_mensal.index == 12])
indexT = [6, 7, 12]
plt.bar(indexT,mediaT, bar_width, alpha = opacity, label = 'Transitional', color = 'darkred')


media = media_chuva_mensal[media_chuva_mensal.index == 8]
for i in np.arange(9, 12, 1):
    a = media_chuva_mensal[media_chuva_mensal.index == i]
    media = media.append(a)
indexD = np.arange(8,12,1)
plt.bar(indexD,media.values, bar_width, alpha = opacity, label = 'Dry', color = cores[0])
plt.legend()

plt.xticks(index, meses_label.keys())
plt.ylim([0, 899])


"""
separando periodos seco, chuvoso e de transicao de acordo com o
grafico da ANA
"""
"Meses de chuva de jan a mai"
periodo_chuvoso = dados_inmet[dados_inmet.index.month < 6]
"chuvoso para os dados da ANA"
periodo_chuvoso_ANA = ANA[ANA.index.month < 6]

# media de chuva durante o periodo chuvoso
periodo_chuvoso_ANA.groupby(periodo_chuvoso_ANA.index.month).Total.mean().mean()
periodo_chuvoso_ANA.groupby(periodo_chuvoso_ANA.index.month).Total.max().max()

"Meses de Transicao (Jun, Jul e Dez)"
periodo_transicao = dados_inmet[dados_inmet.index.month == 6]
periodo_transicao = periodo_transicao.append(dados_inmet
                                             [dados_inmet.index.month == 7])
periodo_transicao = periodo_transicao.append(dados_inmet
                                             [dados_inmet.index.month == 12])
"Transicao para os dados da ANA"
periodo_transicao_ANA = ANA[ANA.index.month == 6]
periodo_transicao_ANA = periodo_transicao_ANA.append(ANA
                                             [ANA.index.month == 7])
periodo_transicao_ANA = periodo_transicao_ANA.append(ANA
                                             [ANA.index.month == 12])
periodo_transicao_ANA.groupby(periodo_transicao_ANA.index.month).Total.mean().mean()
periodo_transicao_ANA.groupby(periodo_transicao_ANA.index.month).Total.max().max()

"Meses secos de Ago a Nov"
periodo_seco = pd.DataFrame()
for i in np.arange(8, 12, 1):
    pmes = dados_inmet[dados_inmet.index.month == i]
    periodo_seco = periodo_seco.append(pmes, index=True)

"ANA"
periodo_seco_ANA = pd.DataFrame()
for i in np.arange(8, 12, 1):
    pmesA = ANA[ANA.index.month == i]
    periodo_seco_ANA = periodo_seco_ANA.append(pmesA)
periodo_seco_ANA.groupby(periodo_seco_ANA.index.month).Total.mean().mean()
periodo_seco_ANA.groupby(periodo_seco_ANA.index.month).Total.max().max()
periodo_seco_ANA.groupby(periodo_seco_ANA.index.month).Total.min().min()

"*******************************************************************"
"*                                                                 *"
"* ANALISE HORARIA DE CHUVA - PERIODO CHUVOSO, SECO E TRANSICAO    *"
"*                 A PARTIR DOS DADOS DO INMET                     *"
"*                                                                 *"
"*                                                                 *"
"*******************************************************************"

# CONTANDO A QUANTIDADE DE DIAS QUE CHOVE EM CADA HORARIO, NO PERÍODO
# CHUVOSO, NO PERIODO SECO E NO PERIODO DE TRANSICAO
# PRIMEIRO SEPARA OS REGISTROS COM CHUVA MAIOR QUE 0.2 MM
chuva_periodo_chuvoso = periodo_chuvoso[periodo_chuvoso > lim_chuva]
# AGRUPA POR HORA
# chuva_periodo_chuvoso = chuva_periodo_chuvoso.groupby(
#                                    by=chuva_periodo_chuvoso.index.hour,
#                                    sort=True, group_keys=True)

# CONTA O NUMERO DE REGISTROS POR HORA E TIRA A PORCENTAGEM COM RELAÇÃO AO TOTAL DE MEDICOES NO PERIODO
dias_chuva_chuvoso = chuva_periodo_chuvoso.groupby(
                                    by=chuva_periodo_chuvoso.index.hour,
                                    sort=True, group_keys=True).count()*100./(
                                                     len(periodo_chuvoso)/24.)
# media_chuva_verao = periodo_chuvoso.groupby(
#                                 periodo_chuvoso.index.hour).chuva.mean()
media_chuva_verao = periodo_chuvoso.groupby(
        by=periodo_chuvoso.index.hour).mean()


"###########################################################################"
# MESMA COISA PARA O PERIODO SECO
chuva_periodo_seco = periodo_seco[periodo_seco > lim_chuva]
# chuva_periodo_seco = chuva_periodo_seco.groupby(
#                                by=chuva_periodo_seco.index.hour,
#                                sort=True, group_keys=True)
dias_chuva_periodo_seco = chuva_periodo_seco.groupby(
                                    by=chuva_periodo_seco.index.hour,
                                    sort=True, group_keys=True).count()*100./(
                                                        len(periodo_seco)/24.)
# tem que fazer essa parte pro periodo seco pq quase nao tem chuva
dias_chuva_seco = np.zeros(24)
dias_chuva_seco[dias_chuva_periodo_seco.index[0]] = dias_chuva_periodo_seco
media_chuva_seco = periodo_seco.groupby(periodo_seco.index.hour).chuva.mean()
#media_chuva_seco = np.zeros(24)
#media_chuva_seco[media_chuva_seco.index[0]] = chuva_periodo_seco.chuva.groupby(
#        by=chuva_periodo_seco.index.hour).mean()

"###########################################################################"
# MESMA COISA PARA O PERIODO DE TRANSICAO
chuva_periodo_transicao = periodo_transicao[periodo_transicao > lim_chuva]
# chuva_periodo_transicao = chuva_periodo_transicao.groupby(
#                                by=chuva_periodo_transicao.index.hour,
#                                sort=True, group_keys=True)
dias_chuva_transicao = chuva_periodo_transicao.groupby(
                                by=chuva_periodo_transicao.index.hour,
                                sort=True, group_keys=True).count()*100./(
                                                   len(periodo_transicao)/24.)
# media_trans = periodo_transicao.groupby(
#                            periodo_transicao.index.hour).chuva.mean()
# muito dias sem chuva!!
media_trans = periodo_transicao.groupby(
        by=periodo_transicao.index.hour).mean()

"*********************************************************"
"*                                                       *"
"  frequencia de ocorrencia (dias) de chuva por horario   "
"*                                                       *"
"*********************************************************"
# criando plot da media horaria das chuvas e do vento
# COM EIXO SECUNDARIO!
# precisa ser subplot pra funcionar o ax.twinx
if grafico == 1:
    n_groups = 24


    mpl.rcParams['xtick.labelsize'] = label_size
    mpl.rcParams['ytick.labelsize'] = label_size
    mpl.rcParams['font.size'] = label_size

    fig, ax = plt.subplots(figsize=[13, 6])
    index = np.arange(n_groups)
    bar_width = 0.25
    opacity = 0.8

    # rects1 = plt.bar(index, media_chuva_seco, bar_width, alpha=opacity,
    #    color= colors['darkcyan'], label='Seco')
    rects1 = plt.bar(index, dias_chuva_seco, bar_width, alpha=opacity,
                     color=cores[0],
                     label='Dry')

    # rects2 = plt.bar(index + bar_width, media_chuva_verao, bar_width,
    #                 alpha=opacity,
    #                 color=colors['goldenrod'],
    #                 label='Chuvoso')
    rects3 = plt.bar(index + (2*bar_width), dias_chuva_transicao, bar_width,
                 alpha=opacity,
                 color=cores[6],
                 label=u'Transitional')

    rects2 = plt.bar(index + bar_width, dias_chuva_chuvoso, bar_width,
                     alpha=opacity,
                     color=cores[12],
                     label='Wet')

    plt.ylabel(u'Rainy days (%)')
    plt.xlabel('Hour')
    plt.legend()
    # ax2 = ax.twinx()
    # ax2.plot(velvento_inv, color=colors['darkcyan'])
    # ax2.plot(velvento_verao, color=colors['goldenrod'])
    # ax2.set_ylabel('velocidade do vento [m/s]')
    # ax2.tick_params('y')
    plt.title('Distribuicao de chuva ao longo do dia')
    plt.xticks(index + bar_width, ('0:00', ' ', '2:00', ' ',
                                   '4:00', ' ', '6:00', ' ',
                                   '8:00', ' ', '10:00', ' ',
                                   '12:00', ' ', '14:00', ' ',
                                   '16:00', ' ', '18:00', ' ',
                                   '20:00', ' ', '22:00', ' '))
    plt.tight_layout()
    plt.xlim([-0.1, 24])
    # mpl.rc('font', **font)
    plt.savefig(pathname + '\\ingles_dias_chuva_hora.png', format='png', dpi=1200)


"*********************************************************"
"*                                                       *"
"*             Quantidade de chuva (mm) por hora         *"
"*                                                       *"
"*********************************************************"
if grafico == 1:
    # data to plot
    n_groups = 24
    # criando plot da media horaria das chuvas e do vento
    # COM EIXO SECUNDARIO!
    # precisa ser subplot pra funcionar o ax.twinx

    mpl.rcParams['xtick.labelsize'] = label_size
    mpl.rcParams['ytick.labelsize'] = label_size
    mpl.rcParams['font.size'] = label_size

    fig, ax = plt.subplots(figsize=[13, 6])
    index = np.arange(n_groups)
    bar_width = 0.3
    opacity = 0.8

    # rects1 = plt.bar(index, media_chuva_seco, bar_width, alpha=opacity,
    #    color= colors['darkcyan'], label='Seco')
    rects1 = plt.bar(index, media_chuva_seco, bar_width, alpha=opacity,
                     color=cores[0],
                     label='Dry')

    # rects2 = plt.bar(index + bar_width, media_chuva_verao, bar_width,
    #                 alpha=opacity,
    #                 color=colors['goldenrod'],
    #                 label='Chuvoso')
    rects3 = plt.bar(index + (2*bar_width), media_trans, bar_width,
                     alpha=opacity,
                     color= cores[6],
                     label=u'Transitional')

    rects2 = plt.bar(index + bar_width, media_chuva_verao, bar_width,
                     alpha=opacity,
                     color=cores[12],
                     label='Wet')

    plt.ylabel(u'Mean rain (mm)')
    plt.xlabel('Hour')
    plt.legend()
    # ax2 = ax.twinx()
    # ax2.plot(velvento_inv, color=colors['darkcyan'])
    # ax2.plot(velvento_verao, color=colors['goldenrod'])
    # ax2.set_ylabel('velocidade do vento [m/s]')
    # ax2.tick_params('y')
    plt.title('Distribuicao de chuva ao longo do dia')
    plt.xticks(index + bar_width, ('0:00', ' ', '2:00', ' ',
                                   '4:00', ' ', '6:00', ' ',
                                   '8:00', ' ', '10:00', ' ',
                                   '12:00', ' ', '14:00', ' ',
                                   '16:00', ' ', '18:00', ' ',
                                   '20:00', ' ', '22:00', ' '))
    plt.tight_layout()
    plt.xlim([-0.1, 24])
    # mpl.rc('font', **font)
    plt.savefig(pathname + '\\ingles_media_chuva_horaria.png', format='png', dpi=1200)


"*********************************************************************************"
"*                                                                               *"
"*                    ANALISE DE CHUVA DIARIA                                    *"
"*                   A PARTIR DOS DADOS DA ANA                                   *"
"*                                                                               *"
"*********************************************************************************"
#Contruindo uma lista de nome das colunas de chuva
list_nome_col = []
for i in np.arange(1, 32):
    if i < 10:
        nome_col = ('Chuva' + '0' + str(i))
    else:
        nome_col = ('Chuva' + str(i))
    list_nome_col.append(nome_col)

chuva_diaria = ANA[list_nome_col].copy()
#chuva_diaria = chuva_diaria[chuva_diaria > 0.2]
chuva_diaria_media = np.array(chuva_diaria.groupby(
        by=chuva_diaria.index.month).mean())


# Tem que colocar o espaco em branco nos dias que nao tiver dia no label!!
dias = [1, 6, 11, 16, 21, 26, 31]
tick = np.arange(0, 32, 5)
if grafico == 1:
    f, axarr = plt.subplots(6, 2, figsize=[13, 6])
    for a in range(2):
        for i in range(6):
            if a == 0:
                m = i
            else:
                m = i+6
            axarr[i,a].plot(chuva_diaria_media[m], marker='o', color='k')
            axarr[i,a].grid(axis='y', color='gray', linestyle='dashed')
            axarr[i,a].set_ylim(0, 34)
            axarr[i,a].set_xlim(0,30)
            axarr[i,a].set_yticks(np.arange(0, 34, 10))
            axarr[i,a].set_ylabel(meses_label.keys()[m] + ' (mm)')
            if i < 5:
                axarr[i,a].set_xticklabels([])
        axarr[5][a].set_xticks(tick)
        axarr[5][a].set_xticklabels(dias)
        axarr[5][a].set_xlabel(u'Dias do Mês')
    plt.suptitle(u'Média diária de chuva por mês (mm)')
    plt.savefig(pathname + '\\media_diaria_chuva.png', format='png',
                dpi=1200)


"***********************************************************"
"*                                                         *"
"*         Contagem dos dias consecutivos de chuva         *"
"*                                                         *"
"***********************************************************"
diasdechuva = []
for line in chuva_diaria.index:
    b = [0]      # sempre zerar
    chuva = []  # sempre zerar
    chuva = chuva_diaria[chuva_diaria.index == line]
    for i in list_nome_col:
        ii = int(i[-2:])  # pega so o numero do dia. i eh o nome da col
        if chuva[i][0] > lim_chuva:
            a = int(b[ii-1]) + 1
            b.insert(ii, a)
        else:
            b.insert(ii, 0)
    b = np.array(b)
    diasdechuva.append(b)
diasdechuva=pd.DataFrame(diasdechuva, index=chuva_diaria.index)


"*************************************************************"
"*                                                           *"
"*        ESTATISTICA DIAS CONSECUTIVOS CHUVA                *"
"*                                                           *"
"*************************************************************"
maximos = diasdechuva.max(axis=1)
maximos_mes = maximos.groupby(by=maximos.index.month, sort=True).mean()
median_maximos = maximos.groupby(by=maximos.index.month, sort=True).median()
std_maximos = maximos.groupby(by=maximos.index.month, sort=True).std()
#var_mes = maximos.groupby(by=maximos.index.month, sort=True).var()

#plt.grid(axis='y')
if grafico == 1:
    plt.figure(figsize=[13, 7])
    plt.errorbar(maximos_mes.index, maximos_mes, yerr=std_maximos, fmt='ok',
                 label=u'Standard Deviation')
    plt.bar(maximos_mes.index, maximos_mes, 0.35,
                         alpha=0.8,
                         color= cinza5,
                         label=u'Consecutive days of rain')
    plt.ylabel(u'Mean consecutive days of rain')
    plt.xlabel(u'Meses do ano')
    plt.ylim([0, 31])

    plt.xticks(maximos_mes.index[1:13:2], ('Fev', 'Abr', 'Jun', 'Ago',
                                           'Out', 'Dez'))


grafico = 1




'''
          CONFERINDO ALGUNS DADOS
'''
chuva_periodo_chuvoso = periodo_chuvoso[periodo_chuvoso.chuva > 0.2]
chuva_periodo_chuvoso = chuva_periodo_chuvoso.groupby(
                                    by=chuva_periodo_chuvoso.index.hour,
                                    sort=True, group_keys=True)
hora = 4
chuva = periodo_chuvoso.chuva[periodo_chuvoso.index.hour == hora]
chuva.plot()
chuva.mean()
plt.ylabel(u'Chuva (mm)')
plt.ylabel([u'Chuva por hora às ' + hora + ' AM (mm)'])

''' #########################################################
#
#  CALCULANDO OS VALORES MAXIMOS DE CHUVA PARA CADA HORA
#
'''#########################################################
maximos = chuva_periodo_chuvoso.chuva.max()

# NAO ESTA REPRESENTATIVO (EU ACHO). ALGUNS EVENTOS EXTREMOS