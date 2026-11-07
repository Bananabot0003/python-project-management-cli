import argparse
from pathlib import Path
from rich.console import Console
from rich.table import Table
from storage import ProjectStore
from ai_client import OllamaChatClient
from summary_service import ProjectSummaryService

console = Console()


def build_parser():
    parser = argparse.ArgumentParser(
        description="Multi-user Project Management CLI"
    )
    commands = parser.add_subparsers(dest="command", required=True)

    def command(name, *arguments):
        sub = commands.add_parser(name)
        for flag in arguments:
            sub.add_argument("--" + flag, required=True)
        return sub

    user = command("add-user", "name")
    user.add_argument("--email", default="")
    commands.add_parser("list-users")

    project = command("add-project", "user", "title")
    project.add_argument("--description", default="")

    listing = commands.add_parser("list-projects")
    listing.add_argument("--user")

    command("show-project", "project")

    task = command("add-task", "project", "title")
    task.add_argument("--description", default="")

    command("list-tasks", "project")
    command("complete-task", "project", "task")
    command("add-contributor", "project", "task", "user")
    command("edit-project", "project", "description")
    command("edit-task", "project", "task", "description")

    summary = command("summarize-project", "project")
    summary.add_argument("--model", default="llama3.2")

    return parser


def print_projects(projects):
    table = Table(title="Projects")
    for column in ("Title", "Owner", "Description", "Tasks"):
        table.add_column(column)
    for p in projects:
        table.add_row(
            p.title, p.owner, p.description, str(len(p.tasks))
        )
    console.print(table)


def print_tasks(project):
    table = Table(title=f"Tasks for {project.title}")
    for column in ("Task", "Status", "Description", "Contributors"):
        table.add_column(column)
    for t in project.tasks:
        table.add_row(
            t.title,
            "Completed" if t.completed else "Open",
            t.description or "-",
            ", ".join(t.contributors) or "-"
        )
    console.print(table)


def run_command(args, store):
    cmd = args.command

    if cmd == "add-user":
        store.add_user(args.name, args.email)
        console.print(f"[green]User '{args.name}' created.[/green]")

    elif cmd == "list-users":
        table = Table(title="Users")
        for column in ("Name", "Email", "Projects"):
            table.add_column(column)
        for u in store.users:
            table.add_row(u.name, u.email, str(len(u.projects)))
        console.print(table)

    elif cmd == "add-project":
        store.add_project(args.user, args.title, args.description)
        console.print(f"[green]Project '{args.title}' created.[/green]")

    elif cmd == "list-projects":
        projects = (
            store.find_user(args.user).projects
            if args.user else
            [p for u in store.users for p in u.projects]
        )
        print_projects(projects)

    elif cmd == "show-project":
        project = store.find_project(args.project)
        print_projects([project])
        print_tasks(project)

    elif cmd == "add-task":
        store.add_task(args.project, args.title, args.description)
        console.print(f"[green]Task '{args.title}' added.[/green]")

    elif cmd == "list-tasks":
        print_tasks(store.find_project(args.project))

    elif cmd == "complete-task":
        store.complete_task(args.project, args.task)
        console.print(f"[green]Task '{args.task}' completed.[/green]")

    elif cmd == "add-contributor":
        store.add_contributor(
            args.project, args.task, args.user
        )
        console.print("[green]Contributor assigned.[/green]")

    elif cmd == "edit-project":
        store.edit_project(args.project, args.description)
        console.print("[green]Project updated.[/green]")

    elif cmd == "edit-task":
        store.edit_task(
            args.project, args.task, args.description
        )
        console.print("[green]Task updated.[/green]")

    elif cmd == "summarize-project":
        project = store.find_project(args.project)
        service = ProjectSummaryService(
            OllamaChatClient(args.model)
        )
        console.print(service.summarize(project))


def main():
    args = build_parser().parse_args()
    filename = Path(__file__).resolve().parent / "data/projects.json"
    try:
        run_command(args, ProjectStore(filename))
        return 0
    except (ValueError, RuntimeError, OSError) as e:
        console.print(f"[red]Error: {e}[/red]")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
