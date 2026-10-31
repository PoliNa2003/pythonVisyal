  
%постороение 3D-линии, заданной в параметрическом виде


clc   %clears all  from the Command Window
clear %removes all variables from the workspace (memory) 


t = 0:pi/50:10*pi;
x = sin(t);
y = cos(t);
z = t;

%функция plot3 рисует 3D-линию по заданным точкам
%стилем заданным по умолчанию и еще !!!
%функция plot3 возвращает дескриптор hPlot3 графического объекта line
hPlot3 = plot3(x,y,z);
pause

%функция set устанавливает новые атрибуты объекта line
set(hPlot3,'Color',[0.0 1.0 1.0],'LineWidth', 7);
pause
%рисуем сетку в текущих координатных осях
grid on
pause

%устанавливаем метку на оси 'x' текущих осей координат
xlabel('x')
%устанавливаем метку на оси 'y' текущих осей координат
ylabel('y')
%устанавливаем метку на оси 'z' текущих осей координат
%возвращает дескриптор hZlable графического объекта zlable
hZlable = zlabel('z');
pause
%функция set устанавливает новые атрибуты объекта zlable
set(hZlable,'Color',[1.0 0.5 0.0],'FontSize',[24]);





