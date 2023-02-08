## importar arquivo functions.py da pasta functions
import openai
import argparse
import os
import webbrowser
from train import *

os.environ["PYTHONIOENCODING"] = "utf-8"
model = "text-davinci-003"
temperature=0
max_tokens=300
key = "..."
nameUser = "User"

parser = argparse.ArgumentParser() # cria um objeto para receber os argumentos
## Chave da API
parser.add_argument("-k", "--key", help="Sua chave da OpenAI.", type=str)
## O Nome do usuário
parser.add_argument("-n", "--user", help="O seu nome.", type=str)

def main():

    ## FUNÇÃO PARA CRIAR IMAGEM
    def createImage(prompt, size="1024x1024"):
        response = openai.Image.create(
        prompt=prompt,
        n=1,
        size=size,
        )
        response = response['data'][0]['url']
        # Abre a imagem criada no navegador
        webbrowser.open(response)

    ## Função executar chat
    def creatCompletion(model, prompt, temperature, max_tokens, train, respostas):
        response = openai.Completion.create(
            model=model,
            prompt=train + respostas + "Você: " + prompt,
            temperature=temperature,
            max_tokens=max_tokens
        )
        response = response["choices"][0]["text"]
        return response

    ## FUNÇÃO PARA EXECUTAR COMANDOS
    def executeCommand(command):
        os.system(command)

    ## FUNÇÃO PARA LIMPAR O CONSOLE
    def clearConsole():
        os.system("cls")


    ## EXECUTAR O CHAT ##
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

## Executa a função main() se o arquivo for executado diretamente
if __name__ == "__main__":
    args = parser.parse_args()
    if args.key:
        key = args.key
        print("Chave de API redefinida", openai.api_key)
    if args.user:
        nameUser = args.user
        print("Novo usuário definido: " + nameUser)
    openai.api_key = key ## Chave da API
    ## Configura o treinamento
    train = train.replace("{nameUser}", nameUser).replace("{cunstomTrain}", cunstomTrain.replace("{nameUser}", nameUser))
    ## Imprime a ajuda sobre os argumentos
    parser.print_help()
    print("........Chat iniciazado........")
    main()