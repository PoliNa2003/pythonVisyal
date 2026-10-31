
%в одном окне (figure 1) рисуется два раза один и тотже график
%разными стилями


clc   %clears all  from the Command Window
clear %removes all variables from the workspace (memory) 

x = 0:0.1:3;  y = sin(x);
plot(x,y,'r-',x,y,'ko');

