import re
from graphviz import Digraph

dot = Digraph()
processes = set()
idP = 0

def incrementa():
    global idP
    idP += 1
    return str(idP)

while True:
    data = input("Introduzir ano >> ")
    try:
        data = int(data)
        break
    except ValueError:
        print("Valor Inválido")

familyRE = re.compile(r'([a-zA-Z, ]+),(Irmao|Irmaos)\.[ ]?Proc\.(\d+)')
contentRE = re.compile(
    r'<processo id="(\d+)">(.|\n)*?<data>((\d{4})-\d{2}-\d{2})</data>(.|\n)*?<nome>(.+)</nome>(.|\n)*?<pai>(.+)</pai>(.|\n)*?<mae>(.+)</mae>(.|\n)*?(<obs>((.|\n)*?)</obs>|<obs/>)')

with open("processos.xml") as f:
    file = f.read()
    content = re.findall(contentRE, file)

for line in content:
    if line[0] not in processes:
        processes.add(line[0])
        year = int(line[3])

        if year == data:
            linha = re.sub(r'( |\n)+', r' ', line[12].strip())
            family = re.findall(familyRE, linha)
            idfilho = incrementa()
            idmae = incrementa()
            idpai = incrementa()
            dot.node(idfilho,line[5])
            dot.node(idpai,line[7])
            dot.node(idmae,line[9])
            dot.edge(idpai, idfilho)
            dot.edge(idmae, idfilho)

            for relativeGroup in family:
                grau = relativeGroup[1]
                processes.add(relativeGroup[2])

                relatives = re.split(' e| e |, |,', relativeGroup[0])

                for relative in relatives:
                    idirmao = incrementa()
                    dot.node(idirmao,relative)
                    dot.edge(idpai,idirmao)
                    dot.edge(idmae,idirmao) 



dot.render('output/graph.gv', view=True)
