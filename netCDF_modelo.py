# -*- coding: utf-8 -*-
"""
Spyder Editor

Este é um arquivo de script temporário.
"""
import xarray as xray
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

filename, pathname = get_path('*.nc')
xr = xray.open_dataset(filename)



x = xr.station_x_coordinate.values
y = xr.station_y_coordinate.values
plt.scatter(x, y)
nomes = xr.station_name.values
nomes = [str(nomes[i]) for i in range(len(nomes))]
for i in range(len(nomes)):
    plt.text(float(x[i]),float(y[i]), 
             nomes[i], 
             va="top", 
             family="monospace")
    
# Plotando todas as series em cada ponto do hist.
for i in range(len(xr.station_id.data)):
    plt.figure()
    plt.plot(xr.waterlevel.data[:,i])
    plt.title(xr.waterlevel['station_name'][i].data)