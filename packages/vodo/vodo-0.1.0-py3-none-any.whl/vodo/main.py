import typer
from rich.text import Text
from rich.prompt import Prompt
from typing import Optional
from datetime import datetime, timezone, time

app = typer.Typer()


@app.command()
def tasks(done: bool = typer.Option(False, help="Include completed tasks")):
    """List all tasks with labels and priority"""
    from vodo.api import list_tasks
    from vodo.ui import render_priority, render_due_date
    from rich.console import Console
    from rich.table import Table

    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Title", style="bold")
    table.add_column("Priority", style="white")
    table.add_column("Due Date", style="white")

    for task in list_tasks():
        priority_bar = render_priority(task.priority or 0)
        due_text = render_due_date(task.due_date)
        title_text = Text()
        if task.done:
            title_text.append("✔ ", style="green")
        title_text.append(task.title)
        if not done and task.done:
            continue

        table.add_row(str(task.id), title_text, priority_bar, due_text)

    console.print(table)


@app.command()
def view(id: int):
    """View a task"""
    from vodo.api import get_task
    from vodo.ui import render_priority, render_due_date
    from rich.console import Console
    from rich.table import Table

    task = get_task(id)

    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Title", style="bold")
    table.add_column("Priority", style="white")
    table.add_column("Due Date", style="white")

    priority_bar = render_priority(task.priority or 0)
    due_text = render_due_date(task.due_date)
    title_text = Text()
    if task.done:
        title_text.append("✔ ", style="green")
    title_text.append(task.title)

    table.add_row(str(task.id), title_text, priority_bar, due_text)

    console.print(table)


@app.command()
def add(
    title: str,
    description: Optional[str] = typer.Option(None, help="Task description"),
    priority: int = typer.Option(1, min=1, max=5, help="Task priority (1–5)"),
    due_date: Optional[str] = typer.Option(None, help="Due date in YYYY-MM-DD format"),
):
    """Add a new task"""
    from vodo.api import create_task

    if due_date:
        try:
            if ":" in due_date:
                # full datetime format: YYYY-MM-DD:HH:MM:SS
                date_part, time_part = due_date.split(":", 1)
                full_str = f"{date_part} {time_part.replace(':', ':', 2)}"
                full_datetime = datetime.strptime(full_str, "%Y-%m-%d %H:%M:%S")
            else:
                # fallback to midnight
                full_datetime = datetime.strptime(due_date, "%Y-%m-%d")
                full_datetime = datetime.combine(full_datetime.date(), time(0, 0, 0))

            full_datetime = full_datetime.replace(tzinfo=timezone.utc)
            due_date = full_datetime.isoformat().replace("+00:00", "Z")

        except ValueError:
            typer.echo(
                "❌ Invalid due date. Use YYYY-MM-DD or YYYY-MM-DD:HH:MM:SS", err=True
            )
        raise typer.Exit(code=1)

    task = create_task(
        title=title, description=description, priority=priority, due_date=due_date
    )

    typer.echo(f" Created task: [{task.id}] {task.title}")


@app.command()
def edit(id: int):
    """Edit an existing task"""
    from vodo.api import get_task, update_task

    task = get_task(id)
    if not task:
        typer.echo(f"❌ Task with ID {id} not found.")
        raise typer.Exit(code=1)

    typer.echo(
        f"📝 Editing task [{task.id}]: {task.title}\n Press Enter to accept the current value."
    )

    new_title = Prompt.ask("Title", default=task.title)
    new_description = Prompt.ask("Description", default=task.description or "")
    new_priority_str = Prompt.ask("Priority (1–5)", default=str(task.priority or 1))
    new_due_date_str = Prompt.ask(
        "Due Date (YYYY-MM-DD or YYYY-MM-DD:HH:MM:SS)",
        default=task.due_date.strftime("%Y-%m-%d:%H:%M:%S")
        if task.due_date and task.due_date.year > 1
        else "",
    )

    # Parse fields
    try:
        new_priority = int(new_priority_str)
        if not 1 <= new_priority <= 5:
            raise ValueError
    except ValueError:
        typer.echo("❌ Invalid priority. Must be an integer between 1 and 5.")
        raise typer.Exit(code=1)

    due_date = None
    if new_due_date_str:
        try:
            if ":" in new_due_date_str:
                # full datetime
                date_part, time_part = new_due_date_str.split(":", 1)
                full_str = f"{date_part} {time_part.replace(':', ':', 2)}"
                due_date = datetime.strptime(full_str, "%Y-%m-%d %H:%M:%S")
            elif new_due_date_str == "":
                due_date = task.due_date
            else:
                # date only
                due_date = datetime.strptime(new_due_date_str, "%Y-%m-%d")
                due_date = datetime.combine(due_date.date(), datetime.min.time())

            due_date = due_date.replace(tzinfo=timezone.utc)
            due_date = due_date.isoformat().replace("+00:00", "Z")
        except ValueError:
            typer.echo("❌ Invalid due date format.")
            raise typer.Exit(code=1)

    updated = update_task(
        id=id,
        title=new_title,
        description=new_description,
        priority=new_priority,
        due_date=due_date,
    )

    typer.echo(f"✅ Updated task [{updated.id}]: {updated.title}")


@app.command()
def done(task_id: int):
    """Mark a task as done"""
    from vodo.api import mark_task_done

    mark_task_done(task_id)
    typer.echo(f"Task {task_id} marked as done.")


if __name__ == "__main__":
    app()
