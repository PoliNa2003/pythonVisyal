
%оформление графика с помощью дескрипторной графики
%дескрипторная графика имеет дело с базовыми графическими объектами
%дескрипторная графика это низкоуровневая графика системы MATLAB 


clc   %clears all  from the Command Window
clear %removes all variables from the workspace (memory) 

x = 0:0.1:3;  y = sin(x);

%функция plot рсует линию с параметрами по умолчанию и еще !!!
%функция plot возвращает дескриптор hPlot графического объекта line
hPlot = plot(x,y);
pause
%функция set устанавливает толщину линии связанной с дескриптором hPlot
set(hPlot, 'LineWidth', 7);

%функция get возвращает знаяение атрибута 'LineWidth' для линии hPlot
width = get(hPlot,'LineWidth')

%функция get возвращает знаяения всех атрибутов для линии hPlot
width = get(hPlot)




