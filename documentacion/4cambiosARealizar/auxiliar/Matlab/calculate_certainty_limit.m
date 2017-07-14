function certainty = calculate_certainty_limit(x)
    upper_limit = 0.75;
    lower_limit = 0.45;
    minimum_votes = 6;
    votes_to_minimum_certainty = 15 * 3;
    if x >= votes_to_minimum_certainty
        certainty = lower_limit;
    elseif x < minimum_votes
        certainty = upper_limit;
    else
        x = x - minimum_votes;
        certainty_difference = upper_limit - lower_limit;
        
        step = certainty_difference / (votes_to_minimum_certainty - minimum_votes);
        certainty = upper_limit - step * x;
        display(certainty);       
    end
         