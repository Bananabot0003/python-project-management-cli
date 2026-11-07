from dataclasses import dataclass, field, asdict


@dataclass
class Task:
    title: str
    description: str = ""
    completed: bool = False
    contributors: list = field(default_factory=list)

    def complete(self):
        self.completed = True

    def add_contributor(self, name):
        if name not in self.contributors:
            self.contributors.append(name)

    def to_dict(self):
        return asdict(self)


@dataclass
class Project:
    title: str
    owner: str
    description: str = ""
    tasks: list = field(default_factory=list)

    def add_task(self, task):
        if any(t.title.lower() == task.title.lower() for t in self.tasks):
            raise ValueError("Task already exists.")
        self.tasks.append(task)

    def find_task(self, title):
        for task in self.tasks:
            if task.title.lower() == title.lower():
                return task
        raise ValueError(f"Task '{title}' not found.")

    def to_dict(self):
        return {
            "title": self.title,
            "owner": self.owner,
            "description": self.description,
            "tasks": [t.to_dict() for t in self.tasks]
        }


@dataclass
class User:
    name: str
    email: str = ""
    projects: list = field(default_factory=list)

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "projects": [p.to_dict() for p in self.projects]
        }
