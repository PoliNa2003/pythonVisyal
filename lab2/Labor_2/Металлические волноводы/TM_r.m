%волна E - типа (TM - волна)
%рисование дисперсионных кривых 
%в прямоугоьном волноводе

clc
clear






%размеры волновода
a = 3; % (cm)
b = 1; % (cm)
fm = 50; %максимальная частота (GHz)
eGHz = 1.e+9; %один гигаГерц
c = 3.e+10; %скорость света (cm/s)

%индексы волноводной моды
n=1;  m=1;  

%частота отсечки
f_nm = c/2*sqrt((n/a)^2 + (m/b)^2)/eGHz; % (GHz)

%находим постоянную распространения 'bet' для моды E_11
f1=f_nm:0.01:fm;
bet1 = 2*pi/c*eGHz*sqrt(f1.^2 - f_nm^2);


%индексы волноводной моды
n=1;  m=2;  

%частота отсечки
f_nm = c/2*sqrt((n/a)^2 + (m/b)^2)/eGHz; % (GHz)

%находим постоянную распространения 'bet' для моды E_12
f2=f_nm:0.01:fm;
bet2 = 2*pi/c*eGHz*sqrt(f2.^2 - f_nm^2);


%индексы волноводной моды
n=2;  m=1;  

%частота отсечки
f_nm = c/2*sqrt((n/a)^2 + (m/b)^2)/eGHz; % (GHz)

%находим постоянную распространения 'bet' для моды E_21
f3=f_nm:0.01:fm;
bet3 = 2*pi/c*eGHz*sqrt(f3.^2 - f_nm^2);


%индексы волноводной моды
n=2;  m=2;  

%частота отсечки
f_nm = c/2*sqrt((n/a)^2 + (m/b)^2)/eGHz; % (GHz)

%находим постоянную распространения 'bet' для моды E_22
f4=f_nm:0.01:fm;
bet4 = 2*pi/c*eGHz*sqrt(f4.^2 - f_nm^2);


%находим асимптотику bet = 2*pi/c*f
f0=0:0.01:fm;
bet0 = 2*pi/c*eGHz*f0;





hPl=plot(f1,bet1,f2,bet2,f3,bet3,f4,bet4,f0,bet0,'--');
set(hPl,'LineWidth',4);
grid on
%функция gca возвращает дескриптор текущих осей координат (гарафический объект axis)  
hAxes = gca;
%функция set устанавливает метки вдоль оси 'x' координатных осей hAxes
%set(hAxes,'xtick',[1.5 1.75 2.0 2.25 2.5])
set(hAxes,'FontSize',20,'FontWeight','bold');


%устанавливаем метку на оси 'x' текущих осей координат
xlabel('f     (GHz)')
%устанавливаем метку на оси 'y' текущих осей координат
ylabel('\beta     (1/cm)')

text(11.0, 0.5,'E_{11}','Color',[0 0 0],'FontSize',20,'FontWeight','bold')
text(26.0, 0.5,'E_{12}','Color',[0 0 0],'FontSize',20,'FontWeight','bold')
text(19.0, 0.5,'E_{21}','Color',[0 0 0],'FontSize',20,'FontWeight','bold')
text(33.0, 0.5,'E_{22}','Color',[0 0 0],'FontSize',20,'FontWeight','bold')
title('Dispersion Relation     \beta  =  \beta (f)')


