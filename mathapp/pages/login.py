import reflex as rx
from mathapp.state import State

def login():
    return rx.box(
        rx.vstack(
            rx.heading("Login", size="8"),
            rx.form(
                rx.vstack(
                    rx.input(placeholder="Username", name="username"),
                    rx.input(placeholder="Password", name="password", type="password"),
                    rx.cond(
                        State.error_message != "",
                        rx.text(State.error_message, color="red"),
                        None,
                    ),
                    rx.button("Login", type="submit"),
                    spacing="4",
                ),
                on_submit=State.handle_login,
            ),
            spacing="4",
            align="center",
            padding="2em",
        ),
        margin_top="calc(50px + 2em)",
    ) 