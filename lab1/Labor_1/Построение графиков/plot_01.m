%в одно окне (figure 1) рисуется один график, затем стирается
%затем рисуется другой график


clc   %clears all  from the Command Window
clear %removes all variables from the workspace (memory) 

x = 0:0.1:2;
y = sin(x);

plot(x,y)

pause
clf   %deletes from the current figure all graphics objects  
pause

x = 0:0.1:2;
z = cos(x);

plot(x,z)

pause
cla   %deletes from the current axes all graphics objects and Clear current axes

 