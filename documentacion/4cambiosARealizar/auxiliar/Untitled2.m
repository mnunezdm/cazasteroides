
vote_punt = zeros(1,100);
for n_votes = 1:100
%     vote_punt(n_votes) = 1/(log((n_votes-1) + 1)+0.75);
    vote_punt(n_votes) = log(n_votes/3);
end

plot(vote_punt)