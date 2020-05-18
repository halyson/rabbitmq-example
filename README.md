# Exemplo de utilização do RabbitMQ

Projeto de estudo de filas utilizando RabbitMQ.

Acesso ao RabbitMQ: http://localhost:15672

- Username: guest
- Password: guest

### Tarefas

- [x] Criar API
- [x] Criar Service A
- [x] Criar Service B
- [x] Criar dockerfile`s
- [x] Criar docker-compose
- [x] Tornar RabbitMQ resiliente
- [x] Finalizar Readme

## Principais Conceitos

### Exchange

A Exchange é um artefato de roteamento que funciona como um carteiro responsável por entregar as mensagens. Quando uma mensagem é publicada numa exchange, é enviada uma propriedade (setada por quem envia) chamada routing key. Essa key funciona como o endereço do destinatário. A exchange olha a key e sabe para onde entregar.
Existem alguns tipos de exchanges:

- **Direct**: a mensagem é enviada para uma fila com o mesmo nome da routing key. Se a routing key não for informada, ela é enviada para uma fila padrão.

- **Fanout**: a mensagem é distribuída para todas as filas associadas. Esse tipo de exchange ignora a routing key, geralmente usada para replicação de alguma informação entre serviços.

- **Topic**: a mensagem é distribuída de acordo com um padrão enviado pela routing key.

- **Header**: a mensagem é distribuída de acordo com seus cabeçalhos. Dessa forma, é feito um match com qual consumidor deve receber aquela mensagem.

### Queues

Recebem as mensagens da exchange e armazenam até que um consumidor se conecte para retirar as mensagens de lá. O nome sugere, isso é feito seguindo uma lógica FIFO (first-in, first-out). Podem ter os seguintes atributos:

- **Durable**: a fila sobrevive ao restart do message broker. O RabbitMQ possui um banco de dados chamado Mnesia aonde armazena essas informações.
- **Exclusive**: possui somente 1 consumidor e morre quando não há mais consumidores.
- **Autodelete**: morre quando não há mais mensagens.

### Binds (associações)

Para que uma exchange entregue uma mensagem para uma fila, deve haver uma associação, um bind entre elas. Isso pode ser feito de maneira programática por quem envia ou através de uma interface web que o RabbitMQ disponibiliza para gerenciamento do broker.

# Deploy

- docker-compose -f "docker-compose.yml" up -d --build

# Fluxo do projeto

## API

- Recebe um request com uma mensagem via POST http://localhost:5000/message/<msg>
  - Envia a mensagem para a fila "task_queue" do rabbitmq

## Service A

- Conecta a fila "task_queue" esperando as mensagens
- Quano recebe uma mensagem analisa o texto e decide o que será feito:
  - **entregar**: Cria uma nova mensagem para exchange "events" com a key "event.calc", logo após confirma o recebimento a mensagem para o rabbitmq
  - **outro valor**: Ignora a mensagem (rejeita)

## RabbitMQ

- Configurando uma binding na exchange "events" para redirecionar as mensagens com a key "events.calc" para a fila "task_queue_b"

## Service B

- Conecta a fila "task_queue_b" esperando as mensagens
- Reliza um processamento "fake"gerando numeros pares e impares
  - **par**: Acusa o recebimento
  - **impar**: Rejeita devolvendo para a fila, para retentativa
  - **20**: Gera uma exception e rejeita a mensagem

# Referências

- https://blog.ateliedocodigo.com.br/primeiros-passos-com-rabbitmq-e-python-938fb0957019
- https://gago.io/blog/rabbitmq-amqp-3-conceitos/
- https://pika.readthedocs.io/en/stable/index.html
- https://www.cloudamqp.com/blog/2015-09-03-part4-rabbitmq-for-beginners-exchanges-routing-keys-bindings.html
- https://hub.docker.com/r/bitnami/rabbitmq/
- https://dev.to/mviegas/pt-br-introducao-ao-rabbitmq-com-net-core-15oc
