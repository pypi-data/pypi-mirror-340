"""Init command"""

from pathlib import Path
import sqlite3
from typing import Annotated
import typer
from rich import print

from quran_cli import utils


def init(
    database: Annotated[Path, typer.Argument(dir_okay=False, help="Database name")],
    generate_sql: Annotated[
        bool,
        typer.Option(
            "-g",
            "--generate-sql",
            help="Weather to generate SQL statements for this command",
        ),
    ] = False,
) -> None:
    """
    Initialize Quran database.

    Examples:

    ```bash
    # Create initial database
    quran-cli init db.sqlite3
    ```
    """

    name = utils.get_database_name(database)

    try:
        connection = sqlite3.connect(name)

        print(f"Initializing [bold]{name}[/bold]...")

        utils.apply_initial_schema(connection, generate_sql)
        utils.insert_initial_data(connection, generate_sql)

        connection.commit()
        connection.close()

        print("Initialization [bold green]completed[/bold green].")

    except Exception as error:
        print(f"[bold red]Error[/bold red]: {error}")
