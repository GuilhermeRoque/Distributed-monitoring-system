## API Reset

Gerenciar as informações das requisições.

Endpoint: **`/sensor`**


#### GET

Retorna informações do sensor{id} informado.
Retorna os dados do sensor em formato `application/json`.

* **Requisitos:**

  Precisa está na mesma rede do `station`.
  
 O atributo `id` é obrigatório para a requisição. 

* **Código de resposta de sucesso:**`200 OK`

Sem corpo de resposta.

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

Sem corpo de resposta.

#### POST
Executa o cadastro de uma novo sensor. 
O corpo da requisição contém todos os parâmetros do sensor em formato `application/json`. 

* **Requisitos:**

   Precisa está na mesma rede do `station`.

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
  
* **Código de resposta de sucesso:**`201`

Sem corpo de resposta.

* **Código de resposta de erro:**`404 NOT FOUND`

Sem corpo de resposta.

* **Código de resposta de erro:**`400 BAD REQUEST`

Sem corpo de resposta.

#### PUT

Executa a atualização dos dados de um sensor. 
O corpo da requisição contém todos os atributos do sensor que serão alterados em formato `application/json`.

* **Requisitos:**

   Precisa está na mesma rede do `station`.

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

Sem corpo de resposta.

* **Código de resposta de erro:**`404 NOT FOUND`

Sem corpo de resposta.

* **Código de resposta de erro:**`400 BAD REQUEST`

Sem corpo de resposta.

#### DELETE 

Executa a exclusão do sensor informado.
O corpo da requisição contém todos os atributos do sensor que serão alterados em formato `application/json`.

* **Requisitos:**

  Precisa está na mesma rede do `station`.

* **Código de resposta de sucesso:**`200 OK`

Sem corpo de resposta.

* **Código de resposta de erro:**`404 NOT FOUND`

Sem corpo de resposta.

* **Código de resposta de erro:**`400 BAD REQUEST`

Sem corpo de resposta.
