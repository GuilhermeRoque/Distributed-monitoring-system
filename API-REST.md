## API Reset

Gerenciar as informações das requisições.

Endpoint: **`/sensor`**


#### GET /sensor/{id}

Retorna informações do sensor{id} informado
Retorna os dados do sensor em formato `application/json`.

* **Requisitos:**

  Precisa está na mesma rede do `station` ou apontar para o ip do `station`
  
 O atributo `id` é obrigatório para a requisição. 

* **Código de resposta de sucesso:**`200 OK`

Sem corpo de resposta.
  Comentários relacionados à tarefa informada encontrados

* **Corpo da resposta:**
  ```json
  [
      {
          "humidity": 50,
          "temperature": 26.0
      }
  ]
  ```
* **Código de resposta de sucesso:**`404 NOT FOUND`

  1. Nenhum sensor encontrado.
  * **Corpo da resposta:**

    ```json
    {
        "error": "Sensor ID não encontrado"
    }
    ```

#### POST /sensor
Executa o cadastro de uma novo sensor. 
O corpo da requisição contém todos os parâmetros do sensor em formato `application/json`. 
Sem corpo de resposta.

* **Requisitos:**

 Precisa está na mesma rede do `station` ou apontar para o ip do `station`

  Os seguintes atributos são obrigatórios no corpo da requisição:`id`, `max` `min`, `model`, `data_type` e `type_specific`.

* **Corpo da requisição:**

  ```json
  {
      "id": "sensor1",
      "max": "24",
      "min": "20",
      "model": "DHT11",
      "data_type": "temperature"
      "type_specific": "{"pin":4}"
  }
  ```
  
* **Código de resposta de sucesso:**`201 CREATED`

  Sensor criado com sucesso. Sem corpo de resposta.

* **Código de resposta de erro:**`404 NOT FOUND`

Sensor não criado.

* **Corpo da resposta:**
  ```json
  {
      "error": "Sensor não criado"
  }
  ```
* **Código de resposta de erro:**`400 BAD REQUEST`

  Campos obrigatórios não informados.

* **Corpo da resposta:**
  ```json
  {
      "error": "Atributos Obrigatórios"
  }
  ```


#### PUT /sensor

Executa a atualização dos dados de um sensor. 
O corpo da requisição contém todos os atributos do sensor que serão alterados em formato `application/json`.

* **Requisitos:**

 Precisa está na mesma rede do `station` ou apontar para o ip do `station`

  Os seguintes atributos são obrigatórios no corpo da requisição:`id`,  `max`,  `min` e `data_type`.

* **Corpo da requisição:**

  ```json
  {
      "id": 1,
      "max": 24,
      "min": 20,
      "data_type": "temperature"
  }
  ```
  
* **Código de resposta de sucesso:**`200`

  Sensor atualizado com sucesso. Sem corpo de resposta.

* **Código de resposta de erro:**`404 NOT FOUND`

  Sensor não encontrado

* **Corpo da resposta:**
  ```json
  {
      "error": "Sensor não encontrado"
  }
  ```
* **Código de resposta de erro:**`400 BAD REQUEST`

  Campo obrigatório não informado.

* **Corpo da resposta:**
  ```json
  {
      "error": "Campo id obrigatório"
  }
  ```


#### DELETE /sensor/{id}


Executa a exclusão do sensor informado(`id`)
O corpo da requisição contém todos os atributos do sensor que serão alterados em formato `application/json`.

* **Requisitos:**

Precisa está na mesma rede do `station` ou apontar para o ip do `station`

* **Código de resposta de sucesso:**`200 OK`

  Sensor deletado com sucesso. Sem corpo de resposta.
  
* **Corpo da requisição:**

  ```json
  {
      "id": sensor1
  }
  ```
  
  ```
* **Código de resposta de erro:**`404 NOT FOUND`

  Sensor não encontrado

* **Corpo da resposta:**
  ```json
  {
      "error": "Sensor não encontrado"
  }
  ```
* **Código de resposta de erro:**`400 BAD REQUEST`

  Campo obrigatório não informado.

* **Corpo da resposta:**
  ```json
  {
      "error": "Campo id obrigatório"
  }
  ```

