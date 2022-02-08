from turtle import pos
import telegram
import config
from func import *

bot = telegram.Bot(token=config.telegram_token)

# ids dos databbases usados
database_tarefas_id = "TAREFAS_DATABASE_ID"
database_grupos_id = "GRUPO_DATABASE_ID" # caso vc use uma tabela separada com grupos de pessoas responsáveis

# nome das colunas do seu ddatabase
nome_coluna_tarefa = "Tarefa"
nome_coluna_prazo = "Data"
nome_coluna_responsaveis = "Responsáveis"

# pega todas as tarefas com prazo de hoje
tarefas = get_tarefas_hoje(database_tarefas_id, nome_coluna_prazo)
print(f'***TAREFAS*** \n{tarefas}\n')


# Exemplo caso não tenha uma tabela com grupos separada mas vc coloca o nome das pessoas direto na tabela de tarefas
for tarefa in tarefas:
    descricao = get_valor_coluna(tarefa, nome_coluna=nome_coluna_tarefa)
    responsaveis = get_responsaveis(tarefa, nome_coluna_responsaveis)
    resp = formata_responsaveis(responsaveis)

    msg = f'*Tarefas de Hoje* 👀 \n\n' \
          f'*Descrição*: {descricao} \n\n' \
          f'{resp} \n' \
          f''

    print(f'***]Mensagem*** \n{msg}\n')
    bot.send_message(text=msg, parse_mode='MarkdownV2', chat_id=config.chat_id)


"""
SE VOCÊ NAO TIVER UMA RELAÇÃO NA TABELA PODE DELETAR ESSA PARTE
Exemplo caso você use uma tabela separada para criar grupos e vc chama essa tabela de 
grupos na sua tabela de tarefas gerando uma relação
"""
for tarefa in tarefas:
    descricao = get_valor_coluna(tarefa, 'Descrição')
    grupo_resp = get_responsaveis(tarefa=tarefa, database_relacao_id=database_grupos_id, nome_coluna_responsaveis='Related to posts + stories (Responsável)')
    resp = formata_responsaveis(grupo_resp, col_nome_grupo='Name')

    msg = f'*Posts de Hoje* 👀 \n\n' \
          f'*Descrição*: {descricao} \n\n' \
          f'{resp} \n' \
          f''

    print(f'***]Mensagem*** \n{msg}\n')
    # bot.send_message(text=msg, parse_mode='MarkdownV2', chat_id=config.chat_id)
