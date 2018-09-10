#############################################################################
#############################################################################
#### Analise Harmonica  PP ####
nivel=dd['nivel(m)']

from pytides.tide import Tide #IMPORTAR PACOTE PYTIDE
n = nivel.values - nivel.values.mean()
tide = Tide.decompose(dd['nivel(m)'],dd.index.to_datetime())
#CONTRUINDO TABELA DAS CONSTANTES HARMONICAS
import numpy as np
from pandas import DataFrame
constituent = [c.name for c in tide.model['constituent']]
ddf = DataFrame(tide.model, index=constituent).drop('constituent', axis=1)
ddf.sort('amplitude', ascending=False).head(10)
#############################################
# FORM NUMBER : CLASSIFICACAO DA MARE
print('Form number %s, the tide is %s.' %
      (tide.form_number()[0], tide.classify()))
############################################
# PREVISÃO DE MARÉ
from pandas import Series, read_csv, date_range #IMPORTAR FUNÇÕES DO PANDAS
dates = date_range(start='2009-01-01', end='2009-12-31', freq='60T')# determinar eixo temporal e freq.

hours = np.cumsum(np.r_[0, [t.total_seconds() / 3600.0
                            for t in np.diff(dates.to_pydatetime())]])

times = Tide._times(dates[0], hours)

#prediction = Series(tide.at(times) + nivel.mean(), index=dates)
dd['tide'] = Series(tide.at(times) + dd['nivel(m)'].mean(), index=dates)

dd['nivel(m)']=dd['nivel(m)']-dd['nivel(m)'].mean()
dd['tide']=dd['tide']-dd['tide'].mean()
dd['filt_tide']=dd['nivel(m)']-dd['tide']

#fig2, ax2 = plt.subplots(figsize=(20, 10))
fig2=plt.subplots(figsize=(20, 10))
ax2=dd['nivel(m)'].plot(color='b',label='Observed data')
ax2=dd['tide'].plot(color='r',label='Tide')
ax2=dd['filt_tide'].plot(marker='*',color='k',linewidth=3,label='[data] - [tide]')
ax2.legend(loc='best')
fig.savefig(path+'ILHAFISCAL_2009_data_tide.png', dpi=100)

#referencias
'https://ocefpaf.github.io/python4oceanographers/blog/2014/07/07/pytides/'
#############################################################################