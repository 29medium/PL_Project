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


seculo = 0
seculoPrimeiro = dict()
seculoUltimo = dict()
processes = set()

contentRE = re.compile(
    r'<processo id="(\d+)">(.|\n)*?<data>((\d{4})-\d{2}-\d{2})</data>(.|\n)*?<nome>([a-zA-Z]+ )([a-zA-Z]+ )*([a-zA-Z]+)</nome>')

with open("processos.xml") as f:
    file = f.read()
    content = re.findall(contentRE, file)

for line in content:
    if line[0] not in processes:
        processes.add(line[0])

        seculo = int(line[3]) // 100 + 1
        primeiro = line[5]
        ultimo = line[7]

        if seculo not in seculoPrimeiro:
            seculoPrimeiro[seculo] = dict()
            seculoUltimo[seculo] = dict()

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
