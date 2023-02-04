## importar arquivo functions.py da pasta functions
import sys
sys.path.append('config')
from settings import *
sys.path.append('utils')
from utils import *

respostas = ""
while True:
    # Limpa o console
    prompt = input("Você: ")
    # Verifica se o comando é para criar uma imagem
    if prompt == "criar imagem":
        # exibir lista 1: '256x256', 2: '512x512', 3: '1024x1024'
        tamanhos = {
            "1": "256x256",
            "2": "512x512",
            "3": "1024x1024",
        }
        for key, value in tamanhos.items():
            print(key,":", value)
        size = input("Tamanho da imagem: ")
        size = tamanhos[size]
        promptImage = input("Descrição da imagem: ")
        createImage(promptImage, size)
        continue
    response = creatCompletion(model, prompt, temperature, max_tokens, train, respostas)
    
    # Verifica se no texto contem chaves
    if "{" in response:
        # Pega o texto entre chaves
        comand = response.split("{")[1].split("}")[0]
        # Executa o comando
        executeCommand(comand)

    respostas += response
    print(response)