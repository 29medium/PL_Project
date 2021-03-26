import re
import operator


def isPlural(member):
    return (member[-1] == 's')


def toSingular(plural):
    singular = re.sub(r'(s )', r' ', plural)
    return re.sub(r's$', r'', singular)


obsRE = re.compile(r'<obs>((.|\n)*?)</obs>')
familyRE = re.compile(r'((.+),(.+))\. Proc')

withFamily = 0
frequencyFamily = {}

with open("processos.xml") as f:
    conteudo = f.read()
    obs = re.findall(obsRE, conteudo)

for line in obs:
    linha = re.sub(r'( |\n)+', r' ', line[0].strip())
    family = re.findall(familyRE, linha)

    if family:
        withFamily += 1

        for relativeGroup in family:
            grau = relativeGroup[2]
            numFamiliares = 1

            if isPlural(grau):
                relatives = re.split(' e |, ', relativeGroup[1])
                numFamiliares = len(relatives)
                grau = toSingular(grau)

            if grau in frequencyFamily:
                frequencyFamily[grau] += numFamiliares
            else:
                frequencyFamily[grau] = numFamiliares

print("Numero de candidatos com parentes eclesiásticos: " + str(withFamily))

print("Tipo de parentesco mais frequente: " +
      max(frequencyFamily.items(), key=operator.itemgetter(1))[0])
