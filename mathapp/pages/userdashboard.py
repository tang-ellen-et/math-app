import reflex as rx
from mathapp.data_graph import UserMetricStats
from mathapp.state import State
from mathapp.user_state import UserState

def userdashboard():
    return rx.box(
        rx.section(
            rx.center(rx.heading("User Exercise Dashboard", size="9", bold=True, color_scheme="blue")),
            rx.center(
                rx.text(
                    f"Welcome, {UserState.current_user}",
                    size="5",
                    color="green",
                    font_weight="bold",
                    margin_top="1em",
                )
            ),
            rx.center(
                rx.hstack(
                    rx.link("Home", href="/", size="8", bold=True, color_scheme="blue"),
                    rx.link("Back to Quiz", href="/quiz", size="8", bold=True, color_scheme="blue"),
                    spacing="5",
                )
            ),
            padding="2"
        ),
        rx.section(
            rx.flex(
                rx.box(
                    UserMetricStats.graph_table(State.items_by_result),
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
                    UserMetricStats.graph_pie(State.items_by_result),
                    width="50%",
                    padding="1em"
                ),
                rx.box(
                    UserMetricStats.graph(State.items_by_type),
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