function nivel = calcularNivel (puntuacion)
   nivel = (exp(puntuacion/2000) - 1)*3;
end