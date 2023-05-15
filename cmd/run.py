# importar arquivo functions.py da pasta functions
import openai
import argparse
import os
import json
# importar modulo para data
from datetime import datetime
import webbrowser
from train import *

os.environ["PYTHONIOENCODING"] = "utf-8"
model = "gpt-3.5-turbo"
temperature = 0
max_tokens = 300
key = "..."
nameUser = "User"
chatContent = [{
    "role": "assistant",
    "content": "Assistente: Olá, eu sou o seu asistente virtual, como posso te ajudar?"
}]
chatContentCurtidas = ""

parser = argparse.ArgumentParser()  # cria um objeto para receber os argumentos
# Chave da API
parser.add_argument("-k", "--key", help="Sua chave da OpenAI.", type=str)
# O Nome do usuário
parser.add_argument("-n", "--user", help="O seu nome.", type=str)

def main():
    global chatContent

    # GERAR IMAGEM
    def generatImage(promptImage, size, n = 4):
        try:
            response = openai.Image.create( prompt=promptImage, n=n, size=size)  # Cria a imagem
            if response['data'] != []:
                for i in response['data']:
                    webbrowser.open(i['url']) # Abre a imagem criada no navegador
        except openai.error.OpenAIError as e:
            print('# Ocorreu um erro ao criar a imagem #')
            print('Erro: ', e.error['message'])
            print('Tipo: ', e.error['type'])

    # ENTRADA PARA CRIAÇÃO DE IMAGEM
    def create_image():
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
            create_image()

    # EXECUTAR COMPLETION
    def creat_completion(model, prompt, temperature, max_tokens, train, chatContent):
        chatContent.append({
                    "role": "user",
                    "content": prompt
                })
        # Adiciona o treinamento na primeira posição do chatContent
        chatContent.insert(0, {
            "role": "system",
            "content": train
        })
        response = openai.ChatCompletion.create(
            model=model,
            # prompt=train + chatContent + "Você: " + prompt,
            messages=chatContent,
            temperature=0
        )
        response = response.choices[0].message
        return response

    # EXECUTAR COMANDOS
    def execute_command(command):
        os.system(command)

    # LIMPAR O CONSOLE
    def clear_console():
        os.system("cls")

    # FUNÇÃO PARA MOSTRAR COMANDOS DISPONÍVEIS
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

    # VERIFICAR COMANDOS
    def check_command(command):
        command = command.replace(nameUser + ": ", "").replace("<|endoftext|>", "")
        if command == "!clear":
            clear_console()
        elif command == "!help":
            help()
        elif command == "!exit":
            exit()
        elif command == "!image":
            create_image()
        elif command == "!export":
            export_train()
        elif command == "!import":
            print("Exemplo: C:/Users/Usuario/Desktop/train.txt")
            import_train(input("Localização do arquivo: "))
        elif command == "!reset":
            reset_train()
        elif command == "!like":
            like()
        elif command == "!dislike":
            dislike()

    # CURTIR A RESPOSTA
    def like():
        # Pega as ultimas 2 chatContent do chat
        global chatContent
        global chatContentCurtidas
        global nomeUser
        resposta = chatContent.split(nameUser + ": ")
        # Salva a ultima resposta do chat
        chatContentCurtidas += nameUser + ": " + resposta[len(resposta) - 1]
        # Verifica se existe a pasta _like_responses
        if not os.path.exists("_like_responses"):
            os.makedirs("_like_responses")
        # Cria o arquivo txt com as chatContent curtidas
        nameFile = datetime.now().strftime("%d-%m-%Y")
        with open("_like_responses/" + nameFile + ".txt", "w", encoding="utf-8") as file:
            file.write(chatContentCurtidas)

    # DESCURTIR A RESPOSTA
    def dislike():
        # Remove a última resposta do Chat
        global chatContent
        resposta = chatContent.split(nameUser + ": ")
        textchatContent = ""
        respostaRemovida = ""
        for i in range(len(resposta) - 1): # Remove a ultima resposta
            textchatContent += nameUser + ": " + resposta[i]
        respostaRemovida = resposta[len(resposta) - 1]
        chatContent = textchatContent
        print("Resposta removida com sucesso!")
        print("-------------------------------------")
        # Impressão a última resposta do Chat
        print(nameUser + ": " + respostaRemovida)
        print("-------------------------------------")


    # EXPORTAR O TREINAMENTO
    def export_train():
        nameFile = datetime.now().strftime("%d-%m-%Y")
        # Verifica se existe a pasta _saves
        if not os.path.exists("_saves"):
            os.makedirs("_saves")
        # Cria o arquivo txt com o treinamento
        with open("_saves/train_" + nameFile + ".txt", "w", encoding="utf-8") as file:
            file.write(chatContent)
        # Verifica se o arquivo foi criado
        if os.path.exists("_saves/train_" + nameFile + ".txt"):
            print("Treinamento exportado com sucesso!")
            print("Arquivo: train_" + nameFile + ".txt")
        else:
            print("Erro ao exportar o treinamento!")

    # SALVAR PROMPT NA PASTA TEMP
    def save_prompt(prompt):
        prompt = json.dumps(prompt)
        nameFile = datetime.now().strftime("%d-%m-%Y") # Prompts do dia atual
        # Verifica se existe a pasta _temp_prompts
        if not os.path.exists("_temp_prompts"):
            os.makedirs("_temp_prompts")
            # Cria o arquivo txt com o treinamento
            with open("_temp_prompts/prompt_" + nameFile + ".txt", "w", encoding="utf-8") as file:
                file.write(prompt)
        else:
            # Sobrescreve o arquivo txt com o treinamento
            with open("_temp_prompts/prompt_" + nameFile + ".txt", "w", encoding="utf-8") as file:
                file.write(prompt)

    # IMPORTAR O TREINAMENTO
    def import_train(nameFile):
        global chatContent
        # Verifica se o arquivo existe
        if os.path.exists(nameFile):
            # Abre o arquivo
            with open(nameFile, "r", encoding="utf-8") as file:
                chatContent = file.read()
            print("Treinamento importado com sucesso!")
            print("Arquivo: " + nameFile)
        else:
            print("Erro ao importar o treinamento!")

    # RESETAR O CHAT
    def reset_train():
        global train
        train = ""

    # RECEBER PROMPT E PREPARAR ENVIO
    def get_prompt(input_prompt):
        global nameUser
        return nameUser + ": " + input_prompt + "<|endoftext|>"

    # EXECUTAR O CHAT
    while True:
        prompt = get_prompt(input(nameUser + ": "))
        # Verificar se o prompt é um comando
        if prompt.replace(nameUser + ": ", "").startswith("!"):
            check_command(prompt)
            continue
        response = creat_completion(model, prompt, temperature, max_tokens, train, chatContent)

        # Verifica se no texto contem chaves
        if "{" in response.content and "}" in response.content:
            # Pega o texto entre chaves
            comand = response.content.split("{")[1].split("}")[0]
            # Executa o comando
            execute_command(comand)
        # Adiciona no array de chatContent
        chatContent.append(response)

        save_prompt(chatContent)
        print("\033[32m" + response.content + "\033[0;0m")


# Executa a função main() se o arquivo for executado diretamente
if __name__ == "__main__":
    args = parser.parse_args()
    if args.key:
        key = args.key
        print("Chave de API redefinida")
    if args.user:
        nameUser = args.user
        print("Novo usuário definido: " + nameUser)
    openai.api_key = key  # Chave da API
    # Configura o treinamento
    train = train.replace("{nameUser}", nameUser).replace("{cunstomTrain}",
                                                          cunstomTrain.replace("{nameUser}", nameUser))
    # Imprime a ajuda sobre os argumentos
    parser.print_help()
    print("........Chat Inicializado........")
    main()
