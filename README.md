# capivara-agiota

Bot para cobrar as pessoas no telegram

### Notion para Telegram
Recebe dados do notion para mandar as mensagens no telegram com as informações da tarefa a ser cobrada e marca as pessoas responsáveis pela tarefa
 
## Exemplo dela funcionando
Toda vez que você rodar o código a capivara-agiota vai pegar as tarefas do dia do seu notion e vai mandar uma mensagem no grupo do telegram cobrando os responsáveis.
- tabela no notion: podemos ver que temos uma tarefa para hoje e a stefany é a responsável

![image](https://user-images.githubusercontent.com/40060993/152910005-8240473f-fe32-4a30-9863-25b73b2a759d.png)

- Depois de rodar o programa a capivara-agiota vai mandar uma mensagem no grupo dessa forma:

![image](https://user-images.githubusercontent.com/40060993/152911453-60a47949-5e73-4e35-a79a-bd5bbda6365f.png)

 
# Como eu uso a capivara-agiota?
## Configure seu bot no telegram
1. Crie um bot no telegram (tutorial [aqui](https://sendpulse.com/knowledge-base/chatbot/create-telegram-chatbot)) 
2. Copie o token de acesso do seu bot
3. Substitua `telegram_token` em [config.py](https://github.com/stefanyramos/capivara-agiota/blob/main/config.py#L2) pelo token que você acabou de copiar:
   
   ```python
    notion_token = "YOUR_NOTION_TOKEN"
    telegram_token = "YOUR_TELEGRAM_TOKEN"
    chat_id = "TELEGRAM_CHAT_ID"
    ```

4. Crie um grupo no telegram e adicione o bot nele, de permissões de adm para o bot
5. Entre no link `https://api.telegram.org/bot<YourBOTToken>/getUpdates` . Não se esqueça de trocar `YourBOTToken` pelo token do seu bot
6. Procure por chat_id. Copie ele
7. Substitua `chat_id` em [config.py](https://github.com/stefanyramos/capivara-agiota/blob/main/config.py#L2) pelo chat_id que você acabou de copiar
    
## Configure seu notion
1. Crie um notion: https://www.notion.so
- não se esqueça de selecionar **o teste gratuito do plano de time**

2. Crie uma página 

![image](https://user-images.githubusercontent.com/40060993/152905582-298b33bf-c410-4de2-88ef-9f0d40a1b924.png)

3. Adicione um database ([tutorial aqui](https://www.notion.so/help/guides/creating-a-database)): 

![image](https://user-images.githubusercontent.com/40060993/152908146-b9a72220-2aa9-4301-9a78-4e90988e6689.png)

4. Adicione as pessoas no seu workspace
- na barra lateral esquerda do notion, clique em **Settings & Members**
- clique em **Membres**
- copie o link de convite e envie para os membros de seu time (ou adicione o email deles direto):

![image](https://user-images.githubusercontent.com/40060993/152907576-f163e818-0449-4f4a-a7d2-e94b1068c3bc.png)

5. Agora, você consegue adicionar as pessoas na coluna de **Responsáveis** no seu database:

![image](https://user-images.githubusercontent.com/40060993/152912957-fca27c3d-52dd-43c4-be03-a8860ce028bc.png)


## Crie um token de acesso no Notion

1. CLique em **Settings & Members**
2. Clique em **Integration**
3. Clique em **Develop your own Integrations**

![image](https://user-images.githubusercontent.com/40060993/152908326-290e6a9e-f9a2-4243-89ca-6e6782218797.png)

4. Clique em **New Integration**
5. Dê um nome para ela e clique em **Submit**
6. Copie o token de acesso 

![image](https://user-images.githubusercontent.com/40060993/152908609-e39e9462-50ec-4a1b-9c23-ff098746650e.png)

7. Volte para o seu database no notion. No canto superior direito clique em **Share**
8. Clique em **Invite**
9. Adicione sua integração que você acabou de criar
10. Agora você pode substituir o `token_notion` no [config.py](https://github.com/stefanyramos/capivara-agiota/blob/main/config.py#L1) pelo token do notion que você copiou


## Conecte o database do seu notion com o bot
1. na página de seu database selecione o id do seu database. Ele fica na url dessa forma:

https://www.notion.so/<long_hash_1>?v=<long_hash_2>

<long_hash_1> é o id do database. Copi ele

2. Em [bot.py](https://github.com/stefanyramos/capivara-agiota/blob/main/bot.py#L8-L15), substitua:
- `database_tarefas_id ` pelo id do database que você acaboou de copiar
- `nome_coluna_tarefa` pelo nome da coluna no seu database com o nome que descreve sua tarefa
- `nome_coluna_prazo ` pelo nome da coluna no seu database com o prazo da tarefa (lembre de colocar o tipo da coluna como o de data mesmo, se for somente texto, o bot quebra)
- `nome_coluna_responsaveis` pelo nome da coluna no seu database com os responsáveis pela tarefa (preferencialmente do tipo pessoa, não testei com outros tipos pra saber se funciona)

```
# ids dos databbases usados
database_tarefas_id = "TAREFAS_DATABASE_ID"
database_grupos_id = "GRUPO_DATABASE_ID" # caso vc use uma tabela separada com grupos de pessoas responsáveis

# nome das colunas do seu ddatabase
nome_coluna_tarefa = "Tarefa"
nome_coluna_prazo = "Data"
nome_coluna_responsaveis = "Responsáveis"
```
- Ignore o `database_grupos_id` por enquanto


## Como a capivara agiota marca as pessoas no telegram?

1. Vá em [config.py](https://github.com/stefanyramos/capivara-agiota/blob/main/config.py#L5-L9) e coloque o nome dos membros no notion e seus respectivos usuários no telegram.

```
membros = {
    "nome da pessoa no notion": "@ do telegram da pessoa ",
    "Fulano da Silva": "@fulano", # exemplo
    "": "" # não retire essa linha, se vc tirar ela, quando uma tarefa não tiver ninguem como responsavel o bot vai quebrar
}
```

## Deploy 

Agora, você precisa rodar seu programa uma vez por dia para que a capivara-agiota envie as mensagens no telegram cobrando as pessoas. Para isso, eu usei uma máquina EC2 na aws no teste grátis e usei um crontab para rodar o programa todo dia às 12h30. Passo a passo disso em breve 




