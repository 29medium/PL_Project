import re


def isPlural(member):
    return (member[-1] == 's')


def toSingular(plural):
    singular = re.sub(r'(s )', r' ', plural)
    return re.sub(r's$', r'', singular)


contentRE = re.compile(
    r'<processo id="(\d+)">(.|\n)*?(<obs>((.|\n)*?)</obs>|<obs/>)')
familyRE = re.compile(r'(([a-zA-Z, ]+),([A-Z][a-zA-Z ]+))\.[ ]?Proc\.\d+')

withFamily = 0
frequencyFamily = dict()
processes = set()

with open("processos.xml") as f:
    file = f.read()
    content = re.findall(contentRE, file)

for line in content:
    if line[0] not in processes:
        processes.add(line[0])

        linha = re.sub(r'( |\n)+', r' ', line[2].strip())
        family = re.findall(familyRE, linha)

        if family:
            withFamily += 1

            for relativeGroup in family:
                grau = relativeGroup[2]
                numFamiliares = 1

                if isPlural(grau):
                    relatives = re.split(' e| e |, |,', relativeGroup[1])
                    numFamiliares = len(relatives)
                    grau = toSingular(grau)

                if grau in frequencyFamily:
                    frequencyFamily[grau] += numFamiliares
                else:
                    frequencyFamily[grau] = numFamiliares


print("Numero de candidatos com parentes eclesiásticos: " + str(withFamily) + "\n")

ff = dict(sorted(frequencyFamily.items(), key=lambda p: p[1], reverse=True))

for item in ff.items():
    print(str(item[0]) + ": " + str(item[1]))

print("\nTipo de parentesco mais frequente: " +
      max(frequencyFamily.items(), key=lambda p: p[1])[0])
