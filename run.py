## importar arquivo functions.py da pasta functions
import openai
import argparse
import os
## importar modulo para data
from datetime import datetime
import webbrowser
from train import *

os.environ["PYTHONIOENCODING"] = "utf-8"
model = "text-davinci-003"
temperature = 0
max_tokens = 300
key = "..."
nameUser = "User"
respostas = ""

parser = argparse.ArgumentParser()  # cria um objeto para receber os argumentos
## Chave da API
parser.add_argument("-k", "--key", help="Sua chave da OpenAI.", type=str)
## O Nome do usuário
parser.add_argument("-n", "--user", help="O seu nome.", type=str)


def main():
    global respostas
    ## CRIAR IMAGEM
    def createImage():
        tamanhos = {  # Lista de tamanhos de imagens
            "1": "256x256",
            "2": "512x512",
            "3": "1024x1024",
        }
        for key, value in tamanhos.items():
            print(key, ":", value)
        size = input("Tamanho da imagem: ")
        size = tamanhos[size]
        promptImage = input("Descrição da imagem: ")
        responseImage = []
        for i in range(4):  # Loop para criar 4 imagens
            response = openai.Image.create( prompt=promptImage, n=1, size=size)  # Cria a imagem
            responseImage.append(response)  # Adiciona a imagem no array
        for response in responseImage:  # Pega a url da primeira imagem
            response = response['data'][0]['url']
            webbrowser.open(response)  # Abre a imagem criada no navegador

    ## EXECUTAR COMPLETION
    def creatCompletion(model, prompt, temperature, max_tokens, train, respostas):
        response = openai.Completion.create(
            model=model,
            prompt=train + respostas + "Você: " + prompt,
            temperature=temperature,
            max_tokens=max_tokens
        )
        response = response["choices"][0]["text"]
        return response

    ## EXECUTAR COMANDOS
    def executeCommand(command):
        os.system(command)

    ## LIMPAR O CONSOLE
    def clearConsole():
        os.system("cls")

    ## FUNÇÃO PARA MOSTRAR COMANDOS DISPONÍVEIS
    def help():
        print("Comandos disponíveis: ")
        print("!clear - Limpar o console")
        print("!help - Mostrar os comandos disponíveis")
        print("!exit - Sair do chat")
        print("!image - Criar uma imagem")
        print("!export - Exportar o treinamento")
        print("!import - Importar um treinamento")
        print("!reset - Resetar o chat")

    ## VERIFICAR COMANDOS
    def checkCommand(command):
        command = command.replace(nameUser + ": ", "").replace("<|endoftext|>", "")
        if command == "!clear":
            clearConsole()
        elif command == "!help":
            help()
        elif command == "!exit":
            exit()
        elif command == "!image":
            createImage()
        elif command == "!export":
            exportTrain()
        elif command == "!import":
            importTrain(input("Nome do arquivo: "))
        elif command == "!reset":
            resetTrain()

    ## EXPORTAR O TREINAMENTO
    def exportTrain():
        dataAtual = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        # Verifica se existe a pasta saves
        if not os.path.exists("saves"):
            os.makedirs("saves")
        # Cria o arquivo json com o treinamento
        with open("saves/train_" + dataAtual + ".json", "w", encoding="utf-8") as file:
            file.write(respostas)
        # Verifica se o arquivo foi criado
        if os.path.exists("saves/train_" + dataAtual + ".json"):
            print("Treinamento exportado com sucesso!")
            print("Arquivo: train_" + dataAtual + ".json")
        else:
            print("Erro ao exportar o treinamento!")

    ## IMPORTAR O TREINAMENTO
    def importTrain(nameFile):
        # Verifica se existe a pasta saves
        if not os.path.exists("saves"):
            os.makedirs("saves")
        # Verifica se o arquivo existe
        if os.path.exists("saves/" + nameFile):
            # Abre o arquivo
            with open("saves/" + nameFile, "r", encoding="utf-8") as file:
                # Pega o conteudo do arquivo
                respostas = file.read()
            print("Treinamento importado com sucesso!")
        else:
            print("Arquivo não encontrado!")

    ## RESETAR O CHAT
    def resetTrain():
        global train
        train = ""

    ## RECEBER PROMPT E PREPARAR ENVIO
    def getPrompt(inputPrompt):
        global nameUser
        return nameUser + ": " + inputPrompt + "<|endoftext|>"

    ## EXECUTAR O CHAT
    while True:
        prompt = getPrompt(input(nameUser + ": "))
        # Verificar se o prompt é um comando
        if prompt.replace(nameUser + ": ", "").startswith("!"):
            checkCommand(prompt)
            continue
        response = creatCompletion(model, prompt, temperature, max_tokens, train, respostas)

        # Verifica se no texto contem chaves
        if "{" in response:
            # Pega o texto entre chaves
            comand = response.split("{")[1].split("}")[0]
            # Executa o comando
            executeCommand(comand)

        respostas += prompt + "\n" + response + "<|endoftext|>\n"
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
    openai.api_key = key  ## Chave da API
    ## Configura o treinamento
    train = train.replace("{nameUser}", nameUser).replace("{cunstomTrain}",
                                                          cunstomTrain.replace("{nameUser}", nameUser))
    ## Imprime a ajuda sobre os argumentos
    parser.print_help()
    print("........Chat iniciazado........")
    main()
