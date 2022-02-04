import datetime
from tokenize import group
from notion_client import Client
import datetime
import config
from config import membros

notion = Client(auth=config.notion_token)


def get_tarefas_hoje(datadabe_id, nome_coluna_prazo):
    """ Relazia uma busca no database do notion (database_tarefas_id) e 
    Retorna um dict todas as linhas do database que tem prazo (nome_coluna_prazo) para hoje
    
    IMPORTANTE: a coluna no NOTION com o prazo da tarefa deve ser do tipo 'date' no database, não pode ser string
    """

    hoje = datetime.datetime.today()
    amanha = hoje + datetime.timedelta(days=1)

    return notion.databases.query(
        **{
            "database_id": datadabe_id,
            "filter": {
                "and": [
                    {
                        "property": nome_coluna_prazo,
                        "date": {
                            "before": f'{amanha.strftime("%Y-%m-%d")}T12:00:00',
                        }
                    },
                    {
                        "property": nome_coluna_prazo,
                        "date": {
                            "after": f'{hoje.strftime("%Y-%m-%d")}T12:00:00',
                        }
                    },
                ]
            },
        }
    ).get('results')


def get_responsaveis(tarefa, nome_coluna_responsaveis, database_relacao_id=''):
    """Retorna os responsaveis por uma tarefa
    Se tiver database_relacao_id retorna uma lista com os valores da relação
    Caso contrario retorna uma string com o nome do responsável

    Se sua tabela no notion de TAREFAS tem uma relação com outra tabela de GRUPOS (os responsáveis pela tarefa) passe os argumentos:
    database_relacao_id -- id do database onde vc colocou os grupos e que se relaciona com a database de tarefas
    nome_coluna_responsaveis -- a coluna que relaciona o database de TAREFAS com o database de GRUPOS
    """
    if database_relacao_id == '':
        return get_valor_coluna(tarefa, nome_coluna_responsaveis)

    resp = notion.databases.query(
        **{
            "database_id": database_relacao_id,
            "filter": {
                "property": nome_coluna_responsaveis,
                "relation": {
                    "contains": tarefa.get('id'),
                },
            },
        }
    ).get('results') 

    if len(resp) > 0:
        return resp[0]
    
    return resp


def get_valor_coluna(linha, nome_coluna):
    """ Retorna o valor de uma coluna como está no notion """

    linha = linha.get('properties').get(nome_coluna)
    tipo_coluna = linha.get('type')

    if tipo_coluna == 'title':
        return linha.get('title')[0].get('plain_text')

    if tipo_coluna == 'rich_text':
        return linha.get('rich_text').get('plain_text')

    if tipo_coluna == 'relation':
        return linha.get('relation')[0].get('id')
    
    if tipo_coluna == 'people':
        pessoas = linha.get('people')
        nomes = list()
        if len(pessoas) > 0:
            for p in pessoas:
                nomes.append(p.get('name'))
            return nomes
        return ['']
        

def formata_responsaveis(grupo_resp, col_nome_grupo=''):
    """
    Retorna uma string com cada coluna do database de grupos e marca com @ do telegram da pessoa responsável
    Exemplo:
        Arte: @stefany
        Texto: @felipe
        Revisão: @gabi
    """

    resp_format = 'Responsáveis: '
    if col_nome_grupo == '':
        for nome in grupo_resp:
            resp_format += f'{membros[nome]} '
        return resp_format

    if len(grupo_resp) == 0:
        return f'*1 Arte*: \n*2 Texto*: \n*3 Revisão e Postagem*:'

    nome_grupo = get_valor_coluna(grupo_resp, col_nome_grupo)

    colunas = sorted(grupo_resp.get('properties').keys())
    resp_format = f'Grupo: {nome_grupo}\n'
    for col in colunas:
        if grupo_resp.get('properties').get(col).get('type') == 'people':
            pessoa = get_valor_coluna(grupo_resp, col)[0]
            membro = membros[pessoa]
            resp_format += f'*{col}*: {membro}\n'
    
    return resp_format
