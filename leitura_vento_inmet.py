# -*- coding: utf-8 -*-
"""
Spyder Editor

Este é um arquivo de script temporário.
"""

import pandas as pd
import matplotlib.pyplot as plt


f = pd.read_csv('serie_ano_salinopolis_alterado.csv', sep=';', header = 0, 
                na_values = '////')# parse_dates=[['Data', 'Hora']], dayfirst= 'True')
data_hora = f['Data'] + ' ' + f['Hora'] + ':00'  #nao esta dando certo!
