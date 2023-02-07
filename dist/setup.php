<!DOCTYPE html>
<html lang="pt-br">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Setup</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
    <link href="style.css" rel="stylesheet">
</head>

<body>

    <main id="app">
        <div class="container py-5">
            <div class="row">
                <div class="col-md-6 form-group">
                    <!-- Chave da API -->
                    <div class="mb-3">
                        <label for="chave" class="form-label">Chave da API</label>
                        <input type="text" class="form-control" id="chave" v-model="chave" placeholder="Chave da API">
                    </div>
                    <!-- Nome do usuário -->
                    <div class="mb-3">
                        <label for="nome" class="form-label">Nome do usuário</label>
                        <input type="text" class="form-control" id="nome" placeholder="Nome do usuário">
                    </div>
                    <!-- Data de nascimento -->
                    <div class="mb-3">
                        <label for="dataNascimento" class="form-label">Data de nascimento</label>
                        <input type="date" class="form-control" id="dataNascimento" placeholder="Data de nascimento">
                    </div>
                </div>
                <!-- Últimos conversas -->
                <div class="col-md-6">
                    <table class="table table-striped table-hover">
                        <thead>
                            <tr>
                                <th scope="col">Usuário</th>
                                <th scope="col">Mensagem</th>
                                <th scope="col">Data</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="conversa in conversas">
                                <td>{{conversa.user}}</td>
                                <td>{{conversa.message}}</td>
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
        const {
            createApp
        } = Vue;
        const app = createApp({
            data() {
                return {
                    users: '',
                    chave: '',
                    conversas: []
                }
            },
            methods: {
                async initData() {
                    const SELF = this;

                    // Faz solicitação para para verificar o banco de dados
                    const ExisteBancoDados = await SELF.verificarBancoDados();
                    // Se banco de dado ok, busca os dados
                    if (ExisteBancoDados) {
                        SELF.buscarDados();
                    }
                },
                verificarBancoDados() {
                    return new Promise((resolve, reject) => {
                        $.get("php/createDataBase.php", function(data) {
                            if (data == 'true') {
                                resolve(true);
                            } else {
                                resolve(false);
                            }
                        });
                    });
                },
                buscarDados() {
                    const SELF = this;
                    $.get("php/getData.php", function(data) {
                        SELF.conversas = data.chat;
                        SELF.chave = data.key;
                        SELF.users = data.users;
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