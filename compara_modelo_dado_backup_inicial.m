%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%      ROTINA PARA VISUALIZACAO, COMPARACAO E DEMAIS 
%              ANALISES DO RESULTADO DO MODELO
%             
%             CRIADA POR ALINE LEMOS DE FREITAS
%                       EM 26/09/2017
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

clear all;
close all;
clc;

% LENDO OS ARQUIVOS DE SAIDA DO MODELO
[filename, pathname] = uigetfile('wav*.dat', 'Escolha o arquivo de map');
wavm = vs_use([pathname,filename]);


[filename, pathname] = uigetfile('trih*.dat', 'Escolha o arquivo hist');
trih = vs_use([pathname,filename]);


[filename, pathname] = uigetfile('*.grd', 'Escolha o arquivo de grid');
G = wlgrid('read', [pathname, filename]);

[filename, pathname] = uigetfile('*.dep', 'Escolha o arquivo de profundidades');
depth = wldep('read', [pathname,filename], G);


[filename, pathname] = uigetfile('*.csv', 'Escolha o arquivo da previsao de mare');
fid = fopen([pathname, filename], 'rt');
a = textscan(fid, '%s %f', ...
      'Delimiter',';', 'CollectOutput',1, 'HeaderLines',1);
fclose(fid);

format short g;
previsao = [datenum(a{1}) a{2}];

% Montando uma variavel estruturada para todos os dados do modelo e 
% depois fazer a mesma coisa pro dado
% Valor de Hs para todos os pontos de observacao
% vs_get cria uma estrutura com o tamanho do tempo e "variaveis internas"
% do tamanho do numero de pontos de observacao
% vs_let cria uma unica variavel de tempo x ponto de observacao
M.hs      = vs_let(trih, 'his-wav-series', 'ZHS'); %hs = hs(5:end, :);
M.wl      = vs_let(trih, 'his-series', 'ZWL'); %wl = wl(5:end, :);  
M.names   = splitcellstr(vs_get(trih, 'his-const', 'NAMST'));
M.names = strtrim(M.names);
% M.TZONE   = vs_let(trih, 'his-const', 'TZONE');
% resultados a cada 10 min
M.time    = gregoria(julian(2011,7,1):10/(24*60):julian(2011,8,31));
M.datenum = datenum(M.time);
M.datenum = M.datenum - 0.1249992;
M.datestr = datestr(M.datenum);
% Passando de UTC para hora local na marra



% Leitura dos dados
D.time = previsao(:,1);
D.datestr = datestr(D.time);
D.wl = previsao(:,2);



% PLOTANDO A DIFERENCA DE AMPLITUDE ENTRE AS MODELAGENS
for i = 1:1:40
plot(M.datenum, M.wl(:,i), M.datenum, M.wl10cm(:,i), 'r--', M.datenum, M.wl50cm(:,i), 'g--');
legend('Water Level', 'Water Level -10cm', 'Water Level -50cm');
title(M.names(i,:));
print([pathname, 'ponto_', num2str(i)], '-dpng');
%savefig([pathname, 'ponto_', num2str(i)])
close('all')
end




% PARA CORRIGIR A DIFERENCA DE TIMEZONE
% Fix to PDT and PST 
% 'America/Los_Angeles'
% nao esta implementado. nao funciona no Matlab 2014
t1 = datetime(M.datenum,'TimeZone','Belem, Brazil');
t1 = datetime(datestr(M.datenum),'TimeZone','America/Los_Angeles');
%[dt,dst] = tzoffset(t1);
%M.dateshift(1,:) = M.datenum;
%M.dateshift(2,:) = datenum(dt);
%M.datenum        = sum(M.dateshift,1);


% Normalizando a saida do modelo de Hs
% usando a formula z = x - min(x)/max(x)-min(x)
[m, n] = size(M.hs);
M.hs_norm = zeros(m, n);
for i = 1:n
X = M.hs(:,i);
xmin = min(X); xmax=max(X);
x_std = (X - xmin) ./ (xmax - xmin);
x_scaled = x_std .* (1+1) + (-1);
M.hs_norm(:,i) = x_scaled;
end

% Mesma coisa pro Water Level
[m, n] = size(M.wl);
M.wl_norm = zeros(m, n);
for i = 1:n
X = M.wl(:,i);
xmin = min(X); xmax=max(X);
x_std = (X - xmin) ./ (xmax - xmin);
x_scaled = x_std .* (1+1) + (-1);
M.wl_norm(:,i) = x_scaled;
end


plot(M.wl_norm(:, 2), 'r--');
hold on;
plot(M.hs_norm(:, 2));
title(['Ponto ', names(2, :)]);


% ESTATISTICAS DA FERNANDA
% S = estatistics
% AInda nao esta funcionando
S.Omean = nanmean(D.wl, 1);
% quem eh i e quem eh j? Faz para cada ponto de saida do modelo?
% quem eh opt.varname?
% S.Omean(ii,j) = nanmean(DM.(OPT.varname));
% S.Ostd(ii,j)  = nanstd(DM.(OPT.varname));

%S.Mmean(ii,j) = nanmean(model);
% media do water level para cada um dos 40 pontos de observacao
S.Mmean = nanmean(M.wl, 1);
%S.Mstd(ii,j)  = nanstd(model);
S.Mstd  = nanstd(M.wl, 1);

%S.absuRMSE(ii,j) = sqrt(nanmean(((model-S.Mmean(ii,j))-(DM.(OPT.varname)-S.Omean(ii,j))).^2));
S.absuRMSE = sqrt(nanmean(((M.wl-S.Mmean)-(DM.(OPT.varname)-S.Omean)).^2));

S.uRMSE(ii,j) = sign(S.Mstd(ii,j)-S.Ostd(ii,j))*sqrt(nanmean(((model-S.Mmean(ii,j))-(DM.(OPT.varname)-S.Omean(ii,j))).^2));
S.RMSE(ii,j)  = sqrt(nanmean((model-DM.(OPT.varname)).^2));

% S.R2(ii,j)    = ((nansum((model-S.Mmean(ii,j)).*(DM.(OPT.varname)-S.Omean(ii,j)))./(length(model)-1))/(S.Mstd(ii,j)*S.Ostd(ii,j)))^2;
S.R2 = ((nansum((M.wl-S.Mmean).*(DM.(OPT.varname)-S.Omean(ii,j)))./(length(model)-1))/(S.Mstd(ii,j)*S.Ostd(ii,j)))^2;
% S.bias(ii,j)  = S.Mmean(ii,j)-S.Omean(ii,j);
% um valor de bias para cada estacao de observacao
S.bias  = S.Mmean-S.Omean;




% ??????????????????????????????????????????????????????????
% ??????????????????????????????????????????????????????????
%     Plotando a batimetria
% 
surf(G.X, G.Y, -depth(1:end-1, 1:end-1));
shading flat;   % tira as linhas de grid
view(-60,30)  % muda a angulacao da imagem
set(gca, 'da', [1 1 1/300])   % mudou a escala??
camlight


