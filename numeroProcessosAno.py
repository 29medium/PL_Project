import re

def yearToCent(yearList):

    centList = [(int(year) // 100) + 1 for year in yearList]

    return list(dict.fromkeys(centList))

file = open('processos.xml', 'r')

next(file)
next(file)

numProcessesYear = {}

for line in file:
    m = re.search(r'^<data>((\d{4})-(\d{2})-(\d{2}))', line.strip())

    if m:
        ano = m.group(2)

        if ano in numProcessesYear:
            numProcessesYear[ano] += 1
        else:
            numProcessesYear[ano] = 1

numProcessesYear = dict(sorted(numProcessesYear.items(), key=lambda p: p[0]))

numCent = len(yearToCent(numProcessesYear.keys()))


print(numProcessesYear)
print(numCent)

file.close()
