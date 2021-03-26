import re

file = open('processos.xml', 'r')

next(file)
next(file)

pais = {}
maes = {}

paiRE = re.compile(r'^<pai>(.+)</pai>')
maeRE = re.compile(r'^<mae>(.+)</mae>')

for line in file:
    paiSr = re.search(paiRE, line.strip())
    maeSr = re.search(maeRE, line.strip())
    if paiSr:
        pai = paiSr.group(1)
        if pai in pais:
            pais[pai] += 1
        else:
            pais[pai] = 1
    if maeSr:
        mae = maeSr.group(1)
        if mae in maes:
            maes[mae] += 1
        else:
            maes[mae] = 1

print("\nPais:\n")
for pai in pais.items():
    if pai[1] > 1:
        print(pai[0] + ": " + str(pai[1]))

print("\nMães:\n")
for mae in maes.items():
    if mae[1] > 1:
        print(mae[0] + ": " + str(mae[1]))

file.close()
