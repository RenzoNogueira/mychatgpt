<?php

require __DIR__ . '/vendor/autoload.php'; // remove this line if you use a PHP Framework.

use Orhanerday\OpenAi\OpenAi;

$open_ai_key = 'key';
$open_ai = new OpenAi($open_ai_key);

$prompt = $_POST['prompt'];
// verifica se há uma sessão iniciada
if (isset($_COOKIE['CHATMESSAGES'])) {
    $chatMessages = json_decode($_COOKIE['CHATMESSAGES'], true);
} else {
    $chatMessages =  [
        [
            "role" => "system",
            "content" => "Você é um assistente útil."
        ]
    ];
}

array_push($chatMessages, [
    "role" => "user",
    "content" => $prompt
]);

$complete = $open_ai->chat([
    'model' => 'gpt-3.5-turbo',
    'messages' => $chatMessages,
    'temperature' => 1.0,
    'max_tokens' => 4000,
    'frequency_penalty' => 0,
    'presence_penalty' => 0,
]);

$response = json_decode($complete);
array_push($chatMessages, [
    "role" => "system",
    "content" => $response->choices[0]->message->content
]);

// Sava nos cookies durante 1 dia
setcookie('CHATMESSAGES', json_encode($chatMessages), time() + (86400 * 1), "/");
echo $chatMessages[count($chatMessages) - 1]['content'];
