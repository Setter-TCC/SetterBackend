<p align="center">
  <img width="200" height="200" src="./public/logo.svg">
  <br />
</p>

# Setter

O Setter é uma aplicação *open-source* que auxilia administradores de times amadores de voleibol a gerirem seus times.

As principais funcionalidades são:
- Controle dos Dados do Time
- Controle dos Dados do Técnico
- Controle dos Dados dos Atletas
- Gerenciamento de Atletas
- Controle do Fluxo de Caixa
- Mensalidade
- Pagamento de Técnico
- Manutenção da conta

As próximas funcionalidades serão:
- Controle de Presença em Eventos
- Controle de Uniformes
- Calendário de Jogos
- Lembretes e Avisos
- Gerenciamento de Administradores
- Registro de Jogos

A aplicação está disponível em: [https://setter-front-d443799d9d71.herokuapp.com/](https://setter-front-d443799d9d71.herokuapp.com/)

## Quer contribuir?
O Setter possui dois repositórios de desenvolvimento, e um de documentação. Todos eles podem ser encontrados na [organização](https://github.com/Setter-TCC). É bem simples saber como contribuir para o projeto, basta acessar o nosso [Guia de Contribuição](./CONTRIBUTING.md). 

## Comandos de Execução (Setter Backend)

Antes de propriamente executar o projeto, se faz necessária a instalação da ferramenta docker em conjunto com o docker-compose como pré-requisitos. Para tal, você pode seguir [este guia para instalação do docker](https://docs.docker.com/engine/install/) e [este guia para instalação do docker-compose](https://docs.docker.com/compose/install/).
Uma vez instaladas as dependências, você pode seguir os próximos passos para a execução.

1. Na raiz do projeto, na primeira execução, rode o comando:
```
$ docker-compose up --build
```

2. Para rodar localmente, execute o comando:
```
$ docker-compose up
```

A aplicação estará rodando na porta ```localhost:8000```.

3. Para acessar a documentação das rotas criadas, acesse a página: 
```
http://localhost:8000/api/docs
```
