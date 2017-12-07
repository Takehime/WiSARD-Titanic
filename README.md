# WiSARD-Titanic

Trabalho final da disciplina Redes Neurais Sem Peso - UFRJ 2017.2

Integrantes: Silvia Pimpão Vasquez e Vinícius Garcia Silva da Costa


**Dataset utilizado**

https://www.kaggle.com/c/titanic/data


**Para rodar**

Executar a Main.py seguida da escolha dos seguintes parâmetros:

    [T (key)]: Train with 80% of training set and test on the other 20%
    [T* (key*)]: Same as T, but tests with every num_bits_address in the range (0, 20)
    [G (key)]: Train with the entirety of the training set and test on the test set, generating a file 'result.csv' in Resources folder.
    [C (num_of_folds) (key)]: Cross-Validation with the given number of folds.
    
    Key format: [num_bits_addr, (0, 1), (0, 1), (0, 6), (0, 6), (0, 1), (0, 3), (0, 3), (0, 3)]
    Key* format: [(0, 1), (0, 1), (0, 6), (0, 6), (0, 1), (0, 3), (0, 3), (0, 3)]
