% bright

x_bright = 5:0.1:25;
N_bright = length(x_bright);
y_bright = zeros (N_bright, 1);

for k = 1:N_bright
     y_bright(k) = 100 * (1 / (1 + (exp(1) ^ -(0.6 * (x_bright(k) - 15)))));
end

figure(1)
plot (x_bright,y_bright)

% fwhm

x_fwhm = -5:0.1:5;
N_fwhm = length(x_seing);
y_fwhm = zeros (N_fwhm, 1);

for k = 1:N_fwhm
     y_fwhm(k) = 200 * (1 / (1 + (exp(1) ^ -(x_fwhm(k)) + 1)));
end

figure(2)
plot (x_fwhm,y_fwhm)

