import reflex as rx
from mathapp.state import UserState

def signup():
    return rx.box(
        rx.vstack(
            rx.heading("Sign Up", size="8"),
            rx.form(
                rx.vstack(
                    rx.input(placeholder="Username", name="username"),
                    rx.input(placeholder="Email", name="email", type="email"),
                    rx.input(placeholder="Password", name="password", type="password"),
                    rx.input(placeholder="Confirm Password", name="confirm_password", type="password"),
                    rx.cond(
                        UserState.signup_error_message != "",
                        rx.text(UserState.signup_error_message, color="red"),
                        None,
                    ),
                    rx.button("Sign Up", type="submit"),
                    spacing="4",
                ),
                on_submit=UserState.handle_signup,
            ),
            spacing="4",
            align="center",
            padding="2em",
        ),
        margin_top="calc(50px + 2em)",
    ) 