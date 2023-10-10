from django.shortcuts import render
from django.http import HttpResponse
import subprocess
import os

def home(request):
    return render(request,'biopw/home.html')

def modelagem(request):
    return render(request,'biopw/modelagem.html')

def proteina(request):
    return render(request, 'biopw/proteina.html')

def executar_pipeline(request):
    output = ""
    
    script_path = '/home/antonio/Desktop/Byo-front/src/app/script/BioPyPW.py'

    try:
        resultado = subprocess.run(['python3.10', script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if resultado.returncode == 0:
            output = resultado.stdout
        else:
            output = f"Erro ao executar o script: {resultado.stderr}"
    except Exception as e:
        output = f"Erro ao executar o script: {str(e)}"

    return render(request, 'biopw/modelagem.html', {'output': output}) 
    

#resultado = subprocess.run(['python3.10', '/home/antonio/Desktop/Byo-front/src/app/script/BioPyPW.py'], cwd=script_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
