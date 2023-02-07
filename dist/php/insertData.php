<?php

require_once 'conection.php';

function insertChat($conn, $data)
{
    $query = "INSERT INTO chat (id, user, message, date) VALUES (NULL, '{$data['user']}', '{$data['message']}', '{$data['date']}')";
    $result = mysqli_query($conn, $query);
    if ($result) {
        return true;
    } else {
        return false;
    }
}

function insertKey($conn, $data)
{
    // Se não existir chave, insere, senão, atualiza o único registro
    $query = "SELECT * FROM api_keys";
    $result = mysqli_query($conn, $query);
    if (mysqli_num_rows($result) == 0) {
        $query = "INSERT INTO api_keys (key_value) VALUES ('$data')";
        $result = mysqli_query($conn, $query);
        if ($result) {
            return true;
        } else {
            return false;
        }
    } else {
        $query = "UPDATE api_keys SET key_value = '$data'";
        $result = mysqli_query($conn, $query);
        if ($result) {
            return true;
        } else {
            return false;
        }
    }
}

function insertUser($conn, $data)
{
    // Se não existir chave, insere, senão, atualiza o único registro
    $query = "SELECT * FROM users";
    $result = mysqli_query($conn, $query);
    if (mysqli_num_rows($result) == 0) {
        $query = "INSERT INTO users (nome, data_nascimento) VALUES ('$data[0]', '$data[1]')";
        $result = mysqli_query($conn, $query);
        if ($result) {
            return true;
        } else {
            return false;
        }
    } else {
        $query = "UPDATE users SET nome = '$data[0]', data_nascimento = '$data[1]'";
        $result = mysqli_query($conn, $query);
        if ($result) {
            return true;
        } else {
            return false;
        }
    }
}

if (isset($_POST['key'])) {
    $key = $_POST['key'];
    $data = $_POST['data'];
    $type = $_POST['type'];
    if ($type == 'chat') {
        $result = insertChat($conn, $data);
    } else if ($type == 'key') {
        $result = insertKey($conn, $data);
    } else if ($type == 'user') {
        $result = insertUser($conn, $data);
    }
    if ($result) {
        echo 'success';
    } else {
        echo 'error';
    }
}
