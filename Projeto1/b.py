import re


def printPrimeiro():
    print('\n---------------------------------')
    print('5 Primeiros Nomes mais frequentes')
    print('---------------------------------')


def printApelidos():
    print('\n---------------------------------')
    print('5 Últimos Nomes mais frequentes')
    print('---------------------------------')


def printSeculo(sec):
    print('\nSÉCULO ' + '\033[1m' + str(sec))


def printNome(nome, valor):
    print('Nome ' + '\033[1m' + nome +
          '  \033[0m' + ' Valor ' + '\033[1m' + str(valor))


file = open('processos.xml', 'r')

next(file)
next(file)

seculo = 0
seculoPrimeiro = {}
seculoUltimo = {}

nomeRE = re.compile(r'^<nome>(([a-zA-Z]+ )([a-zA-Z]+ )*([a-zA-Z]+))</nome>')
dataRE = re.compile(r'^<data>((\d{4})-\d{2}-\d{2})</data>')

for line in file:
    nome = re.search(nomeRE, line.strip())
    data = re.search(dataRE, line.strip())

    if data:
        seculo = int(data.group(2)) // 100 + 1

    if nome:
        primeiro = nome.group(2)
        ultimo = nome.group(4)

        if seculo not in seculoPrimeiro:
            seculoPrimeiro[seculo] = {}
            seculoUltimo[seculo] = {}

        if primeiro in seculoPrimeiro[seculo]:
            seculoPrimeiro[seculo][primeiro] += 1
        else:
            seculoPrimeiro[seculo][primeiro] = 1

        if ultimo in seculoUltimo[seculo]:
            seculoUltimo[seculo][ultimo] += 1
        else:
            seculoUltimo[seculo][ultimo] = 1

seculoPrimeiro = dict(sorted(seculoPrimeiro.items(),
                             key=lambda p: p[0], reverse=True))
seculoUltimo = dict(sorted(seculoUltimo.items(),
                           key=lambda p: p[0], reverse=True))

for sec in seculoPrimeiro.keys():
    seculoPrimeiro[sec] = dict(
        sorted(seculoPrimeiro[sec].items(), key=lambda p: p[1], reverse=True)[:5])

for sec in seculoUltimo.keys():
    seculoUltimo[sec] = dict(
        sorted(seculoUltimo[sec].items(), key=lambda p: p[1], reverse=True)[:5])

printPrimeiro()
for sec in seculoPrimeiro.keys():
    printSeculo(sec)
    for item in seculoPrimeiro[sec].items():
        printNome(item[0], item[1])

printApelidos()
for sec in seculoUltimo.keys():
    printSeculo(sec)
    for item in seculoUltimo[sec].items():
        printNome(item[0], item[1])

file.close()
