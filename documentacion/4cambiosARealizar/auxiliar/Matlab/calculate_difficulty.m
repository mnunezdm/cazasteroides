function dificulty = calculate_difficulty(p, s, b, n_votes)
    p = 100 - p
    s = 100 * (1 / (1 + (exp(1) ^ -(s) + 1)))
    b = 100 * (1 / (1 + (exp(1) ^ -(0.6 * (b - 15)))))
    
    static = 1/3 * p + 1/3 * s + 1/3 * b
    
    dynamic = 0
    
    difficulty = static - dynamic
end