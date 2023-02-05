<?php
// Pega os dados json do arquivo settings.json

define('ROOT', dirname(__DIR__));

$settings = file_get_contents(ROOT.'/config/settings.json');
$settings = json_decode($settings, true);

$OPENAI_API_KEY = $settings['OPENAI_API_KEY'];
$YOUR_NAME = $settings['YOUR_NAME'];

$TREINAMENTO = $settings['CUNSTOM_TRAINING'];