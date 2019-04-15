y = zeros(1, 50);
for x1 = 1:50
    if x1 < 10
        y(x1) = 1;
    elseif x1 < 20
        y(x1) = 2;
    elseif x1 < 30
        y(x1) = 3;
    elseif x1 < 40
        y(x1) = 4;
    else
        y(x1) = 5;
    end
end

plot(1:50, y)