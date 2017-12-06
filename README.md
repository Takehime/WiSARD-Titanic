# WiSARD-Titanic

Trabalho final da disciplina Redes Neurais Sem Peso - UFRJ 2017.2
Integrantes: Silvia Pimpão Vasquez e Vinícius Garcia Silva da Costa

**Dataset utilizado**

https://www.kaggle.com/c/titanic/data

**Para rodar**

Executar a Main.py seguida da escolha dos seguintes parâmetros:

    [T]: Treina apenas os primeiros 80% do dataset de treinamento e testa com os 20% restantes da mesma base. (num_bits_addr = 5)

    [T*]: Mesmo que o T porém testa com todos os números de bits de endereçamente no intervalo (0, 40).

    [G (n)]: Treina com toda a base de dados de teste e gera um arquivo 'result.csv' na pasta 'Resources' possibilitando o envio do mesmo ao Kaggle. Usa 'n' como num_bits_addr.

    [CW (n) (g) (s)]: Realiza o treinamento pela ClusWiSARD, sendo 'n' o número de bits de endereçamento, 'g' o coeficiente de crescimento e 's' o score minímo.

    [C (k)]: Realiza o treinamento utilizando Cross-Validation, onde 'k' é o número de folds utilizados.
