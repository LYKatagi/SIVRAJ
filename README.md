# SIVRAJ

> **SIVRAJ** — um assistente de voz local, modular e extensível, desenvolvido em Python.

SIVRAJ é um projeto experimental de assistente pessoal que utiliza **Ollama** para interpretar comandos em linguagem natural e executa ações através de um sistema próprio de comandos.

O projeto começa como uma aplicação de terminal. A interface gráfica com **CustomTkinter** será adicionada posteriormente.

## ✨ Features

* 🤖 Integração com modelos locais através do Ollama
* 🎤 Sistema de reconhecimento de voz
* 🔊 Resposta por voz
* ⚙️ Sistema modular de comandos
* 🧠 Interpretação de linguagem natural
* 🗺️ Sistema de mapas e localização
* 🔌 Sistema de plugins planejado
* 🖥️ Interface gráfica planejada com CustomTkinter
* 🧪 Arquitetura preparada para testes

## 🧠 Arquitetura

O SIVRAJ utiliza uma arquitetura baseada em separação de responsabilidades:

```text
Usuário
   │
   ▼
Voice / Terminal
   │
   ▼
Ollama
   │
   ▼
JSON Command
   │
   ▼
Validator
   │
   ▼
Command Router
   │
   ▼
Command Executor
   │
   ├── Apps
   ├── System
   ├── Maps
   └── Plugins
   │
   ▼
Response
```

O modelo de IA **não executa ações diretamente**. Ele apenas interpreta o pedido e retorna uma estrutura de comando. O SIVRAJ valida essa estrutura antes de executar qualquer ação.

### Exemplo

Entrada:

```text
Mostre minha localização
```

Resposta esperada da IA:

```json
{
  "cmd": "maps",
  "response": "Aqui está sua localização.",
  "show": "location"
}
```

## 📁 Estrutura

```text
SIVRAJ/
├── src/
│   ├── ai/
│   ├── commands/
│   ├── core/
│   ├── voice/
│   └── ui/
│
├── plugins/
├── tests/
│
├── main.py
├── AGENTS.md
├── README.md
├── .gitignore
├── .gitattributes
└── requirements.txt
```

> A estrutura pode mudar conforme o projeto evoluir.

## 🚀 Desenvolvimento

Clone o repositório:

```bash
git clone <repository-url>
cd SIVRAJ
```

Crie um ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente virtual no Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Certifique-se de que o Ollama esteja instalado e que um modelo compatível esteja disponível localmente.

Execute:

```bash
python main.py
```

## 🛠️ Tecnologias

* **Python**
* **Ollama**
* **CustomTkinter** — interface gráfica planejada
* **Git** — controle de versão

## 🗺️ Roadmap

### v0.1 — Core

* [X] Estrutura inicial
* [] CLI
* [X] Integração com Ollama
* [X] Parser de comandos
* [X] Validação de JSON
* [X] Command Router

### v0.2 — Voice

* [X] Speech-to-Text
* [ ] Text-to-Speech
* [X] Pipeline de voz

### v0.3 — Commands

* [ ] Abrir aplicativos
* [ ] Sistema
* [ ] Arquivos
* [ ] Comandos personalizados

### v0.4 — SIVRAJ Maps

* [ ] Map renderer
* [ ] Localização
* [ ] Marcadores
* [ ] Zoom e navegação

### v0.5 — Plugins

* [ ] Plugin API
* [ ] Plugin registry
* [ ] Carregamento dinâmico

### v1.0 — Interface

* [ ] CustomTkinter
* [ ] Dashboard
* [ ] Animações
* [ ] Logs
* [ ] Configurações

## 🔐 Segurança

O SIVRAJ não deve executar comandos arbitrários gerados pelo modelo de IA.

Toda resposta do modelo deve ser:

1. Interpretada.
2. Validada.
3. Comparada com os comandos permitidos.
4. Executada pelo código do SIVRAJ.

## 📜 Licença

Este projeto ainda não possui uma licença definida.
