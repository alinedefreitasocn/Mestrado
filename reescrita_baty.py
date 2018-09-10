# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 18:15:09 2017

@author: aline
Scrip para ler e salvar os arquivos de batmetria

"""

import pandas as pd
import numpy as np
import wx
import matplotlib.pyplot as plt
import xarray
from mpl_toolkits.basemap import Basemap as bm
from scipy.interpolate import griddata
import utm


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

filename, pathname = get_path('*Bruno*.csv')

bruno = pd.read_table(filename, sep=';', header=0)

filename, pathname = get_path('*aline*.csv')

aline = pd.read_table(filename, sep=';', header=0)

bat = pd.concat([aline, bruno])
bat.Prof = bat.Prof.values * -1
plt.plot(bat.POINT_X, bat.POINT_Y, '.')

lon = bat.POINT_X.values            # array like
lat = bat.POINT_Y.values            # array like
topo = bat.Prof.values           # array like

bat.to_csv(path_or_buf=pathname + '\\batimetria_UTM.csv',sep='\t', index=False)

a = [utm.to_latlon(lon[i], lat[i], 23, 'N') for i in range(len(lat))]
