import telegram
import config
from config import membros
from func import *

bot = telegram.Bot(token=config.telegram_token)

database_posts_id = "19970d82fb4b40de8380949481656708"
database_grupos_id = "09d84fdfe9744f4cbd25d00ea9cc4145"
nome_coluna_prazo = "Data da Postagem"

posts = get_tarefas_hoje(database_posts_id, nome_coluna_prazo)

for tarefa in posts:
    descricao = get_valor_coluna(tarefa, 'Descrição')
    grupo_resp = get_responsaveis(tarefa=tarefa, database_relacao_id=database_grupos_id, nome_coluna_responsaveis='Related to posts + stories (Responsável)')
    resp = formata_responsaveis(grupo_resp, col_nome_grupo='Name')

    msg = f'*Posts de Hoje* 👀 \n\n' \
          f'*Descrição*: {descricao} \n\n' \
          f'{resp} \n' \
          f''

    bot.send_message(text=msg, parse_mode='MarkdownV2', chat_id=config.chat_id)


""" Exemplo caso não tenha uma tabela com grupos separada mas vc coloca o nome das pessoas direto na tabela de tarefas
for tarefa in posts:
    descricao = get_valor_coluna(tarefa, 'Descrição')
    grupo_resp = get_responsaveis(tarefa=tarefa, nome_coluna_responsaveis='Pessoa responsavel')
    resp = formata_responsaveis(grupo_resp)

    msg = f'*Posts de Hoje* 👀 \n\n' \
          f'*Descrição*: {descricao} \n\n' \
          f'{resp} \n' \
          f''

    bot.send_message(text=msg, parse_mode='MarkdownV2', chat_id=config.chat_id)
"""
