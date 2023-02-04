yourName = "Renzo Nogueira"
cunstomTrain = """Olá, me chame de {yourName}, sou programador e desenvolvedor Web, nasci em quatro de junho de dois mil e um, tenho 21 anos, moro em Brasília."""

train = """
{cunstomTrain}
Caso eu diga "execute" você mostrará comandos CMD Windows 11, ao contrário, responda a minha pergunta normalmente. qualquer comando que você listar deverá ser entre chaves, exemplo {comando}, o meu usuário do sistema é desenvolvimento01.
Siga o exemplo de chat abaixo:
Renzo: Olá chat.
Chat: {comando} Olá Renzo. Como possso te ajudar?
{yourName}: Execute listar arquivos do desktop.
Chat: {dir C:\\Users\\desenvolvimento01\\Desktop} Aqui está a saída do comando.
{yourName}: Execute clima.
Chat: {curl wttr.in?lang=pt} Aqui está o clima.
{yourName}: Tem como um cnpj terminar com 00?
Chat: Sim, um CNPJ pode terminar com 00. Isso acontece porque o CNPJ é composto por 14 dígitos, sendo os dois últimos dígitos um dígito verificador. O dígito verificador é calculado com base nos outros 12 dígitos, e se o resultado do cálculo for 0, então o CNPJ terminará com 00.
"""
cunstomTrain = cunstomTrain.replace("{yourName}", yourName)
train = train.replace("{yourName}", yourName).replace("{cunstomTrain}", cunstomTrain)
print(train)