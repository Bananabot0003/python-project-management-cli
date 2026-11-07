import json
import os
from pathlib import Path
from models import User, Project, Task


class ProjectStore:
    def __init__(self, filename="data/projects.json"):
        self.filename = Path(filename)
        self.users = []
        self.load()

    def load(self):
        if not self.filename.exists():
            return
        try:
            with self.filename.open(encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, dict) or not isinstance(
                data.get("users"), list
            ):
                raise ValueError("Invalid data structure.")

            users = []
            for u in data["users"]:
                user = User(u["name"], u.get("email", ""))
                for p in u.get("projects", []):
                    project = Project(
                        p["title"], p["owner"],
                        p.get("description", "")
                    )
                    for t in p.get("tasks", []):
                        project.tasks.append(Task(
                            t["title"],
                            t.get("description", ""),
                            t.get("completed", False),
                            list(t.get("contributors", []))
                        ))
                    user.projects.append(project)
                users.append(user)
            self.users = users

        except (OSError, ValueError, TypeError, KeyError) as e:
            raise RuntimeError(f"Could not load data: {e}") from e

    def save(self):
        self.filename.parent.mkdir(parents=True, exist_ok=True)
        temp = self.filename.with_suffix(".tmp")
        try:
            with temp.open("w", encoding="utf-8") as f:
                json.dump(
                    {"users": [u.to_dict() for u in self.users]},
                    f, indent=2
                )
            os.replace(temp, self.filename)
        except OSError as e:
            raise RuntimeError(f"Could not save data: {e}") from e

    def find_user(self, name):
        for user in self.users:
            if user.name.lower() == name.lower():
                return user
        raise ValueError(f"User '{name}' not found.")

    def find_project(self, title):
        for user in self.users:
            for project in user.projects:
                if project.title.lower() == title.lower():
                    return project
        raise ValueError(f"Project '{title}' not found.")

    def add_user(self, name, email=""):
        name = name.strip()
        if not name:
            raise ValueError("Name cannot be empty.")
        if any(u.name.lower() == name.lower() for u in self.users):
            raise ValueError("User already exists.")
        user = User(name, email.strip())
        self.users.append(user)
        self.save()
        return user

    def add_project(self, username, title, description=""):
        user = self.find_user(username)
        title = title.strip()
        if not title:
            raise ValueError("Project title cannot be empty.")
        if any(
            p.title.lower() == title.lower()
            for u in self.users for p in u.projects
        ):
            raise ValueError("Project already exists.")
        project = Project(title, user.name, description.strip())
        user.projects.append(project)
        self.save()
        return project

    def add_task(self, project_title, title, description=""):
        project = self.find_project(project_title)
        title = title.strip()
        if not title:
            raise ValueError("Task title cannot be empty.")
        task = Task(title, description.strip())
        project.add_task(task)
        self.save()
        return task

    def complete_task(self, project_title, task_title):
        task = self.find_project(project_title).find_task(task_title)
        task.complete()
        self.save()
        return task

    def add_contributor(self, project_title, task_title, username):
        user = self.find_user(username)
        task = self.find_project(project_title).find_task(task_title)
        task.add_contributor(user.name)
        self.save()
        return task

    def edit_project(self, title, description):
        project = self.find_project(title)
        project.description = description.strip()
        self.save()

    def edit_task(self, project_title, task_title, description):
        task = self.find_project(project_title).find_task(task_title)
        task.description = description.strip()
        self.save()
