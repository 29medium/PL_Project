import re

def yearToCent(yearList):

    centList = [(int(year) // 100) + 1 for year in yearList]

    return list(dict.fromkeys(centList))

def printNumProcessYear(item):
    print(f'No ano ' + '\033[1m' + item[0] + '\033[0m' + ' foram registados ' + '\033[1m' + str(item[1]) + '\033[0m' + ' processos.')

def printNumCent(numCent):
    print(f'\nExistem registos de ' + '\033[1m' + str(numCent) + ' séculos' + '\033[0m' + ' diferentes.')

def printDateRange(firstDate, lastDate):
    print(f'\nHá registos entre ' + '\033[1m' + firstDate + '\033[0m' + ' e ' '\033[1m' + lastDate + '\033[0m' + '.')

file = open('processos.xml', 'r')


next(file)
next(file)

numProcessesYear = {}
minDate = '9999-99-99'
maxDate = '0000-00-00'

for line in file:
    m = re.search(r'^<data>((\d{4})-\d{2}-\d{2})', line.strip())

    if m:
        year = m.group(2)
        date = m.group(1)

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



file.close()
