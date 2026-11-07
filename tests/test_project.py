import pytest
from models import Task, Project
from storage import ProjectStore
from summary_service import ProjectSummaryService


@pytest.fixture
def store(tmp_path):
    return ProjectStore(tmp_path / "projects.json")


def test_users(store):
    store.add_user("Alex", "alex@example.com")
    assert store.find_user("Alex").email == "alex@example.com"


def test_duplicate_user(store):
    store.add_user("Alex")
    with pytest.raises(ValueError):
        store.add_user("Alex")


def test_projects(store):
    store.add_user("Alex")
    store.add_project("Alex", "CLI Tool")
    assert store.find_project("CLI Tool").owner == "Alex"


def test_tasks(store):
    store.add_user("Alex")
    store.add_project("Alex", "CLI Tool")
    store.add_task("CLI Tool", "Write code")
    store.complete_task("CLI Tool", "Write code")
    assert store.find_project("CLI Tool").find_task(
        "Write code"
    ).completed


def test_contributors(store):
    store.add_user("Alex")
    store.add_user("Jordan")
    store.add_project("Alex", "CLI Tool")
    store.add_task("CLI Tool", "Write code")
    store.add_contributor("CLI Tool", "Write code", "Jordan")
    assert "Jordan" in store.find_project("CLI Tool").find_task(
        "Write code"
    ).contributors


def test_persistence(store, tmp_path):
    store.add_user("Alex")
    store.add_project("Alex", "CLI Tool")
    restored = ProjectStore(tmp_path / "projects.json")
    assert restored.find_project("CLI Tool").owner == "Alex"


def test_summary():
    class FakeClient:
        def send(self, prompt):
            assert "CLI Tool" in prompt
            return "Project summary"

    project = Project("CLI Tool", "Alex")
    project.add_task(Task("Write code"))
    service = ProjectSummaryService(FakeClient())
    assert service.summarize(project) == "Project summary"
