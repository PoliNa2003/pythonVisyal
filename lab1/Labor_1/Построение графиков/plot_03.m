%рисуетс€ график функции < r = 2.2*sin(3*phi) > в пол€рных координатах


clc   %clears all  from the Command Window
clear %removes all variables from the workspace (memory) 

phi = 0:0.01:pi;   
r = 2.2 *sin(3*phi);  

polar(phi,r)

