function puntos = puntosHastaNivel (nivel)
    N = 1:nivel
    puntos = sum(log((N/3)+1) * 2000);
end