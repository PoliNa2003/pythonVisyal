%волна E - типа (TM - волна)
%рисование линий электрического и магнитного полей 
%в пр€моугоьном волноводе

clc
clear


%в сечении z = 0
%в момент времени t0
t0 = 1/8; % в единичах периода T


a = 3;
b = 1;

%задаем сетку в области [0 a 0 b]
%дл€ рисовани€ линий уровн€
dx = a/300;
dy = b/100;
[x,y] = meshgrid(0:dx:a, 0:dy:b);


%выбираем моду E_nm
n = 1;
m = 1;
z = sin(pi*n*x/a).*sin(pi*m*y/b)*sin(-2*pi*t0);    %Ёлектрический потенциал √ерца  

%рисует эквипотенциальные линии (линии магнитного пол€)
[C,hc] = contour(x,y,z);       
set(hc,'LineWidth',3,'Color',[0.3 0.3 0.8]);
axis([0 a 0 b]);
%clabel(C,hc)

%задаем сетку в области [0 a 0 b]
%дл€ рисовани€ линий градиента
dx = a/60;
dy = b/20;
[x,y] = meshgrid(0:dx:a, 0:dy:b);

z = sin(pi*n*x/a).*sin(pi*m*y/b)*sin(-2*pi*t0);    %Ёлектрический потенциал √ерца  

%находим минус градиент пол€ z(x,y)
[px,py] = gradient(-z);                  


hold on;
%рисует векторы градиента (электрическое поле)
h = quiver(x,y,px,py,1.5);     
set(h,'LineWidth',2,'Color',[0.8 0.3 0.3]);


%функци€ gca возвращает дескриптор текущих осей координат (гарафический объект axis)  
hAxes = gca;
%функци€ set устанавливает метки вдоль оси 'x' координатных осей hAxes
set(hAxes,'xtick',[0.0 0.5 1.0  1.5 2.0 2.5 3.0]);
set(hAxes,'ytick',[0.0 0.5 1.0]);
set(hAxes,'FontSize',20,'FontWeight','bold');

%устанавливаем метку на оси 'x' текущих осей координат
xlabel('x     (cm)')
%устанавливаем метку на оси 'y' текущих осей координат
ylabel('y     (cm)')

%title('Lines E and B fields')

strn = int2str(n);
strm = int2str(m);
string = ['Lines of E and B fields.  TM - mode, E_',strn,'_',strm];
title(string)

