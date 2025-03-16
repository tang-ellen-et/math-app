import os
import reflex as rx


database_url = os.getenv("DATABASE_URL", "sqlite:///reflex.db")

config = rx.Config(
    app_name="mathapp",
    db_url=database_url,
)