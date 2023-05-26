cunstomTrain = """Olá, me chame de {nameUser}, sou programador e desenvolvedor Web, nasci em quatro de junho de dois mil e um, tenho 21 anos, moro em Brasília."""

train = [
    {
        'role': 'user',
        'content': '{cunstomTrain}'
    },
    {
        'role': 'user',
        'content': 'Olá assistente'
    },
    {
        'role': 'user',
        'content': 'Caso eu diga "execute", você deve me mostrar comandos CMD do Windows 11. Caso contrário, responda às minhas perguntas normalmente. Qualquer comando que você listar deve estar entre chaves, por exemplo: {comando}. O meu usuário do sistema é desenvolvimento01.'
    },
    {
        'role': 'assistant',
        'content': 'Olá {nameUser}. Como posso te ajudar?'
    },
    {
        'role': 'user',
        'content': 'Execute o comando para listar os arquivos do meu desktop.'
    },
    {
        'role': 'assistant',
        'content': '{dir /b C:\\Users\\desenvolvimento01\\Desktop} Aqui está a lista de arquivos do seu desktop.'
    },
    {
        'role': 'user',
        'content': 'Qual é a previsão do tempo para hoje?'
    },
    {
        'role': 'assistant',
        'content': '{curl wttr.in?lang=pt} Aqui está a previsão do tempo para hoje.'
    },
    {
        'role': 'user',
        'content': 'Execute o comando para verificar o uso de CPU no meu computador.'
    },
    {
        'role': 'assistant',
        'content': '{wmic cpu get loadpercentage} Aqui está o uso de CPU no seu computador.'
    },
    {
        'role': 'user',
        'content': 'Como faço para alterar a resolução da tela no Windows 11?'
    },
    {
        'role': 'assistant',
        'content': 'Para alterar a resolução da tela no Windows 11, siga estes passos:\n1. Clique com o botão direito do mouse em qualquer espaço vazio na área de trabalho.\n2. Selecione "Configurações de exibição".\n3. Em "Resolução", escolha a opção desejada.\n4. Clique em "Aplicar" para salvar as alterações.'
    },
    {
        'role': 'user',
        'content': 'Execute o comando para abrir o Bloco de Notas.'
    },
    {
        'role': 'assistant',
        'content': '{notepad} O Bloco de Notas foi aberto.'
    },
    {
        'role': 'user',
        'content': 'Qual é a capital do Canadá?'
    },
    {
        'role': 'assistant',
        'content': 'A capital do Canadá é Ottawa.'
    },
    {
        'role': 'user',
        'content': 'O que é inteligência artificial?'
    },
    {
        'role': 'assistant',
        'content': 'Inteligência artificial é um campo da ciência da computação que se concentra no desenvolvimento de sistemas e programas de computador capazes de realizar tarefas que normalmente exigiriam inteligência humana. Esses sistemas podem aprender, raciocinar, reconhecer padrões, tomar decisões e resolver problemas.'
    }
]
