import re


def toSingular(group):
    return individualGrupo[group]


file = open('processos.xml', 'r')

next(file)
next(file)

familiaresIndividuais = ["Irmao", "Tio Materno", "Sobrinho Materno", "Tio Paterno",
                         "Sobrinho Paterno", "Tio Avo Materno", "Tio Avo Paterno",
                         "Avo Materno", "Avo Paterno", "Bisavo Materno", "Bisavo Paterno",
                         "Primo", "Primo Paterno", "Primo Materno"]

familiaresGrupos = ["Irmaos", "Primos", "Tios Paternos", "Tios Maternos",
                    "Sobrinhos Maternos", "Sobrinhos Paternos"]

individualGrupo = {"Irmaos": "Irmao", "Primos": "Primo", "Tios Paternos": "Tio Paterno",
                   "Tios Maternos": "Tio Materno", "Sobrinhos Maternos": "Sobrinho Materno", "Sobrinhos Paternos": "Sobrinho Paterno"}

familyRE = re.compile(
    r'(<obs>|\. )(((\w+| )+),({}).)'.format('|'.join(familiaresIndividuais) + '|' + '|'.join(familiaresGrupos)))

withFamily = 0

frequencyFamily = {}

for line in file:
    m = re.findall(familyRE, line.strip())

    if m:
        withFamily += 1

        for relativeGroup in m:
            print(relativeGroup)
            relative = relativeGroup[3]
            grau = relativeGroup[4]

            if relative in familiaresGrupos:
                familiares = relativeGroup[2].split('e')
                numFamiliares = familiares.size()
                if relative in frequencyFamily:
                    frequencyFamily[toSingular(grau)] += numFamiliares
                else:
                    frequencyFamily[toSingular(grau)] = numFamiliares

            else:
                if relative in frequencyFamily:
                    frequencyFamily[grau] += 1
                else:
                    frequencyFamily[grau] = 1

print("Numero de candidatos com parentes eclásticos: " + withFamily)

print("Tipo de parentesco mais frequente: " +
      max(stats.iteritems(), key=operator.itemgetter(1))[0])

file.close()
