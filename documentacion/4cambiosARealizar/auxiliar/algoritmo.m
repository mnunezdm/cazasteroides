% numero de niveles
n = 50;

% ppo
ppo = 100;

% nivel
N = 0:n;

% puntos por nivel
ppn = log((N/3)+1) * 350;

% observaciones por nivel
opn = round(ppn/ppo);

% puntos y observaciones hasta nivel
ptot = zeros(1,51);
otot = zeros(1,51);

for k = 1:n+1
    ptot(k) = sum(ppn(1:k));
    otot(k) = sum(opn(1:k));
end

subplot(2,2,1)
plot(N, ppn);
title('Puntos por nivel');
ylabel('Puntos');
xlabel('Niveles');

subplot(2,2,2);
plot(N, opn);
title('Observaciones por nivel');
ylabel('Observaciones');
xlabel('Niveles');

subplot(2,2,3)
plot(N, ptot);
title('Puntos hasta nivel');
ylabel('Puntos totales');
xlabel('Niveles');

subplot(2,2,4);
plot(N, otot);
title('Observaciones hasta nivel');
ylabel('Observaciones totales');
xlabel('Niveles');

