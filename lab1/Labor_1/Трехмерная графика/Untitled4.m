
clc   %clears all  from the Command Window
clear %removes all variables from the workspace (memory) 


xb = -2.0; xe = 2.0;
yb = -1.0; ye = 1.0;

x = [];
y = [];
z = [];
x = xb:0.1:xe;
y = yb:0.1:ye;

N = length(x);
M = length(y);
for(i=1:N)
    for(j=1:M)
        z(i,j) = exp(-(x(i)*x(i) + y(j)*y(j)));
    end
end

%превращают вектора u и v в соответствующие матрицы X и Y   
[X,Y] = meshgrid(x,y);
%Z = exp(-X.^2 - Y.^2);
%Z(3,:)
mesh(X,Y,z');

xs

