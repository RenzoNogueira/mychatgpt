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
respostasCurtidas = ""

parser = argparse.ArgumentParser()  # cria um objeto para receber os argumentos
## Chave da API
parser.add_argument("-k", "--key", help="Sua chave da OpenAI.", type=str)
## O Nome do usuário
parser.add_argument("-n", "--user", help="O seu nome.", type=str)


def main():
    global respostas

    ## GERAR IMAGEM
    def generatImage(promptImage, size, n = 4):
        try:
            response = openai.Image.create( prompt=promptImage, n=n, size=size)  # Cria a imagem
            if response['data'] != []:
                for i in response['data']:
                    webbrowser.open(i['url']) # Abre a imagem criada no navegador
        except openai.error.OpenAIError as e:
            print('## Ocorreu um erro ao criar a imagem ##')
            print('Erro: ', e.error['message'])
            print('Tipo: ', e.error['type'])

    ## ENTRADA PARA CRIAÇÃO DE IMAGEM
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
        generatImage(promptImage, size)
        input("Coninuar...")
        print("1 - Reecriar imagem com o mesmo prompt")
        print("2 - Criar nova imagem")
        print("3 - Voltar ao chat")
        op = input("Opção: ")
        if op == "1":
            print("Digite a quantidade de imagens que deseja criar")
            n = int(input("Quantidade(1/10): "))
            generatImage(promptImage, size, n)
        elif op == "2":
            createImage()

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
        print("!dislike - Descurtir a resposta do chat")
        print("!exit - Sair do chat")
        print("!export - Exportar o treinamento")
        print("!help - Mostrar os comandos disponíveis")
        print("!image - Criar uma imagem")
        print("!import - Importar um treinamento")
        print("!like - Curtir a resposta do chat")
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
            print("Esolha o tipo de arquivo")
            print("1 - Buscar conversas salvas")
            print("2 - Buscar respostas curtidas")
            op = input("Opção: ")
            if op == "1":
                importTrain(input("Nome do arquivo: "), False)
            elif op == "2":
                importTrain(input("Data do arquivo(dd-mm-aaaa): "), True)
        elif command == "!reset":
            resetTrain()
        elif command == "!like":
            like()
        elif command == "!dislike":
            dislike()

    ## CURTIR A RESPOSTA
    def like():
        ## Pega as ultimas 2 respostas do chat
        global respostas
        global respostasCurtidas
        global nomeUser
        resposta = respostas.split(nameUser + ": ")
        ## Salva a ultima resposta do chat
        respostasCurtidas += nameUser + ": " + resposta[1]
        ## Verifica se existe a pasta tempResponses
        if not os.path.exists("tempResponses"):
            os.makedirs("tempResponses")
        ## Cria o arquivo txt com as respostas curtidas
        date = datetime.now().strftime("%d-%m-%Y")
        with open("tempResponses/" + date + ".txt", "w", encoding="utf-8") as file:
            file.write(respostasCurtidas)

    ## DESCURTIR A RESPOSTA
    def dislike():
        ## Remove a ultima resposta do chat
        global respostas
        resposta = respostas.split(nameUser + ": ")
        textRespostas = ""
        respostaRemovida = ""
        for i in range(len(resposta) - 1): ## Remove a ultima resposta
            textRespostas += nameUser + ": " + resposta[i]
        respostaRemovida = resposta[len(resposta) - 1]
        respostas = textRespostas
        print("Resposta removida com sucesso!")
        print("-------------------------------------")
        ## Impressão a ultima resposta do chat
        print(nameUser + ": " + respostaRemovida)
        print("-------------------------------------")


    ## EXPORTAR O TREINAMENTO
    def exportTrain():
        dataAtual = datetime.now().strftime("%d-%m-%Y")
        # Verifica se existe a pasta saves
        if not os.path.exists("saves"):
            os.makedirs("saves")
        # Cria o arquivo json com o treinamento
        with open("saves/train_" + dataAtual + ".txt", "w", encoding="utf-8") as file:
            file.write(respostas)
        # Verifica se o arquivo foi criado
        if os.path.exists("saves/train_" + dataAtual + ".json"):
            print("Treinamento exportado com sucesso!")
            print("Arquivo: train_" + dataAtual + ".json")
        else:
            print("Erro ao exportar o treinamento!")

    ## IMPORTAR O TREINAMENTO
    def importTrain(nameFile, curtidas = False):
        global respostas
        if curtidas:
            # Verifica se existe a pasta tempResponses
            if not os.path.exists("tempResponses"):
                os.makedirs("tempResponses")
            # Verifica se o arquivo existe
            if os.path.exists("tempResponses/" + nameFile + ".txt"):
                # Abre o arquivo
                with open("tempResponses/" + nameFile + ".txt", "r", encoding="utf-8") as file:
                    # Pega o conteudo do arquivo
                    respostas = file.read()
                print("Treinamento importado com sucesso!")
            else:
                print("Arquivo " + nameFile + ".txt não encontrado!")
        else:
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

        respostas += prompt + response + "<|endoftext|>"
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
