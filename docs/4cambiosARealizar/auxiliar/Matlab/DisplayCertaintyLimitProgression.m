x = 1:50;
N = length(x);
y = zeros(1,N);

for x1 = 1:N
    y(x1) = calculate_certainty_limit(x1 - 1);
end

plot(x, y)