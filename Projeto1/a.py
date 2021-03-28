import re


def yearToCent(yearList):
    centList = [(int(year) // 100) + 1 for year in yearList]

    return list(dict.fromkeys(centList))


def printNumProcessYear(item):
    print(f'No ano ' + '\033[1m' + item[0] + '\033[0m' + ' foram registados ' +
          '\033[1m' + str(item[1]) + '\033[0m' + ' processos.')


def printNumCent(numCent):
    print(f'\nExistem registos de ' +
          '\033[1m' + str(numCent) + ' séculos' + '\033[0m' + ' diferentes.')


def printDateRange(firstDate, lastDate):
    print(f'\nHá registos entre ' + '\033[1m' + firstDate +
          '\033[0m' + ' e ' '\033[1m' + lastDate + '\033[0m' + '.')


minDate = '9999-99-99'
maxDate = '0000-00-00'
numProcessesYear = dict()
processes = set()

contentRE = re.compile(
    r'<processo id="(\d+)">(.|\n)*?<data>((\d{4})-\d{2}-\d{2})</data>')

with open("processos.xml") as f:
    file = f.read()
    content = re.findall(contentRE, file)

for line in content:
    if line[0] not in processes:
        processes.add(line[0])

        date = line[2]
        year = line[3]

        if date < minDate:
            minDate = date
        elif date > maxDate:
            maxDate = date

        if year in numProcessesYear:
            numProcessesYear[year] += 1
        else:
            numProcessesYear[year] = 1

numProcessesYear = dict(sorted(numProcessesYear.items(), key=lambda p: p[0]))

numCent = len(yearToCent(numProcessesYear.keys()))

for item in numProcessesYear.items():
    printNumProcessYear(item)

printNumCent(numCent)
printDateRange(minDate, maxDate)
