import reflex as rx
from mathapp.data_graph import UserStats
from mathapp.state import State

def userdashboard():
    return rx.box(
        rx.section(
            rx.center(rx.heading("User Exercise Dashboard", size="9", bold=True, color_scheme="blue")),
            rx.center(rx.link("Home", href="/", size="8", bold=True, color_scheme="blue")),
            background="right/cover url('/math_app_logo.png')",
            padding="2em"
        ),
        rx.section(
            rx.flex(
                rx.box(
                    UserStats.graph_table(State.items_by_result),
                    width="100%",
                    padding="1em"
                ),
                width="100%",
                justify="center"
            )
        ),
        rx.section(
            rx.flex(
                rx.box(
                    UserStats.graph_pie(State.items_by_result),
                    width="50%",
                    padding="1em"
                ),
                rx.box(
                    UserStats.graph(State.items_by_type),
                    width="50%", 
                    padding="1em"
                ),
                width="100%",
                justify="center",
                align="center"
            )
        ),
        width="80%",
        margin="0 auto"
    )