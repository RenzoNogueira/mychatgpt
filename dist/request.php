<?php

// executa um comando no sistema operacional para uma janela cmd
// echo shell_exec('start cmd');

include_once 'vendor/autoload.php';
include "utils/utils.php";

header('Content-Type: application/json');



$prompt = $_POST['prompt'];

$utils = new Utils();
echo json_encode($utils->createCompletion($prompt));