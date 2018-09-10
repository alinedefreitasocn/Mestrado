
# coding: utf-8

# # Processando os dados da Boia axis

# In[8]:



# Hm0 == Hs só que a primeira eh no dominio da frequencia e a segunda no dominio do tempo. obtida nas informacoes de heave
# periodo associado ah altura maxima de onda (importante)
# espectro direcional também eh legal de fazer (polar colorido)

# ctrl + enter --> executa e continua no mesmo bloco
# shift + ctrl --> executa e vai pra proxima linha
# b --> cria uma nova celula
# tab --> identa o que estiver selecionado
# shift + tab --> desidentar


# In[9]:

import os
import numpy as np
import matplotlib.pylab as pl
from matplotlib import mlab
get_ipython().magic(u'matplotlib inline')
# plota o grafico direto na linha 
# %matplotlib qt5 # plotaria o grafico numa nova aba, mas nao funcionou


# In[10]:

def espec1(x, nfft, fs):
    # calculando o espectro
    sp = mlab.psd(x,                              # time series
                 NFFT=nfft,                       # length window (averages)
                 Fs= fs,                          # remove trend ( remove a mare da serie de onda, p.ex.)
                 detrend=mlab.detrend_mean,       # hanning window
                 window=mlab.window_hanning,      # overlap for welch spectrum
                 noverlap=nfft/2)
    f, sp = sp[1][1:], sp[0][1:]
    
    # graus de liberdade
    gl = len(x)/nfft * 2
    
    # intervalo de confianca 95%
    ici = sp * gl / 26.12
    ics = sp * gl / 5.63
    
    aa = np.array([f, sp, ici, ics]).T           # .T faz a transporta do array
    
    return aa


# In[11]:

# carrega os dados de onda
os?  # abre o help


# In[14]:

pathname = os.environ['USERPROFILE'] + '\\Dropbox\\PythonScripts\\CursoPythonHenrique\\data\\pnboia' 
# bom para pegar o inicio do endereco quando vc usa mais de um computador
print(pathname)


# In[15]:

listfiles = np.sort(os.listdir(pathname)) # lista todo o contedudo do seu pathname

# nem sempre ele lista em ordem. Eh sempre bom nao confiar. O sort ajuda a colocar em ordem
listfiles[:4]  # quando usa o np.sort, transforma o listfiles num array


# In[16]:

# vamos criar um loop pra ele pegar somente os arquivos com extencao HNE
# range --> cria uma lista com os valores
# np.arange --> cria um array com o valores
listhne = []
for l in listfiles:
    #print l
    if l.endswith('.HNE'):    # a funcao endswith eh exclusiva das variaveis strings
        listhne.append(l)  
listhne


# In[17]:

# vamos criar um dicionario com determinados dias
days = ['01', '05', '10', '23']
dictdays = {}
listdays = []
for a in listhne:
    #print a
    for day in days:
        if a.startswith('200905%s' %day):
            listdays.append(a)
        dictdays['d%s' %day] =  listdays
dictdays['d05']    # nao prestou!! Esta acumulando os listdays! 
# precisa limpar o listdays em algum ponto...


# In[18]:

filename = listhne[0]
filename


# In[19]:

pathname + '\\' + filename


# In[20]:

arq = np.loadtxt(pathname + '\\' + filename, skiprows=11)


# In[21]:

print(arq[:3])


# In[22]:

arq.shape


# In[23]:

get_ipython().magic(u'matplotlib inline')
pl.close('all')   # como nao precisa do hold on, eh bom fechar todas as janelas antes de uma nova figura
pl.figure(figsize=[15, 12])
pl.plot(arq[:,0], arq[:,1], '-o')
pl.xlabel(u'Tempo')
pl.ylabel(u'Elevação da superficie')
pl.grid()
pl.title(u'Série de Heave')


# In[24]:

# identificar ondas individuais
# o arquivo txt pode ser lido ja separando em variaveis
time, hv, dy, dx = np.loadtxt(pathname + '\\' + filename, skiprows=11, unpack=True)


# In[25]:

# loop variando os dados de heave
pl.close('all')
pl.figure(figsize=[15, 12])
pl.plot(hv, '-o')

# indice do inicio do zero ascendente (indza) de cada onda
iza = []
# indice do inicio do zero descendente (indzd) de cada onda
izd = []

for e in range(len(hv)-1):
    if hv[e] < 0 and hv[e+1] >= 0:
        iza.append(e)
        pl.plot(e, hv[e], 'ro', e+1, hv[e+1], 'yo')
    elif hv[e] > 0 and hv[e+1] <= 0:
        izd.append(e)

zip(iza, izd)[:5]   # cria um lista com tuplas das duas variaveis de forma ordenada. Nao funciona no Python 3!!
        


# In[26]:

# pega o trecho da onda individual de acordo com o indice do zero ascendente
hv[np.arange(iza[0], iza[1])]


# In[27]:

# extrai o valor maximo absoluto da serie
np.max(abs(hv[np.arange(iza[0], iza[1])]))


# In[28]:

pl.close('all')
pl.figure(figsize=[15, 12])
pl.plot(hv, '-o')

H_onda_individual = []
Taz = []   # periodo dos Zeros Ascendentes
for i in range(len(iza)-1):
    H_onda_individual.append(abs(np.max(hv[np.arange(iza[i],iza[i+1]+1)])) + 
                            abs(np.min(hv[np.arange(iza[i],iza[i+1]+1)])))   # ja retorna a altura de onda. soma o max com o min
    Taz.append(time[iza[i+1]+1] - time[iza[i]])
    pl.plot(np.arange(iza[i], iza[i+1]+1), hv[np.arange(iza[i],iza[i+1]+1)])
pl.xlim([0, 50])

Tazm = np.array(Taz).mean()

print(H_onda_individual[0])
print(Taz[:2])


# In[29]:

H_onda_individual = np.array(H_onda_individual)
sort_onda = np.sort(abs(H_onda_individual))
Hmax = H_onda_individual.max()


# In[30]:

# um terco do numero d emedicoes de onda
terco = len(sort_onda)/3  # pega o numero de ondas que correspondem a um terco da medicoes
print(sort_onda[-terco:])  
terco_onda = sort_onda[-terco:]


# In[31]:

Hs = terco_onda.mean() # media de 1/3 das maiores ondas da serie
print u'Altura significativa: %.1f m' %Hs
print u'Periodo Médio dos Zeros Ascendentes: %.1f s' %Tazm
print u'Altura Máxima: %.1f m' %Hmax


# In[32]:

# calculo de onda no dominio da frequencia
aa = espec1(x=hv,
            nfft=len(hv),             
            fs=1./(time[2]-time[1]))
#espectro bruto
aa


# In[33]:

pl.figure(figsize=[15, 12])
pl.plot(aa[:,0], aa[:,1])


# In[34]:

for nfft1 in [len(hv), len(hv/2), len(hv)/4, len(hv)/6]:
    aa = espec1(x=hv,
                nfft=nfft1,             
                fs=1./(time[2]-time[1]))
    pl.figure(figsize=[8,4])
    pl.plot(aa[:,0], aa[:,1])
    pl.grid()
    pl.show()


# In[38]:

arquivos_hne = {}
a = listhne[0]
arquivos_hne[a] = {'tempo': time}
arquivos_hne


# In[ ]:

# processamento em batelada
arquivos_hne = {}
for a in listhne:
    time, hv, dy, dx = np.loadtxt(pathname + '\\' + a, skiprows=11, unpack=True)
    
    # indice do inicio do zero ascendente (indza) de cada onda
    iza = []
    H_onda_individual = []
    Taz = []   # periodo dos Zeros Ascendentes
    
    for e in range(len(hv)-1):
        if hv[e] < 0 and hv[e+1] >= 0:
            iza.append(e)
            pl.plot(e, hv[e], 'ro', e+1, hv[e+1], 'yo')
            

    for i in range(len(iza)-1):
        H_onda_individual.append(abs(np.max(hv[np.arange(iza[i],iza[i+1]+1)])) + 
                                abs(np.min(hv[np.arange(iza[i],iza[i+1]+1)])))   # ja retorna a altura de onda. soma o max com o min
        Taz.append(time[iza[i+1]+1] - time[iza[i]])
        
    Tazm = np.array(Taz).mean()
    
    H_onda_individual = np.array(H_onda_individual)
    sort_onda = np.sort(abs(H_onda_individual))
    Hmax = H_onda_individual.max()
    
    # um terco do numero d emedicoes de onda
    terco = len(sort_onda)/3  # pega o numero de ondas que correspondem a um terco da medicoes
    terco_onda = sort_onda[-terco:]
    Hs = terco_onda.mean()
    
    espectro = espec1(x=hv,
            nfft=len(hv),             
            fs=1./(time[2]-time[1]))
    
    arquivos_hne[a] = {'Hmax': Hmax,
                      'Periodo medio ascendente': Tazm,
                      'Hs': Hs,
                      'espectro': espectro}

