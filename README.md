*CENTRO FEDERAL DE EDUCAÇÃO TECNOLÓGICA DE MINAS GERAIS*
*ENGEHARIA DE COMPUTAÇÃO*
*LABORATÓRIO DE INTELIGÊNCIA ARTIFICAL*
*Prof. Flávio Cruzeiro*

####TRABALHO PRÁTICO 2: PACMAN MULTIAGENTE
######por Pedro Felipe Froes e Saulo Antunes

---

######Passo 1: Melhorando a função de avaliação do agente reflexivo

Pode-se combinar as variáveis de cada estado do jogo a fim de melhorar o `ReflexAgent` presente em `multiAgents.py`. Para criar um novo agente, combinou-se diversas variáveis diferentes, relacionando a distância mínima até o fantasma e comida mais próximos (`ghostScore` e `foodScore`, respectivamente), quantidade de comida (`remainingFoodScore`) e de tempo (`scaredTimeScore`) restante enquanto os fantasmas estão em estado _scared_ (estado após o Pacman comer uma cápsula), se o movimento do estado seguinte é _STOP_ (`stopScore`, com pontuação negativa) e a relação entre a quantidade de cápsulas consumidas entre o estado atual e o sucessor (`capsuleConsumedScore`).

Para combiná-las, foram testados empiricamente valores com o inverso do `foodScore`, por exemplo, e dando pesos maiores para variáveis como `remainingFoodScore` e `consumedCapsuleScore`. O `score` final foi então resultado da expressão:

```python
score = successorGameState.getScore() + foodScore/ghostScore + remainingFoodScore*10 + scaredTimeScore + capsuleConsumedScore*10 + stopScore
```

Os testes no tabuleiro `testClassic` geraram os seguintes resultados:

```
python pacman.py -p ReflexAgent -l testClassic
```

Já no tabuleiro _default_ com 1 e 2 fantasmas, os resultados obtidos foram:

```
python pacman.py --frameTime 0 -p ReflexAgent -k 1
```

```
python pacman.py --frameTime 0 -p ReflexAgent -k 2
```

*Como é o desempenho do seu agente?*
A SER RESPONDIDO

######Passo 2: Criando um agente de busca competitiva

