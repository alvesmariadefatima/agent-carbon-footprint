from google.adk.agents.llm_agent import Agent # type: ignore
import trello
import dotenv
import os
from datetime import datetime

dotenv.load_dotenv()

# Suas credenciais
API_KEY = os.getenv("TRELLO_API_KEY") or os.getenv("GOOGLE_API_KEY")
API_SECRET = os.getenv("TRELLO_API_SECRET")
TRELLO = os.getenv("TRELLO_TOKEN")


def _get_board():
    client = trello.TrelloClient(
        api_key=API_KEY,
        api_secret=API_SECRET,
        token=TRELLO
    )
    boards = client.list_boards()
    for board in boards:
        if board.name == "DIO":
            return board
    raise ValueError("Não foi encontrado um board chamado 'DIO'.")


def get_temporal_context():
    """Retorna a data e hora atuais para organização das tarefas."""
    return datetime.now().strftime("%d/%m/%Y %H:%M")


def adicionar_tarefa(nome_da_task: str, descricao_da_task: str, due_date: str):
    """Adiciona uma nova tarefa ao quadro DIO."""
    board = _get_board()
    listas = board.list_lists()
    if not listas:
        raise ValueError("O board 'DIO' não possui listas.")

    minha_lista = next(
        (lista for lista in listas if lista.name.lower() in ("a fazer", "to do", "todo")),
        listas[0]
    )
    minha_lista.add_card(name=nome_da_task, desc=descricao_da_task, due=due_date)
    return f"Tarefa '{nome_da_task}' adicionada com sucesso."


def listar_tarefas(status: str = "todos"):
    """Lista as tarefas do quadro DIO, opcionalmente filtradas por status."""
    board = _get_board()
    listas = board.list_lists()
    nome_status = status.lower()

    if nome_status in ("todos", "todas", "all"):
        listas_filtradas = listas
    else:
        alias = {
            "a fazer": ("a fazer", "to do", "todo"),
            "em andamento": ("em andamento", "doing", "in progress"),
            "concluído": ("concluído", "concluido", "done", "completed")
        }
        nomes = alias.get(nome_status, (nome_status,))
        listas_filtradas = [lista for lista in listas if lista.name.lower() in nomes]

    tarefas = []
    for lista in listas_filtradas:
        for card in lista.list_cards():
            tarefas.append({"nome": card.name, "status": lista.name, "descricao": card.desc})
    return tarefas


def _encontrar_card(nome_da_task: str):
    board = _get_board()
    for lista in board.list_lists():
        for card in lista.list_cards():
            if card.name.lower() == nome_da_task.lower():
                return card, lista
    raise ValueError(f"Tarefa '{nome_da_task}' não encontrada.")


def marcar_tarefa_concluida(nome_da_task: str):
    """Marca uma tarefa como concluída."""
    card, _ = _encontrar_card(nome_da_task)
    board = _get_board()
    lista_concluida = next(
        (lista for lista in board.list_lists()
         if lista.name.lower() in ("concluído", "concluido", "done", "completed")),
        None
    )
    if lista_concluida is None:
        card.set_closed(True)
        return f"Tarefa '{nome_da_task}' marcada como concluída."
    card.change_list(lista_concluida.id)
    return f"Tarefa '{nome_da_task}' marcada como concluída."


def remover_tarefa(nome_da_task: str):
    """Remove uma tarefa do quadro."""
    card, _ = _encontrar_card(nome_da_task)
    card.delete()
    return f"Tarefa '{nome_da_task}' removida com sucesso."


def mudar_status_tarefa(nome_da_task: str, novo_status: str):
    """Move uma tarefa para a lista correspondente ao novo status."""
    card, _ = _encontrar_card(nome_da_task)
    board = _get_board()
    alias = {
        "a fazer": ("a fazer", "to do", "todo"),
        "em andamento": ("em andamento", "doing", "in progress"),
        "concluído": ("concluído", "concluido", "done", "completed")
    }
    nomes = alias.get(novo_status.lower(), (novo_status.lower(),))
    lista_destino = next(
        (lista for lista in board.list_lists() if lista.name.lower() in nomes),
        None
    )
    if lista_destino is None:
        raise ValueError(f"Não foi encontrada uma lista para o status '{novo_status}'.")
    card.change_list(lista_destino.id)
    return f"Tarefa '{nome_da_task}' movida para '{lista_destino.name}'."


root_agent = Agent(
    model='gemini-3.5-flash',
    name='root_agent',
    description='Agente de Organização de Tarefas',
    instruction="""
        Você é um agente de organização de tarefas.
        Sua função é realizar uma tarefa e criar um card com o nome e descrição da tarefa.
        Você deve me perguntar as atividades que no dia a dia e criar um card para cada uma delas.
        Você inicia a conversa assim que for ativado, perguntando quais são as tarefas do dia.
        Sempre inicie a conversa perguntando quais são as tarefas do dia informado pela tool_get_temporal_context.
        e depois vá perguntando se tem mais alguma tarefa até que o usuário diga que não tem mais tarefas.
        Suas funções:
            1. Adicionar novas tarefas com nome e descrição
            2. Listar todas as tarefas e filtrar por status
            3. Marcar tarefas como concluídas
            4. Remover tarefas da lista
            5. Mudar o status da tarefa (ex: de 'A Fazer' para 'Em Andamento' e de 'Em Andamento' para 'Concluído')
            6. Gerar contexto temporal (data e hora atual) para organizar as tarefas do dia
    """,
    tools={get_temporal_context, adicionar_tarefa, listar_tarefas, marcar_tarefa_concluida, remover_tarefa, mudar_status_tarefa}
)