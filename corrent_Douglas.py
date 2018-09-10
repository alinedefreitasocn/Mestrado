# -*- coding: utf-8 -*-
"""
Spyder Editor

Este é um arquivo de script temporário.
"""

import pandas as pd
import wx
import matplotlib.pyplot as plt
# import csv
import numpy as np
# import datetime
# from matplotlib import mlab
from windrose import WindroseAxes
import os

plt.close('all')

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

def new_axes():
    fig = plt.figure(figsize=(13, 8), dpi=80, facecolor='w', edgecolor='w')
    rect = [0.1, 0.1, 0.8, 0.8]
    ax = WindroseAxes(fig, rect, axisbg='w')
    fig.add_axes(ax)
    return ax

#...and adjust the legend box
def set_legend(ax):
    l = ax.legend(borderaxespad=-0.10,bbox_to_anchor=[-0.1, 0.5],loc='centerleft',title="m/s")
    plt.setp(l.get_texts(), fontsize=20)



filename, pathname = get_path('*.csv')
df = pd.read_csv(filename, sep=',', header = 0)
datahora = pd.date_range(start='11/22/2017 14:48:23', 
                         end='11/23/2017 15:48:36', freq='250ms')
datahora = datahora[0:-1]
df.index = datahora

df = df.resample('S')
df = df.mean()

for n in range(len(df.direc_graus)):
    if df.direc_graus[n] < 0:
        df.direc_graus[n] = df.direc_graus[n]+360

df.direc_graus = df.direc_graus - 20.20 # declinacao magnetica
ws = df.veloc.values
wd = df.direc_graus.values

label_size = 14
plt.rcParams['xtick.labelsize'] = label_size
plt.rcParams['ytick.labelsize'] = label_size
ax = new_axes()
ax.bar(wd, ws, normed=True, opening=0.8, edgecolor='black',
       bins=np.arange(ws.min(),ws.max(),0.6))
set_legend(ax)
plt.title(u'Correntes Maçarico - Salinas ', y=1.075,
           fontsize=14,fontweight='bold')
manager = plt.get_current_fig_manager()
plt.savefig(pathname + '\\corrente_20171122.png')
