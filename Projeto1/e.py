import re

processes = set()

while True:
    data = input("Introduzir ano >> ")
    try:
        data = int(data)
        break
    except ValueError:
        print("Valor Inválido")

contentRE = re.compile(
    r'<processo id="(\d+)">(.|\n)*?<data>((\d{4})-\d{2}-\d{2})</data>(.|\n)*?<nome>(.+)</nome>(.|\n)*?<pai>(.+)</pai>(.|\n)*?<mae>(.+)</mae>')

with open("processos.xml") as f:
    file = f.read()
    content = re.findall(contentRE, file)

for line in content:
    if line[0] not in processes:
        processes.add(line[0])
        year = int(line[3])

        if year == data:
            nome = line[5]
            pai = line[7]
            mae = line[9]
