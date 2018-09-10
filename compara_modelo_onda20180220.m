clear all;
close all;
clc;

disp('**********************************************')
disp('     Rotina para comparacao das rodadas       ')
disp('       do modelo DELFT3D nos modulos          ')
disp('         hidrodinamico +  ondas               ')
disp('     Criado por Aline Lemos de Freitas        ')
disp('    Data da ultima alteracao: 19/02/2018      ')
disp('**********************************************')
disp('                                              ')
% pergunta = 'n';

% ******************************************
%
%   USANDO A MESMA ROTINA QUE USEI PRA 
%  LER OS DADOS DE ENTRADO DO HIDRODINAMICO
%
% *******************************************
fonte = 14;     % fontsize

pergunta = input('Comparar resultados do modelo hidrodinamico? (s/n)  ', 's');
[M, i, estacoes] = ler_entrada(pergunta);

% DEFININDO PREFIXOS 
DM.OPTVAR = {'hs', 'tp', 'dir',  'MainDir'}; %'Hmax', 'Tm',  'MainDir'
%************************************************
%
% abrindo o arquivo Dados de onda
%  Data; Hm0; H10; Hmax; Tp; Tm02; DirTp; SprTp; MainDir
%
%************************************************
[filename, pathname] = uigetfile('*.csv', ...
    'Escolha o arquivo do AWAC');
fid = fopen([pathname, filename], 'rt');
a = textscan(fid, '%s %f %f %f %f %f %f %f %f', ...
      'Delimiter',';', 'CollectOutput',1, 'HeaderLines',1);
fclose(fid);

format short g;
onda = [datenum(a{1}, 'DD/mm/YYYY HH:MM') a{2}];

% ****************************************************
%
%         CRIANDO UMA ESTRUTURA COM TODAS AS 
%                INFORMACOES DO AWAC
%
% ****************************************************
D.datenum = onda(:,1);
% DADOS DO AWAC TAMBEM ESTAO EM UTC???
% TRANSFORMANDO PARA HORA LOCAL
% IGUAL AO MODELO
D.datenum = D.datenum - 0.1249992;
D.datestr = datestr(D.datenum, 31);
D.hs = onda(:,2);
D.Hmax = onda(:,4);
D.Tm = onda(:,6);
D.Tp = onda(:, 5);
D.dir = onda(:, 7);
D.dir = D.dir - 19.5;
D.MainDir = onda(:, 9);
D.MainDir = D.MainDir - 19.5;
D.dt = D.datenum(2) - D.datenum(1);


% ESCOLHENDO UM PONTO DE SAIDA DO MODELO 
% PARA COMPARAR COM A SERIE DO AWAC
disp(M(1).estacoes);
est=input('Escolha a estacao para comparar a serie     ', 's');
est = str2num(est);

%
%      CORTANDO A SERIE DO MODELO 
%  PARA COINCIDIR COM O TEMPO DO AWAC
%
% Selecionando o periodo de dados do AWAC
% pra comparar o mesmo periodo de tempo do modelo
ini = find(M.datenum == D.datenum(1));
ifim = find(M.datenum == D.datenum(end));
M.datestrcrop = M.datestr(ini:ifim);
M.datenumcrop = M.datenum(ini:ifim);
M.hscrop = M.hs(ini:ifim,est);
% criando Hmax no modelo so para comparar com 
% Hmax do dado
M.Hmaxcrop = M.hs(ini:ifim, est);
M.tpcrop = M.tp(ini:ifim,est);
M.Tmcrop = M.tp(ini:ifim, est);
M.dircrop = M.dir(ini:ifim,est);
M.MainDircrop = M.dir(ini:ifim, est);
%M(i).Tmcrop = M(i).Tm(ini:ifim, est);



%
%       INTERPOLANDO O DADO DO AWAC
%
if M(1).dt ~= D.dt;
%     datev = gregorian(julian([2011 7 31 14 10 0]):10/(24*60):julian(...
%         [2011 8 2 13 10 0]));
% Automatizando a etapa acima
    datev = gregorian(julian([str2num(D.datestr(1,1:4)) ...
                              str2num(D.datestr(1,6:7)) ...
                              str2num(D.datestr(1,9:10)) ...
                              str2num(D.datestr(1,12:13)) ...
                              str2num(D.datestr(1,15:16)) ...
                              str2num(D.datestr(1,18:19))]):10/(24*60): ...
                              julian([str2num(D.datestr(end,1:4)) ...
                              str2num(D.datestr(end,6:7)) ...
                              str2num(D.datestr(end,9:10)) ...
                              str2num(D.datestr(end,12:13)) ...
                              str2num(D.datestr(end,15:16)) ...
                              str2num(D.datestr(end,18:19))]));
    D.dateinterp = datenum(datev);
    % determinando o time step dp modelo e 
    % do dado para interpolar
    %dtD = round((D.dt * 24 * 60));
    %dtM = round((M(i).dt * 24 * 60));
    X = (1:1:length(D.hs));
    D.hsinterp = interp1(D.datenum, D.hs, D.dateinterp);
    D.dirinterp = interp1(D.datenum, D.dir, D.dateinterp);
    D.tpinterp = interp1(D.datenum, D.Tp, D.dateinterp);
    % O vetor tempo tem 283 linhas, o de dados 
    % (hs, tp, dir) ficaram com 288 linhas, 
    % sendo que as ultimas decaem de valor
    % por isso cortei o vetor interpolado ate 
    % a linha 283
    %
    % When filtering, resample assumes that the input 
    % sequence, x, is zero before and after the samples 
    % it is given. Large deviations from zero at the 
    % endpoints of x can result in unexpected values for y.
%     D.hsinterp = D.hsinterp(1:283);
%     D.Hmaxinterp = resample(D.Hmax, dtD, dtM);
%     D.Hmaxinterp = D.Hmaxinterp(1:283);
%     D.tpinterp = resample(D.Tp,dtD,dtM);
%     D.tpinterp = D.tpinterp(1:283);
%     D.dirinterp = resample(D.dir,dtD,dtM);
%     D.dirinterp = D.dirinterp(1:283);
     D.MainDirinterp = interp1(D.datenum, D.MainDir, D.dateinterp);
%     D.MainDirinterp = D.MainDirinterp(1:283);
%     D.Tminterp = resample(D.Tm, dtD, dtM);
%     D.Tminterp = D.Tminterp(1:283);
else
    D.hsinterp = D.hs;
    D.dateinterp = D.datenum;
end

destdir = [pathname 'Figures'];
if ~isdir(destdir)
    mkdir(destdir);
end
% COMPARANDO MODELO COM O AWAC
% TUDO QUE FOR DO MODELO TEM QUE SER
% CROP E TUDO QUE FOR DADO TEM QUE SER
% INTERP

FigH = figure('Position', get(0, 'Screensize'));
plot(M(i).datenumcrop,M(i).hscrop, '-b*')
hold on
plot(D.dateinterp, D.hsinterp, '--ro')
%plot(D.datenum, D.hs, '--ro')
ylabel('Significant Wave Height (m)', 'FontSize', fonte)
datetick('x','mm/dd HH:MM', 'keeplimits')
legend('Hs Modelo', 'Hs AWAC - PC')
set(gca,'FontSize',fonte);
F    = getframe(FigH);
saveas(gcf, [destdir, 'compara_hs.png'])


FigH = figure('Position', get(0, 'Screensize'));
plot(M(i).datenumcrop,M(i).tpcrop, '-b*')
hold on
plot(D.dateinterp, D.tpinterp, '--ro')
ylabel('Peak Period (s)', 'FontSize', fonte)
datetick('x','mm/dd HH:MM', 'keeplimits')
legend('Tp Modelo', 'Tp AWAC - PC')
set(gca,'FontSize',fonte);
F    = getframe(FigH);
saveas(gcf, [destdir, 'compara_Tp.png'])



% figure('FigSize', 230);
FigH = figure('Position', get(0, 'Screensize'));
plot(M(i).datenumcrop,M(i).dircrop, '-b*')
hold on
plot(D.dateinterp, D.MainDirinterp, '--ro')
ylabel('Wave Direction (degrees)', 'FontSize', fonte)
datetick('x','mm/dd HH:MM', 'keeplimits')
legend('Dir Modelo', 'Maind Dir AWAC - PC')
set(gca,'FontSize',fonte)
F    = getframe(FigH);
saveas(gcf, [destdir, 'compara_direc.png'])




FigH = figure('Position', get(0, 'Screensize'));
plot(D.datenum, D.hs, '-bo')
hold on;
plot(D.dateinterp, D.hsinterp, '--r')
datetick('x','mm/dd HH:MM', 'keeplimits')
legend('Data', 'Interpolated')
set(gca,'FontSize',fonte)
F    = getframe(FigH);
saveas(gcf, [destdir, 'interpolado.png'])


% i eh o contador de rodadas na entrada
% PARA QUANDO TIVER MAIS DE UMA SAIDA DO MODELO DE ONDA
% VER SE VAI SER INTERESSANTE
%figure();
%for k=1:i;
%    plot(M(k).datenum, M(k).hs(:,est),'color',rand(1,3), 'line', '--');
%    hold on
%end
%legend(M.des)
%ylabel('Water Level (m)');


% ESTATISTICAS DA FERNANDA
% Quando eu pergunto o ponto que eu quero comparar
% e corto a serie de acordo com o tempo de medicao
% do awac, eu transformo a serie de hs, tp e dir em
% uma variavel 1D (hscrop, tpcrop, dircrop)
% S = estatistics
% AInda nao esta funcionando

% S.Omean.hs = nanmean(D.hsinterp, 1);
% S.Omean.Hmax = nanmean(D.Hmaxinterp, 1);
% S.Omean.Tm = nanmean(D.Tminterp, 1);
% S.Omean.Tp = nanmean(D.Tpinterp, 1);
% S.Omean.dirtp = nanmean(D.dirtpinterp, 1);
% S.Omean.MainDir = nanmean(D.MainDirinterp, 1);

for i = 1:length(DM.OPTVAR)
    interp = [DM.OPTVAR{i}, 'interp'];
    crop = [DM.OPTVAR{i}, 'crop'];
    S.Omean.(DM.OPTVAR{i}) = nanmean(D.(interp),1);
    S.Ostd.(DM.OPTVAR{i}) = nanstd(D.(interp),1);
    S.Mmean.(DM.OPTVAR{i}) = nanmean(M.(crop), 1);
    S.Mstd.(DM.OPTVAR{i})  = nanstd(M.(crop), 1);
    
    
    S.absuRMSE.(DM.OPTVAR{i}) = sqrt(nanmean(((M.(crop)-...
        S.Mmean.(DM.OPTVAR{i}))- ...
        (D.(interp)- S.Omean.(DM.OPTVAR{i}))).^2));
    
    S.uRMSE.(DM.OPTVAR{i}) = sign(S.Mstd.(DM.OPTVAR{i})-...
        S.Ostd.(DM.OPTVAR{i}))* ...
        sqrt(nanmean(((M.(crop)- S.Mmean.(DM.OPTVAR{i}))- ...
        (D.(interp)- S.Omean.(DM.OPTVAR{i}))).^2));
    
    S.RMSE.(DM.OPTVAR{i}) = sqrt(nanmean((M.(crop)- ...
        D.(interp)).^2));
    
    S.R2.(DM.OPTVAR{i}) = ((nansum((M.(crop)-...
        S.Mmean.(DM.OPTVAR{i})).*(D.(interp)-...
        S.Omean.(DM.OPTVAR{i})))./(length(M.(crop))-1))/...
        (S.Mstd.(DM.OPTVAR{i})*S.Ostd.(DM.OPTVAR{i})))^2;
    
    S.bias.(DM.OPTVAR{i})  = S.Mmean.(DM.OPTVAR{i})-...
        S.Omean.(DM.OPTVAR{i});
end

destdir = [pathname 'Processed'];
if ~isdir(destdir)
    mkdir(destdir);
    save([destdir ['\statsmodelo_onda_', date, '.mat']], '-struct', 'S');
else
    save([destdir ['\statsmodelo_onda_', date, '.mat']], '-struct', 'S');
end


% S.Ostd = nanstd(D.hsinterp,1);
% S.Omean(ii,j) = nanmean(DM.(OPT.varname));
% S.Ostd(ii,j)  = nanstd(DM.(OPT.varname));

%S.Mmean(ii,j) = nanmean(model);
% S.Mmean apresenta linhas rodadas por colunas estacoes
% vai me dar uma valor medio por rodada por estacao
%k = 1;
% for k=1:i; % i eh o numero total de rodadas do modelo na entrada
    
    
    %for j=estacoes;
    %S.absuRMSE(ii,j) = sqrt(nanmean(((model-S.Mmean(ii,j))-(DM.(OPT.varname)-S.Omean(ii,j))).^2));
    % RMSE calculado por estacao
    % nao precisava ja que eu so tenho previsao de mare proximo da costa
    %S.absuRMSE(k, 1) = sqrt(nanmean(((M(k).hscrop-S.Mmean)- ...
    %    (D.hsinterp- S.Omean)).^2));
    
    
    %S.uRMSE(ii,j) = sign(S.Mstd(ii,j)-S.Ostd(ii,j))* ...
    %          sqrt(nanmean(((model-S.Mmean(ii,j))- ...
    %          (DM.(OPT.varname)-S.Omean(ii,j))).^2));
    %S.uRMSE(k,:) = sign(S.Mstd-S.Ostd)* ...
    %    sqrt(nanmean(((M(k).hscrop- S.Mmean)- ...
    %    (D.hsinterp- S.Omean)).^2));
    %S.RMSE(ii,j)  = sqrt(nanmean((model-DM.(OPT.varname)).^2));
    %S.RMSE(k,1) = sqrt(nanmean((M(k).hscrop- ...
    %    D.hsinterp).^2));
    
    %S.R2(ii,j)=((nansum((model-S.Mmean(ii,j)).*(DM.(OPT.varname)-...
    % S.Omean(ii,j)))./(length(model)-1))/(S.Mstd(ii,j)*S.Ostd(ii,j)))^2;
    %S.R2(k,1) = ((nansum((M(k).hscrop-S.Mmean).*(D.hsinterp-...
    %    S.Omean))./(length(M(k).hscrop)-1))/(S.Mstd*S.Ostd))^2;
    
    
    % S.bias(ii,j)  = S.Mmean(ii,j)-S.Omean(ii,j);
    % um valor de bias para cada estacao de observacao
    %S.bias(k,1)  = S.Mmean-S.Omean;
    
    
    % MESMA COISA PARA O PERIODO. EH MEIO BURRO DE SE FAZER 
    % ASSIM, MAS MAIS FACIL DE ACESSAR OS RESULTADOS

%end
dado = [];
header = [];
for i = 35:1:39;
    hs = []; tp = []; dir=[]; label = [];
    for j=1;
        hs = M(j).hs(:,i);
        tp = M(j).tp(:,i);
        dir = M(j).dir(:,i);
    end
    for j=2;
        hs = [hs; M(j).hs(:,i)];
        tp = [tp; M(j).tp(:,i)];
        dir = [dir; M(j).dir(:,i)];
        label = {['hs', num2str(i)], ['tp', num2str(i)], ...
            ['dir', num2str(i)]};
   
    end
    header = [header label];
    dado = [dado hs tp dir];
end

[filename, pathname] = uiputfile('*.csv', 'Save Workspace as');


csvwrite([pathname, filename], header);    
