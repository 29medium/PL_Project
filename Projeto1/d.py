import re


def printPais():
    print("\n--------------")
    print("     Pais     ")
    print("--------------\n")


def printMaes():
    print("\n--------------")
    print("     Maes     ")
    print("--------------\n")


pais = dict()
maes = dict()
processes = set()

contentRE = re.compile(
    r'<processo id="(\d+)">(.|\n)*?<pai>(.+)</pai>(.|\n)*?<mae>(.+)</mae>')

with open("processos.xml") as f:
    file = f.read()
    content = re.findall(contentRE, file)

for line in content:
    if line[0] not in processes:
        processes.add(line[0])

        pai = line[2]
        mae = line[4]

        if pai in pais:
            pais[pai] += 1
        else:
            pais[pai] = 1

        if mae in maes:
            maes[mae] += 1
        else:
            maes[mae] = 1

pais = dict((k, v) for k, v in sorted(
    pais.items(), key=lambda p: p[1], reverse=True)[:10] if v > 1)

maes = dict((k, v) for k, v in sorted(
    maes.items(), key=lambda p: p[1], reverse=True)[:10] if v > 1)

printPais()
for pai in pais.items():
    print(pai[0] + ": " + str(pai[1]))

printMaes()
for mae in maes.items():
    print(mae[0] + ": " + str(mae[1]))
