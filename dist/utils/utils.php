<?php

include_once "config/settings.php";

use Orhanerday\OpenAi\OpenAi;

class Utils extends OpenAi
{
    private $prompt;
    private $trainingData;
    public function __construct()
    {
        global $OPENAI_API_KEY;
        global $TREINAMENTO;
        parent::__construct($OPENAI_API_KEY);
        $this->setTrainingData($TREINAMENTO);
    }

    public function setTrainingData($trainingData)
    {
        $this->trainingData = $trainingData;
    }
    public function createCompletion($prompt)
    {
        ini_set('memory_limit','2000M');
        $this->prompt = $this->trainingData . $prompt;
        $response = json_decode($this->completion(["prompt" => $this->prompt, "max_tokens" => 300, "temperature" => 0]));
        $response = $response->choices[0]->text;
        $command = "";
        // Verifica se no response contém "${" e "}"
        if (strpos($response, "{") !== false && strpos($response, "}") !== false) {
            // Se conter executa o comando entre as chaves
            $command = $this->executeCommand(substr($response, strpos($response, "{") + 2, strpos($response, "}") - 2));
        }
        if(strlen($command) > 0){
            return "{".$command."} ".$response;
        } else {
            return $response;
        }
    }

    private function executeCommand($command)
    {
        $response = shell_exec($command);
        if(strlen($response) > 0){
            return $response;
        } else {
            return "Comando não encontrado.";
        }
    }
}