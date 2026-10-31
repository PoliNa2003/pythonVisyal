%Полиномы Чебышева

x=-1.5:0.01:1.5;
y1=cos(acos(x));
y2=cos(2*acos(x));
y3=cos(3*acos(x));
y4=cos(4*acos(x));
%y=cosh(n*acosh(x));


hPl=plot(x, y1, x, y2, x, y3, x, y4);
set(hPl,'LineWidth',4);
axis([-1.5 1.5 -3 3]);
hy=line([0 0], [-3 3]);   %ось Oy
set(hy,'LineWidth',2,'color','black');
hx=line( [-1.5 1.5], [0 0]);   %ось Ox
set(hx,'LineWidth',2,'color','black');
hAx=gca;
set(hAx,'FontSize',[18]);
text( -1.45, -0.8, 'n=1','FontSize',[20]);
text( -1.45, 1.2, 'n=2','FontSize',[20]);
text( -0.95, -2.2, 'n=3','FontSize',[20]);
text( -0.95, 2.2, 'n=4','FontSize',[20]);
title('Chebyshev Polynomials','FontSize',[20]);

grid on;

