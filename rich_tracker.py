import sys
import time
from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeRemainingColumn,
)
from rich.prompt import IntPrompt, Prompt

# Initialize console
console = Console()


def get_user_inputs():
    """Prompts the user interactively for task details with validation."""
    console.clear()

    # Welcome Banner
    console.print(
        Panel(
            "[bold white]Terminal Focus Session Setup[/bold white]\n"
            "[dim]Lock in, minimize distractions, and get to work.[/dim]",
            title="[bold bright_cyan]✦ DEEP WORK TRACKER ✦[/bold bright_cyan]",
            border_style="bright_cyan",
            expand=False,
        )
    )
    console.print()

    # 1. Ask for Task Name
    task_name = Prompt.ask(
        "[bold cyan]?[/bold cyan] What are you working on?",
        default="Deep Work",
        console=console,
    ).strip()

    # 2. Ask for Duration in Minutes (IntPrompt ensures only valid positive integers)
    while True:
        minutes = IntPrompt.ask(
            "[bold cyan]?[/bold cyan] Time target in minutes",
            default=25,
            console=console,
        )
        if minutes > 0:
            break
        console.print(
            "[bold red]![/bold red] Please enter a duration greater than 0 minutes."
        )

    return task_name, minutes


def run_focus_session(task_name: str, minutes: int):
    """Runs the live countdown timer and handles clean exits."""
    duration_secs = minutes * 60
    start_time = time.time()
    end_time = start_time + duration_secs

    console.print()
    # Active Session Card
    header_content = (
        f"[bold white]Task:[/bold white] [bold cyan]{task_name}[/bold cyan]\n"
        f"[bold white]Target:[/bold white] [green]{minutes} minutes[/green] "
        f"[dim]({duration_secs} seconds)[/dim]"
    )
    console.print(
        Panel(
            header_content,
            title="[bold green]● IN PROGRESS[/bold green]",
            subtitle="[dim]Press Ctrl+C to stop early[/dim]",
            border_style="green",
            expand=False,
        )
    )
    console.print()

    try:
        # Progress Bar Configuration
        with Progress(
            SpinnerColumn("dots", style="bright_cyan"),
            TextColumn("[bold white]{task.description}"),
            BarColumn(
                bar_width=34,
                style="grey37",
                complete_style="bright_cyan",
                finished_style="bright_green",
            ),
            TextColumn("[bold yellow]{task.percentage:>3.0f}%"),
            TextColumn("•"),
            TimeRemainingColumn(),
            console=console,
            transient=False,
        ) as progress:

            timer_bar = progress.add_task(
                f"[bold cyan]{task_name}[/bold cyan]",
                total=duration_secs,
            )

            # Timer loop locked to wall-clock time
            while time.time() < end_time:
                elapsed = time.time() - start_time
                progress.update(timer_bar, completed=min(elapsed, duration_secs))
                time.sleep(0.2)

            # Ensure bar locks at 100% on completion
            progress.update(timer_bar, completed=duration_secs)

        # Completion Announcement
        console.print()
        console.print(
            Panel(
                f"[bold green]✔ Session Complete![/bold green]\n"
                f"You crushed [bold white]{minutes} minutes[/bold white] of [bold cyan]{task_name}[/bold cyan].",
                border_style="bright_green",
                expand=False,
            )
        )

    except KeyboardInterrupt:
        # Handle early termination cleanly
        elapsed_secs = max(0, time.time() - start_time)
        elapsed_mins = round(elapsed_secs / 60, 1)

        console.print()
        console.print(
            Panel(
                f"[bold yellow]⏸ Session Stopped Early[/bold yellow]\n"
                f"Completed [bold white]{elapsed_mins} minutes[/bold white] on [bold cyan]{task_name}[/bold cyan].",
                border_style="yellow",
                expand=False,
            )
        )


def main():
    try:
        task_name, minutes = get_user_inputs()
        run_focus_session(task_name, minutes)
    except KeyboardInterrupt:
        console.print("\n[dim]Setup cancelled. Exiting cleanly.[/dim]")
        sys.exit(0)


if __name__ == "__main__":
    main()