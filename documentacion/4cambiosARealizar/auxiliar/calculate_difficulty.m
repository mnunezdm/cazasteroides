function dificulty = calculate_difficulty(probability, seeing, n_votes)
    p_probability = 1/probability;
    p_seeing = seeing;
    p_n_votes = log((n_votes) + 1)-1;
    
    if n_votes ~= 0
        p_n_votes = 1/n_votes;
    end
    
    dificulty = p_probability*0.45 + p_seeing*0.1 - p_n_votes*0.45;
end