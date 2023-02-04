import os
import openai
import webbrowser

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
def creatCompletion(model, prompt, temperature, max_tokens, preTeinamento, respostas):
    response = openai.Completion.create(
        model=model,
        prompt=preTeinamento + respostas + "Você: " + prompt,
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