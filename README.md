# Exemplo de utilização do RabbitMQ

Projeto de estudo de filas utilizando RabbitMQ.

Acesso ao RabbitMQ: http://localhost:15672
Username: guest
Password: guest

### Tarefas

- [x] Criar API
- [x] Criar Service A
- [x] Criar Service B
- [x] Criar dockerfile`s
- [x] Criar docker-compose
- [ ] Refatorar
- [ ] Finalizar readme
- [ ] Conclusão

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
