 
%Рисование поверхностей в 3D-графике


clc   %clears all  from the Command Window
clear %removes all variables from the workspace (memory) 


x = -2:0.1:2;
y = -1:0.1:1;

%превращают вектора u и v в соответствующие матрицы X и Y   
[X,Y] = meshgrid(x,y);
Z = exp(-X.^2 - Y.^2);


%функция plot3 рисует массив 3D-линий по заданным точкам
%стилем заданным по умолчанию и еще !!!
%функция plot3 возвращает массив дескрипторов hPlot3 графического объекта line
hPlot3 = plot3(X,Y,Z);
title('plot3');
pause

%функция set устанавливает новые атрибуты объекта line
set(hPlot3,'Color',[1.0 0.0 0.0],'LineWidth', 2);
title('plot3');
pause

%функция set устанавливает для линий с номерами 5-10 новые атрибуты объекта line
set(hPlot3(5:10),'Color',[0.0 1.0 0.0],'LineWidth', 3);
title('plot3');
pause

%рисуем сетку в текущих координатных осях
grid on
title('plot3');
pause

%устанавливаем метку на оси 'x' текущих осей координат
xlabel('x')
%устанавливаем метку на оси 'y' текущих осей координат
ylabel('y')
%устанавливаем метку на оси 'z' текущих осей координат
zlabel('z')
title('plot3');
pause

%функция mesh рисует поверхность типа mesh по заданным точкам
%стилем заданным по умолчанию и еще !!!
%функция mesh возвращает дескриптор hMesh графического объекта mesh
hMesh = mesh(X,Y,Z);
title('mesh');
pause

%функция set устанавливает новые атрибуты объекта mesh
set(hMesh,'LineWidth',2.0);
title('mesh');
pause

%показываются невидимые линии поверхности
hidden off
title('mesh hidden off');
pause

%показываются невидимые линии поверхности
hidden on
title('mesh hidden on');
pause

%функция surf рисует поверхность типа surf по заданным точкам
surf(X,Y,Z);
title('surf');
pause


%функция surfl рисует поверхность типа surfl по заданным точкам
surfl(X,Y,Z);
title('surfl');
pause

%выбираем окраску типа autumn
colormap(autumn)
title('autumn');
pause

%выбираем окраску типа colorcube
colormap(colorcube)
title('colorcube');
pause

%выбираем окраску типа cool
colormap(cool)
title('cool');
pause

%выбираем окраску типа flag
colormap(flag)
title('flag');
pause


%выбираем окраску типа gray
colormap(gray)
title('gray');
pause

%выбираем окраску типа hot
colormap(hot)
title('hot');
pause

%выбираем окраску типа hsv
colormap(hsv)
title('hsv');
pause

%выбираем окраску типа jet
colormap(jet)
title('jet');
pause

%выбираем окраску типа lines
colormap(lines)
title('lines');
pause

%выбираем окраску типа pink
colormap(pink)
title('pink');
pause

%выбираем окраску типа prism
colormap(prism)
title('prism');
pause

%выбираем окраску типа spring
colormap(spring)
title('spring');
pause

%выбираем окраску типа summer
colormap(summer)
title('summer');
pause


%выбираем окраску типа white
colormap(white)
title('white');
pause


%выбираем окраску типа winter
colormap(winter)
title('winter');
pause


%выбираем окраску типа copper
colormap(copper)
title('copper');
pause

%убрать ребра секи на поверхности
shading interp








