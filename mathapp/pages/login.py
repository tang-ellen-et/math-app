import reflex as rx
from mathapp.state import UserState

def login():
    return rx.box(
        rx.vstack(
            rx.heading("Login", size="8"),
            rx.form(
                rx.vstack(
                    rx.input(placeholder="Username", name="username"),
                    rx.input(placeholder="Password", name="password", type="password"),
                    rx.cond(
                        UserState.error_message != "",
                        rx.text(UserState.error_message, color="red"),
                        None,
                    ),
                    rx.button("Login", type="submit"),
                    spacing="4",
                ),
                on_submit=UserState.handle_login,
            ),
            spacing="4",
            align="center",
            padding="2em",
        ),
        margin_top="calc(50px + 2em)",
    ) 