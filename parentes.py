import re


file = open('processos.xml', 'r')

next(file)
next(file)


family = re.compile(r',(\w+( \w+)?)\.')

withFamily = 0

frequencyFamily = {}

for line in file:

    m = re.findall(family, line)

    if m:
        withFamily += 1
        print(m)
        # print(m.group(3), m.group(4))

        for relative in m:
            if relative in frequencyFamily:
                frequencyFamily[relative] += 1
            else:
                frequencyFamily[relative] = 1

print(withFamily)
print(frequencyFamily)


file.close()
