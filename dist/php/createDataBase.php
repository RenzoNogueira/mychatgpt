<?php

require_once 'conection.php';

// Verificar a conexão
if (!$conn) {
    die("Falha ao conectar ao banco de dados: " . mysqli_connect_error());
} else {
    // Verificar se o banco de dados mywebchat existe
    if (mysqli_num_rows(mysqli_query($conn, "SHOW DATABASES LIKE 'mywebchat'")) == 0) {
        /* 
        Criar o banco de dados com as tabelas: users, api_keys, chat
        users: id, nome, data_nascimento, data_criacao
        api_keys: key, data_criacao
        chat: id, prompt, response, data_criacao
        */
        $sql = <<<SQL
        CREATE DATABASE mywebchat;
        USE mywebchat;
        CREATE TABLE users (
            id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(30) NOT NULL,
            data_nascimento DATE NOT NULL,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        );
        CREATE TABLE api_keys (
            key_api VARCHAR(255) PRIMARY KEY,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        );
        CREATE TABLE chat (
            id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
            prompt VARCHAR(255) NOT NULL,
            response VARCHAR(255) NOT NULL,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        );
SQL;
        if (mysqli_multi_query($conn, $sql)) {
            // echo "Banco de dados criado com sucesso";
        } else {
            echo "Erro ao criar o banco de dados: " . mysqli_error($conn);
        }
    } else {
        echo json_encode(true); // Banco de dados já existe
    }
}