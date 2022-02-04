# capivara-agiota

Bot para cobrar as pessoas no telegram

### Notion para Telegram
Recebe dados do notion para mandar as mensagens no telegram com as informações da tarefa a ser cobrada e marca as pessoas responsáveis por ela
 
## Como eu uso o bot?
### Configure seu bot no telegram
1. Crie um bot no telegram (tutorial [aqui](https://sendpulse.com/knowledge-base/chatbot/create-telegram-chatbot)) 
2. Copie o token de acesso do seu bot
3. Substitua `telegram_token` em [config.py](https://github.com/stefanyramos/capivara-agiota/blob/main/config.py#L2) pelo token que você acabou de copiar:
   
   
   ```python
    notion_token = "YOUR_NOTION_TOKEN"
    telegram_token = "YOUR_TELEGRAM_TOKEN"
    chat_id = "TELEGRAM_CHAT_ID"
    ```
4. Crie um grupo no telegram e adicione o bot nele, de permissões de adm para ele
5. Entre no link `https://api.telegram.org/bot<YourBOTToken>/getUpdates` . Não se esqueça de trocar `YourBOTToken` pelo token do seu bot
6. Procure por chat_id. Copie ele
7. Substitua `chat_id` em [config.py](https://github.com/stefanyramos/capivara-agiota/blob/main/config.py#L2) pelo chat_id que você acabou de copiar
    
// TODO
    notion part
