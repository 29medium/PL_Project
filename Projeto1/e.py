import re

processes = set()

data = int(input("Introduzir ano >>"))

contentRE = re.compile(
    r'<processo id="(\d+)">(.|\n)*?<nome>(.+)</nome>(.|\n)*?<pai>(.+)</pai>(.|\n)*?<mae>(.+)</mae>')

with open("processos.xml") as f:
    file = f.read()
    content = re.findall(contentRE, file)

for line in content:
    if line[0] not in processes:
        processes.add(line[0])

        nome = line[2]
        pai = line[4]
        mae = line[6]
