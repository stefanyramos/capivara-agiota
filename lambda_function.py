import telegram
from notion_client import Client
import datetime
import config
from config import membros

bot = telegram.Bot(token=config.telegram_token)
notion = Client(auth=config.notion_token)

hoje = datetime.datetime.today()
amanha = hoje + datetime.timedelta(days=1)

db = notion.databases.query(
    **{
        "database_id": "19970d82fb4b40de8380949481656708",
        "filter": {
            "and": [
                {
                    "property": "Data da Postagem",
                    "date": {
                        "before": f'{amanha.strftime("%Y-%m-%d")}T12:00:00',
                    }
                },
                {
                    "property": "Data da Postagem",
                    "date": {
                        "after": f'{hoje.strftime("%Y-%m-%d")}T12:00:00',
                    }
                },
            ]
        },
    }
)

posts_hoje = db.get('results')
for post in posts_hoje:
    descricao = post.get('properties').get('Descrição').get('title')[0].get('text').get('content')

    responsaveis = notion.databases.query(
        **{
            "database_id": "09d84fdfe9744f4cbd25d00ea9cc4145",
            "filter": {
                "property": "Related to posts + stories (Responsável)",
                "relation": {
                    "contains": post.get('id'),
                },
            },
        }
    ).get('results')

    grupo = "ninguem >:("
    arte, texto, revisao = '', '', ''

    if len(responsaveis) > 0:
        grupo = responsaveis[0].get('properties').get('Name').get('title')[0].get('text').get('content')

        arte = responsaveis[0].get('properties').get('1 Arte').get('people')
        if len(arte) > 0:
            arte = arte[0].get('name')
            arte = membros[arte]

        texto = responsaveis[0].get('properties').get('2 Texto').get('people')
        if len(texto) > 0:
            texto = texto[0].get('name')
            texto = membros[texto]

        revisao = responsaveis[0].get('properties').get('3 Revisão e Postagem').get('people')
        if len(revisao) > 0:
            revisao = revisao[0].get('name')
            revisao = membros[revisao]

    msg = f'Posts de Hoje 👀 \n\n' \
          f'Descrição: {descricao} \n\n' \
          f'Responsável: {grupo} \n' \
          f'Arte: {arte}\n' \
          f'Texto: {texto}\n' \
          f'Revisão: {revisao}' 

    bot.send_message(text=msg, chat_id=-1001451877609)


