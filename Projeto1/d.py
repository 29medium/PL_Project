import re

name = input("Introduzir nome do pai ou da mãe >> ")

candidates = 0
processes = set()

contentRE = re.compile(
    r'<processo id="(\d+)">(.|\n)*?<pai>(.+)</pai>(.|\n)*?<mae>(.+)</mae>')

with open("processos.xml") as f:
    file = f.read()
    content = re.findall(contentRE, file)

for line in content:
    if line[0] not in processes:
        processes.add(line[0])

        if (line[2] == name) or (line[4] == name):
            candidates += 1

print(f"\nO pai ou mãe tem {candidates} filhos candidatos")
