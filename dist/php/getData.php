<?php

require_once 'conection.php';

function getChat($conn)
{
    $query = "SELECT * FROM chat";
    $result = mysqli_query($conn, $query);
    if (mysqli_num_rows($result) > 0) {
        while ($row = mysqli_fetch_assoc($result)) {
            $data[] = $row;
        }
        return $data;
    } else {
        return false;
    }
}

function mountChatText($nameUser, $nameBot, $data)
{
    $text = '';
    // Se for um objeto válido
    if (is_object($data)) {
        foreach ($data as $key => $value) {
            $text .= $nameUser . ': ' . $value['prompt'] . '<|endoftext|>' . $nameBot . ': ' . $value['response'] . '<|endoftext|>';
        }
        return $text;
    } else {
        return false;
    }
}

function getUsers($conn)
{
    $query = "SELECT * FROM users";
    $result = mysqli_query($conn, $query);
    if (mysqli_num_rows($result) > 0) {
        while ($row = mysqli_fetch_assoc($result)) {
            $data[] = $row;
        }
        return $data;
    } else {
        return false;
    }
}

function getKey($conn)
{
    $query = "SELECT * FROM api_keys";
    $result = mysqli_query($conn, $query);
    if (mysqli_num_rows($result) > 0) {
        while ($row = mysqli_fetch_assoc($result)) {
            $data[] = $row;
        }
        return $data;
    } else {
        return false;
    }
}

if (isset($_GET)) {
    $data = [];

    $data['chat'] = getChat($conn);
    $data['users'] = getUsers($conn);
    $data['key'] = getKey($conn);

    echo json_encode($data);
}
