%в окне (figure 1) рисуется первый график, затем в том же окне
%рисуется второй график в общих осях
%затем в другом окне (figure 4) рисуется третий график


clc   %clears all  from the Command Window
clear %removes all variables from the workspace (memory) 

x = 0:0.1:2;   
y = sin(x);  

plot(x,y)

pause

x = 0:0.1:3;
z = cos(x);

hold on   %hold current graph in the figure
plot(x,z)
grid on   %adds major grid lines to the current axes

pause

x = 0:0.1:2;   
y = exp(x);  

figure(4)
plot(x,y)


