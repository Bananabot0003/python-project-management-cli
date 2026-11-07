class ProjectSummaryService:
    def __init__(self, ai_client):
        self.ai_client = ai_client

    def build_prompt(self, project):
        tasks = []
        for task in project.tasks:
            status = "Complete" if task.completed else "Open"
            contributors = ", ".join(task.contributors) or "None"
            tasks.append(
                f"- {task.title}: {status}; "
                f"Description: {task.description or 'None'}; "
                f"Contributors: {contributors}"
            )

        return (
            "Summarize this fictional project. Use only provided facts. "
            "Do not invent dates, risks or blockers.\n"
            "Provide: Project Summary, Progress, Risks, Next Steps.\n\n"
            f"Project: {project.title}\n"
            f"Owner: {project.owner}\n"
            f"Description: {project.description}\n"
            "Tasks:\n" + ("\n".join(tasks) or "No tasks yet.")
        )

    def summarize(self, project):
        return self.ai_client.send(self.build_prompt(project))
