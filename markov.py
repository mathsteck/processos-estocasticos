# Este codigo realiza simulacoes de caminhadas aleatorias em cadeias de Markov
# de acordo com a especificacao:

# Questão 2 Um grafo pode ser representado por uma matriz de adjacência, onde o elmento ai j = 1 se houver uma
# conexão entre os vértices i e j. Se i e j não estão conectados, então ai j = 0. Gere um grafo com N vértices considerando
# um processo de Bernoulli, isto é, estabeleça cada conexão com uma probabilidade p usando o método de Monte Carlo.
# Cada conexão deve ser testada uma única vez. Considere um grafo não-dirigido, ou seja, ai j = aji (note que você não
# precisa testar todas a conexões, mas metade delas).

# a) Obtenha a distribuição das conexões para N = 1000, p = 0,1 e p = 0,3. O formato desse histograma é familiar?
#    Justifique. O que deve acontecer se N for muito grande e p muito pequeno? Faça um teste.

# b) Para N = 500 e p = 0,2, simule uma caminhada aleatória nesse grafo. Isto é, partindo de cada vértice, a caminhada
#    ocorre segundo uma cadeia de Markov de tempo discreto, onde cada vértice representa um estado. Nesse caso, se um
#    vértice tem 2 conexões, a chance de mudar para cada um dos seus vizinhos é 50%. Note que a matriz de probabilidade
#    de transição pode ser obtida dividindo-se cada elemento da matriz de adjacência pelo soma da respectiva linha. Inicie
#    10 caminhadas de comprimento 50 em cada vértice e, para cada simulação, calcule o número de visitas a cada um dos
#    vértices da rede. Desse modo, obtenha o número médio de vezes que o processo vai passar por cada vértice. Obtenha um
#    gráfico do número de visitas em função do número de conexões. O que você pode concluir desse resultado?


#    Copyright (C) 2014  Matheus Steck Cardoso
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from random import random
import numpy as np
import matplotlib.pyplot as plt

def generate_matrix(N, p):
    # Cria uma matriz de zeros de tamanho N
    matrix = np.zeros(shape=(N,N))

    # Gera cada uma das conexoes do grafo. Neste caso e necessario gerar toda a matriz
    # Porque random.binomial gera uma lista que precisa ser do mesmo tamanho da
    # matriz
    for i in xrange(N):
        # Bernoulli e um caso especial da binomial com tamanho = 1
        matrix[i] = np.random.binomial(1, p, N)

    # Faz com que Aij = Aji (grafo nao direcionado)
    for i in xrange(N):
        for j in xrange(N):
            matrix[i][j] = matrix[j][i]

    return matrix

def show_histogram(N, matrix):
    averages = []

    for i in xrange(N):
        averages.append(np.average(matrix[i]))

    plt.hist(averages)
    plt.show()

def convert_to_markov(matrix, N):
    for i in xrange(N):
        # Conta o numero de conexoes da linha
        count = list(matrix[i]).count(1)
        for k in xrange(N):
            # Divide cada elemento da linha pelo numero de conexoes
            if count > 0:
                matrix[i][k] /= count
    return matrix

def walking(initial_vertex, matrix, N, n_steps):
    vertex_n_visits = [0] * N
    current_vertex = initial_vertex
    for k in xrange(n_steps):
        # Incrementa o numero de vizitas daquele vertice
        vertex_n_visits[current_vertex] += 1
        # Obtem uma lista de vertices que estao conectados ao vertice atual
        connections = np.flatnonzero(matrix[current_vertex])
        # Conta o numero de conexoes da linha
        n_connections = len(connections)
        # Gera uma lista com os valores de 0 ao numero de conexoes para
        # determinar qual dos vertices sera escolhido de acordo com o valor
        # aleatorio gerado
        n = range(1, n_connections)
        # Se nao houver nenhum valor naquela linha pare a caminhada
        if not n_connections:
            pass
        # Probabilidade de mudar de vertice
        p = 1.0 / n_connections
        # Gera um numero aleatorio entre 0 e 1
        x = random()

        # Encontra qual dos elementos deve ser escolhido a partir do
        # valor de x retirado anteriormente
        for j in n:
            # Verifica em qual intervalo de probabilidade x esta.
            # EX: se 0 <= x <= 0.3333 entao next_step = 0,
            #     se 0.3333 <= x <= 0.6666 entao next_step = 1,
            #     se 0.6666 <= x <= 1 entao next_step = 2
            if(j*p <= x <= (j+1)*p):
                # Caminha para o proximo valor conectado ao vertice atual
                current_vertex = connections[j]
                break

    return vertex_n_visits

def a():
    N = [10, 100, 1000, 2000, 4000, 8000]

    # Probabilidade de 0.1
    m1 = generate_matrix(N[2], 0.1)
    # Probabilidade de 0.3
    m2 = generate_matrix(N[2], 0.3)

    show_histogram(N[2], m1)
    show_histogram(N[2], m2)

    # Roda os testes para varios valores de N
    for i in N:
        # Probabilidade de 0.001
        m = generate_matrix(i, 0.001)
        show_histogram(i, m)

def b():
    N = 500

    m = generate_matrix(N, 0.2)
    m = convert_to_markov(m, N)

    # Dicionario em que o indice representa o numero de conexoes e o conteudo representa o
    # numero de visitas recebidas
    axis = dict.fromkeys(xrange(N))
    for i in xrange(N):
        axis[i] = 0

    # Para cada vertice
    for i in xrange(N):
        # Lista de zeros para fazer a media de vizitas
        n_visits = [0] * N
        # Calcula o numero de vizitas 10x
        for j in xrange(10):
            n_visits = np.add(n_visits, walking(i, m, N, 50))
        # Conta o numero de conexoes daquele vertice
        count = len(np.flatnonzero(m[i]))
        # Calcula a media de vizitas para aquele vertice
        total = n_visits[i] / 10
        # Soma o total de acordo com o numero de conexoes, ou seja, se tiver
        # 1 conexao ele ira somar ao endereco que armazena o total de vizitas
        # relativo a 1 conexao
        axis[count] += total

    # Faz a plotagem do grafico
    plt.plot(axis.values())
    plt.show()


def main():
    # Executa a questao a
    a()
    # Executa a questao b (essa e bem pesada e demora bastante para terminar)
    b()

if __name__ == "__main__":
    main()
