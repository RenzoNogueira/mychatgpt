<?php

include_once "config/settings.php";
require_once "php/insertData.php";
require_once "php/getData.php";

use Orhanerday\OpenAi\OpenAi;

// Data time brasileiro
date_default_timezone_set('America/Sao_Paulo');

class Utils extends OpenAi
{
    private $prompt;
    private $trainingData;
    private $yourName;
    private $chatData;
    public function __construct()
    {
        global $OPENAI_API_KEY;
        global $TREINAMENTO;
        global $YOUR_NAME;
        $this->setYourName($YOUR_NAME);
        $this->setTrainingData($TREINAMENTO);
        $this->chatData = $this->getChatData();
        parent::__construct($OPENAI_API_KEY);
    }

    // Pega os dados json do arquivo chat.json
    public function getChatData()
    {
        $this->chatData = file_get_contents(ROOT . '/saves/chat.json');
        $this->chatData = json_decode($this->chatData, true);
        return $this->chatData;
    }

    // Pega os textos do chatData e concatena em uma string
    public function getChatDataString()
    {
        $chatData = $this->getChatData();
        $chatDataString = "";
        foreach ($chatData as $key => $value) {
            $chatDataString .= $value['prompt'];
        }
        return $chatDataString;
    }

    // Adiciona os dados no arquivo chat.json
    public function addChatData($data)
    {
        // Concatena os dados do chat
        $this->chatData[] = $data;
        $chatData = json_encode($this->chatData);
        file_put_contents(ROOT . '/saves/chat.json', $chatData);
    }

    public function setTrainingData($trainingData)
    {
        $this->trainingData = $trainingData;
    }

    public function setYourName($yourName)
    {
        $this->yourName = $yourName;
    }

    public function createCompletion($prompt)
    {
        // $prompt = "- " . $prompt;
        // $this->addChatData(["prompt" => $prompt, "type" => "user", "date" => date("d/m/Y H:i:s")]);
        // // Junta os dados de treinamento com o histórico de conversa
        // $this->prompt = $this->trainingData . $this->getChatDataString();
        // $response = json_decode($this->completion(["prompt" => $this->prompt, "max_tokens" => 50, "temperature" => 0]));
        // $response = $response->choices[0]->text;
        // $this->addChatData(["prompt" => $response, "type" => "bot", "date" => date("d/m/Y H:i:s")]);
        // return $response;
        global $conn;
        $history = getChat($conn);
        $history = mountChatText($this->yourName, "Bot", $history);
        echo $history;
    }
}
