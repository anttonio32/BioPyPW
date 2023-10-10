import os 
import requests
from Bio.PDB import *

sequencia="/home/antonio/Desktop/Byo-front/src/app/script/1BGA.fasta" 
baseDeP="/home/antonio/Desktop/Byo-front/src/app/script/rcsb_pdb.txt"
diretorio="/home/antonio/Desktop/"

os.system("blastp -query "+sequencia+" -subject "+baseDeP+" -outfmt=6 > resultado.txt")

resultado=open("resultado.txt").readlines()

maior=0
identidade=''
id_maior=''

for linha in resultado: 
    colunas=linha.split("\t")
    
    atual=float(colunas[11])
    identidade=float(colunas[2])
    
    if atual > maior:
        if identidade > 25:
            maior = atual
            id_maior=colunas[1]
            cadeia="A"
            id_maior=id_maior[0:4]

print("O PDB template é: "+id_maior+" (IDENTIDADE = "+str(identidade)+"% - SCORE = "+str(maior)+")")

#Download do arquivo PDB
url="https://files.rcsb.org/download/"+id_maior+".pdb"
r=requests.get(url)
w=open(id_maior+".pdb","w")
w.write(r.text) 
w.close()

print("Baixado o arquivo .PDB")

#Download do arquivo FASTA
url2="https://www.rcsb.org/fasta/entry/"+id_maior
f=requests.get(url2)
w=open(id_maior+".fasta","w")
w.write(f.text)
w.close()

print("Baixado o arquivo .FASTA")

print("Saindo do Blast e entrando no Clustalw")

print("--------------------------------------------------------------------------------------")

#--------------------------Clustal--------------------------
#Alinhamento das sequencias

comeco = 2
fim = 448

os.system("cat "+id_maior+".fasta > alinha.fasta")
os.system("cat "+sequencia+" >> alinha.fasta")

# run clustal-w
os.system("clustalw -infile='alinha.fasta' -output='pir'")

aln = open("alinha.pir").readlines()
new_aln = open("new_alinha.pir","w")

tipo = 0 #0 = PDB; 1 = SEQ
seq = open(sequencia)
seq_final = ""

for linha in seq:
    if linha[0] != ">":
        seq_final += linha.strip()
tamanho_seq = len(seq_final)
print ("tamanho da seq = "+str(tamanho_seq))


#Formato ideal pra o modeller
for linha in aln:
    if linha[0] == ">":
        if tipo == 0 and linha != "\n":
            new_aln.write(">P1;"+id_maior+"\n")
            new_aln.write("structure:"+id_maior+":"+str(comeco)+":"+cadeia+":"+str(fim)+":"+cadeia+"::::")
            tipo = tipo+1
        elif tipo == 1:
            new_aln.write(">P1;1BGA\n")
            new_aln.write("sequence:1BGA:"+str(1)+":A:"+str(tamanho_seq)+":A::::")
    else:
        new_aln.write(linha)
new_aln.close()

new_aln = open("new_alinha.pir").read()
new_aln1 = open("new_alinha.pir","w")

new_aln2 = new_aln.replace("M","-",1)
new_aln1.write(new_aln2)
new_aln1.close()

print("Saindo do Clustalw e entrando no modeller")

print("--------------------------------------------------------------------------------------")


#-----------------------MODELLER----------------------------
#Modelagem por homologia
#Criando um script python(modeller) dentro de um script python(pipeline)
w = open("run.py","w")


#Script de automacao do modeller 
script = "\
#-*- coding:utf-8 -*-\n\
from modeller import *\n\
from modeller.automodel import *\n\
\n\
log.verbose()\n\
env = environ()\n\
\n\
env.io.atom_files_directory = ['/home/antonio/Desktop']\n\
\n\
env.io.hetatm = True\n\
env.io.water = True\n\
\n\
a = automodel(env, alnfile = 'new_alinha.pir', knowns = '"+id_maior+"', sequence = '1BGA')\n\
a.starting_model = 1\n\
a.ending_model = 2\n\
a.make() \n\
"
w.write(script)
w.close()

#codego do terminal para execucao do modeller 
os.system("mod10.4 run.py")

print("Saindo do Modeller e entrando no melhor modelo")

print("--------------------------------------------------------------------------------------")

#-------------------------------Melhor Modelo------------------------------
#seleciona o melhor modelo gerado pelo software

menor = 999999999999
menor_id = ''
for _, _, arquivos in os.walk(diretorio):
    for arquivo in arquivos:
        if arquivo[-4:] == ".pdb":
            try:
                linha = open(arquivo).readlines()
                score = linha[1]
                score = float(score[40:])
                if score < menor:
                    menor = score
                    menor_id = arquivo
            except:
                print ("Modelo inválido")
print ("O melhor modelo é "+menor_id)
print("fim da execução")