<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Setup</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
    <link href="style.css" rel="stylesheet">
</head>
<body>

<main id="app">
    <div class="container py-5">
        <div class="row">
            <div class="col-md-12">
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>Nome</th>
                            <th>Chave OpenAI</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>{{ nome }}</td>
                            <td>{{ chave }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Últimas conversas -->
        <!-- Tabela com busca -->
        <div class="row">
            <div class="searsch d-flex justify-content-end">
                <div class="d-flex">
                    <input type="text" class="form-control me-2" placeholder="Buscar">
                    <button class="btn btn-primary" type="submit"><i class="fas fa-search"></i></button>
                </div>
            </div>
            <div class="col-md-12">
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>Conversa</th>
                            <th>Resposta</th>
                            <th>Data</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(conversa, index) in conversas">
                            <td>{{conversa.prompt}}</td>
                            <td>{{conversa.response}}</td>
                            <td>{{conversa.date}}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</main>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
    <script src="https://code.jquery.com/jquery-3.6.3.min.js"></script>
    <script src="https://kit.fontawesome.com/274af9ab8f.js" crossorigin="anonymous"></script>
    <script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
    <script>
        const { createApp } = Vue;
        const app = createApp({
            data() {
                return {
                    nome: '',
                    chave: '',
                    conversasUser: [],
                    conversasBot: [],
                    conversas: []
                }
            },
            methods: {
                initData() {
                    const SELF = this;
                    // Dados do usuário
                    $.get("config/settings.json", function(data) {
                        SELF.nome = data.YOUR_NAME;
                        SELF.chave = data.OPENAI_API_KEY;
                    });

                    // Dados de conversas
                    $.get("saves/chat.json", function(data) {
                        data.forEach((conversa, index) => {
                            if (index % 2 == 0) { // Se for par, é do usuário
                                SELF.conversasUser.push(conversa);
                            } else {
                                SELF.conversasBot.push(conversa);
                            }
                        });
                        // Juntar as conversas
                        SELF.conversasUser.forEach((conversa, index) => {
                            SELF.conversas.push(
                                {
                                    prompt: conversa.prompt,
                                    response: SELF.conversasBot[index].prompt,
                                    date: SELF.conversasBot[index].date
                                }
                            );
                        });
                    });
                }
            },
            mounted() {
                const SELF = this;
                SELF.initData();
            },
            components: {
                
            }
        });
        app.mount('#app')
    </script>
</body>
</html>