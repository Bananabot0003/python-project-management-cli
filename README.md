# Python Project Management CLI

A Python 3.10+ command-line project tracker for multiple users.

## Features

- Object-oriented users, projects, and tasks
- Multiple projects per user
- Multiple task contributors
- Add, list, edit, and complete tasks
- JSON file persistence with load/save error handling
- Rich terminal tables
- Reusable Ollama AI client and project summary service
- Automated tests using pytest

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Or install using Pipenv:

```bash
pipenv install --dev
pipenv shell
```

## Example commands

```bash
python cli.py add-user --name "Alex" --email "alex@example.com"
python cli.py add-user --name "Jordan"
python cli.py list-users
python cli.py add-project --user "Alex" --title "CLI Tool" --description "Build a project tracker"
python cli.py add-task --project "CLI Tool" --title "Write code"
python cli.py add-contributor --project "CLI Tool" --task "Write code" --user "Jordan"
python cli.py complete-task --project "CLI Tool" --task "Write code"
python cli.py list-projects --user "Alex"
python cli.py show-project --project "CLI Tool"
python cli.py edit-project --project "CLI Tool" --description "Updated description"
python cli.py edit-task --project "CLI Tool" --task "Write code" --description "Updated task"
```

To see help:

```bash
python cli.py --help
```

## AI summary

Install Ollama and download the model:

```bash
ollama pull llama3.2
```

Make sure the Ollama service is running, then use:

```bash
python cli.py summarize-project --project "CLI Tool"
```

Choose another installed model with `--model`.

AI requests use only stored fictional project data. Ollama is
optional for the remaining commands and automated tests.

## Architecture

- `models.py`: user, project, and task classes
- `storage.py`: data lookup, changes, and JSON persistence
- `ai_client.py`: reusable external AI service client
- `summary_service.py`: project-specific prompt generation
- `cli.py`: argparse commands and Rich terminal output
- `tests/`: automated tests

## Testing

```bash
python -m pytest -v
```

## Data

The application automatically reads and writes `data/projects.json`.
This file starts with an empty users list.

## Design notes

Users own projects, projects contain tasks, and tasks can reference
multiple existing users as contributors.

The CLI does not call Ollama directly. AI request behavior is
isolated in the client; project-specific prompts live in the
summary service.

No private company information is required or intended for use.
