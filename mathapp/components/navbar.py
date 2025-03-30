import reflex as rx
from mathapp.state import State
from mathapp.user_state import UserState

def navbar():
    return rx.box(
        rx.hstack(
            # Left section with logo and title
            rx.hstack(
                rx.heading(
                    rx.link("Math App - Problems", href="/allproblems"),
                    size="8",
                    font_family="sans serif",
                    color='black',
                ),
                spacing="4",
            ),
            rx.spacer(),
            # Middle section with action buttons
            rx.hstack(
                rx.button(
                    "Generate Exercise",
                    on_click=State.generate_new_problemset,
                    size="3",
                ),
                rx.button(
                    "Reset Problems DB",
                    on_click=State.reset_problems_db,
                    color_scheme="red",
                    size="3",
                ),
                spacing="4",
            ),
            rx.spacer(),
            # Right section with theme toggle and auth
            rx.hstack(
                rx.color_mode.button(),
                rx.cond(
                    UserState.is_authenticated,
                    rx.hstack(
                        rx.text(
                            f"Welcome, {UserState.current_user}",
                            color="green",
                            font_weight="bold",
                            size="3",
                        ),
                        rx.button(
                            "Logout",
                            on_click=UserState.handle_logout,
                            color_scheme="red",
                            size="3",
                        ),
                        spacing="4",
                    ),
                    rx.hstack(
                        rx.link(
                            "Login",
                            href="/login",
                            padding="0.5em 1em",
                            size="3",
                        ),
                        rx.link(
                            "Sign Up",
                            href="/signup",
                            padding="0.5em 1em",
                            size="3",
                        ),
                        spacing="4",
                    ),
                ),
                spacing="4",
            ),
            position="fixed",
            width="100%",
            top="0px",
            z_index="1000",
            padding_x="4em",
            padding_y="1em",
            backdrop_filter="blur(10px)",
            background="rgba(255, 255, 255, 0.8)",
        ),
        rx.box(
            rx.image(
                src="math_app_logo.png",
                width="100%",
                height="100%",
                object_fit="cover",
                opacity="0.1",
                position="absolute",
                top="0",
                left="0",
                z_index="-1",
            ),
        ),
    ) 