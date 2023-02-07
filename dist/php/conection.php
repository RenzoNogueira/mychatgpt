<?php

$host = "localhost";
$user = "root";
$password = "";
$database = "mywebchat";
$conn = mysqli_connect($host, $user, $password);

// Usar o banco de dados mywebchat
mysqli_select_db($conn, $database);