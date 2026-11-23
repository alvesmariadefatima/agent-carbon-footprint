# Agent Carbon Footprint

Projeto educacional desenvolvido em Python para explorar o uso de agentes de IA na estimativa de pegada de carbono pessoal e na organização de tarefas.

O repositório reúne dois exemplos independentes:

- um fluxo conversacional de agentes para coletar dados, calcular emissões, explicar resultados e sugerir metas de redução;
- um agente de organização de tarefas conectado ao Trello.

## Visão geral

### Assistente de pegada de carbono

O assistente foi planejado como uma cadeia especializada de agentes:

1. coletar hábitos de transporte, energia, alimentação, consumo e resíduos;
2. converter respostas em fatores de emissão;
3. calcular uma estimativa anual em toneladas de CO2 equivalente;
4. explicar quais fontes têm maior participação;
5. recomendar ações personalizadas;
6. criar metas e acompanhar o progresso.

Os agentes são descritos em arquivos Markdown na pasta `agents/`. A implementação de exemplo em `agentCoder/` fornece um agente raiz com ferramentas de busca na web e execução de código.

### Gerenciador de tarefas no Trello

A pasta `agents/agent04/` contém um exemplo de agente criado com Google ADK que pode:

- adicionar tarefas;
- listar tarefas;
- alterar o status;
- concluir tarefas;
- remover tarefas;
- informar o contexto temporal atual.

As tarefas são organizadas em cards do board chamado `DIO` no Trello.

## Tecnologias utilizadas

| Tecnologia | Uso no projeto |
|---|---|
| Python | Implementação dos agentes e ferramentas |
| Google Agent Development Kit (ADK) | Definição e execução dos agentes |
| Gemini | Modelos usados pelas aplicações (`gemini-2.5-flash` e `gemini-3.5-flash`) |
| Google Search | Busca de informações externas no exemplo em `agentCoder` |
| Built-in Code Executor | Execução de código pelo agente de programação |
| Trello API | Integração com boards, listas e cards |
| py-trello | Cliente Python para a API do Trello |
| python-dotenv | Carregamento das variáveis de ambiente |
| Markdown | Definição dos papéis e instruções dos agentes |
| SQLite | Persistência local de sessões criada pelo Google ADK |

## Arquitetura dos agentes de carbono

| Arquivo | Responsabilidade |
|---|---|
| `00.agent-orquestrador.md` | Coordena o fluxo da conversa e decide a próxima ação |
| `01.agent-carbon-Intake.md` | Coleta dados de transporte, energia, alimentação, consumo e resíduos |
| `02.agent-Carbon-Factorsmd` | Normaliza respostas e aplica fatores de emissão médios |
| `03.agent-Carbon-Calculator.md` | Soma as emissões e gera o baseline anual |
| `04.agent-Carbon-Explainability.md` | Explica os resultados em linguagem simples e com analogias |
| `05.agent-Carbon-Advisor.md` | Prioriza recomendações por impacto e esforço |
| `06.agent-Carbon-Goal.md` | Define metas, acompanha progresso e cria elementos de engajamento |

### Fluxo conceitual

```text
Usuário
  -> Carbon Orchestrator
  -> Carbon Intake
  -> Carbon Factors
  -> Carbon Calculator
  -> Carbon Explainability
  -> Carbon Advisor
  -> Carbon Goal
  -> Recomendações e meta anual
```

### Dados considerados

- distância semanal percorrida;
- meio de transporte e tipo de combustível;
- consumo mensal de energia elétrica;
- equipamentos de alto consumo;
- frequência de consumo de carne e padrão alimentar;
- consumo de produtos e geração de resíduos;
- viagens e hábitos pessoais relevantes.

### Unidade de resultado

Os exemplos usam **toneladas de CO2 equivalente por ano** (`t CO2e/ano`). O CO2 equivalente permite representar diferentes gases de efeito estufa em uma unidade comparável.

> Os fatores e exemplos presentes neste repositório são educativos. Os valores podem variar conforme região, fonte energética, tecnologia utilizada e metodologia aplicada.

## Estrutura do projeto

```text
agent-carbon-footprint/
|-- readme.md
|-- agentCoder/
|   |-- agent.py
|   |-- __init__.py
|   `-- .env.example
|-- agents/
|   |-- 00.agent-orquestrador.md
|   |-- 01.agent-carbon-Intake.md
|   |-- 02.agent-Carbon-Factorsmd
|   |-- 03.agent-Carbon-Calculator.md
|   |-- 04.agent-Carbon-Explainability.md
|   |-- 05.agent-Carbon-Advisor.md
|   |-- 06.agent-Carbon-Goal.md
|   `-- agent04/
|       |-- readme.md
|       |-- requirements.txt
|       `-- agenttaskmanager/
|           |-- agent.py
|           |-- __init__.py
|           `-- .env.example
`-- .dio/
    |-- presentation.pptx
    `-- skill-map.md
```

O ambiente virtual `.lab-dio/` existente em `agents/agent04/` foi utilizado localmente para desenvolver e executar o agente com o Google ADK. Ele não precisa ser versionado.

## Pré-requisitos

- Python 3.10 ou superior recomendado;
- `pip`;
- conta Google com chave de API para os serviços do Gemini;
- conta Trello para utilizar o agente de tarefas;
- API key, API secret e token de acesso do Trello;
- board chamado `DIO` no Trello.

## Configuração

### 1. Clonar o projeto

```powershell
git clone https://github.com/alvesmariadefatima/agent-carbon-footprint.git
cd agent-carbon-footprint
```

### 2. Criar um ambiente virtual

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Instalar as dependências

Para o agente de tarefas:

```powershell
pip install -r agents\agent04\requirements.txt
```

Para o agente de busca e código em `agentCoder/`:

```powershell
pip install google-adk python-dotenv
```

### 4. Configurar as credenciais

Não coloque credenciais diretamente no código ou em arquivos versionados.

No diretório `agentCoder/`, copie `.env.example` para `.env` e informe a chave Google:

```env
GOOGLE_GENAI_USE_VERTEXAI=0
GOOGLE_API_KEY=sua-chave-google
```

No diretório `agents/agent04/agenttaskmanager/`, copie `.env.example` para `.env`:

```env
GOOGLE_GENAI_USE_VERTEXAI=0
GOOGLE_API_KEY=sua-chave-google
TRELLO_API_KEY=sua-api-key-trello
TRELLO_API_SECRET=sua-api-secret-trello
TRELLO_TOKEN=seu-token-trello
```

As variáveis podem ser obtidas:

- Google AI Studio: chave da API Gemini;
- Trello: página de gerenciamento de Power-Up/API e processo de autorização descrito em `agents/agent04/readme.md`.

## Executando os agentes

### Assistente de busca e código

A partir da raiz do projeto:

```powershell
adk web agentCoder
```

A interface do Google ADK permite conversar com o `root_agent`, que pode delegar tarefas para o agente de busca ou o agente de execução de código.

### Gerenciador de tarefas no Trello

A partir da raiz do projeto:

```powershell
adk web agents\agent04\agenttaskmanager
```

Ao iniciar, o agente solicita as tarefas do dia e cria cards no board `DIO`. No Trello, o board deve conter uma lista chamada `A Fazer`, `To Do` ou `Todo`. Para alteração de status, também podem ser utilizadas listas como `Em Andamento` e `Concluído`.

## Funções do agente Trello

| Função | Objetivo |
|---|---|
| `get_temporal_context` | Obtém data e hora locais |
| `adicionar_tarefa` | Cria um card no board |
| `listar_tarefas` | Lista cards ou filtra por status |
| `marcar_tarefa_concluida` | Move a tarefa para concluída ou fecha o card |
| `remover_tarefa` | Remove uma tarefa |
| `mudar_status_tarefa` | Move uma tarefa entre listas |

## Boas práticas

- nunca versione arquivos `.env`;
- revogue credenciais expostas;
- use tokens com apenas as permissões necessárias;
- valide fatores de emissão antes de apresentar resultados em produção;
- informe estimativas conservadoras quando faltar informação;
- não armazene dados pessoais desnecessários;
- explique as premissas usadas em cada cálculo;

## Limitações

- os arquivos dos agentes de carbono são especificações conceituais e ainda não formam uma implementação única e completa;
- os cálculos podem depender de fatores médios e estimativas;
- o agente Trello busca especificamente um board chamado `DIO`;
- os nomes das listas são reconhecidos por aliases comuns em português e inglês;
- o resultado não substitui inventários corporativos ou estudos profissionais de carbono;

## Possíveis evoluções

- integrar os seis agentes de carbono em uma única aplicação;
- adicionar uma base versionada de fatores de emissão;
- permitir seleção de país e fonte elétrica regional;
- persistir resultados e progresso por usuário;
- incluir testes automatizados;
- criar interface web;
- adicionar autenticação e proteção de dados;
- registrar histórico de cálculos e metas;
- publicar uma API REST;

## Segurança e privacidade

Os dados descritos pelos agentes podem revelar hábitos pessoais. Em uma implementação real, recomenda-se:

- solicitar somente dados necessários;
- evitar armazenamento permanente sem consentimento;
- permitir exclusão e correção das informações;
- mascarar ou excluir credenciais em logs;
- usar segredos gerenciados por ambiente;
- validar entradas antes de enviar dados a ferramentas externas.
