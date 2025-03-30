"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from mathapp.models import UserMathItem, MathProblem
from mathapp.data_graph import UserMetricStats
from mathapp.state import State
from mathapp.pages.about import about
from mathapp.pages.userdashboard import userdashboard
from mathapp.pages.allproblems import allproblems
from mathapp.pages.login import login
from mathapp.pages.signup import signup
from mathapp.state import State
from mathapp.user_state import UserState
from mathapp.pages.aime import aime_content

def add_fields(field):
    return rx.flex(
        rx.text(
            field,
            as_="div", 
            size="2",
            mb="1",
            weight="bold",
        ),
        rx.input(
            placeholder=field,
            name=field,
        ),
        direction="column",
        spacing="2",
    )

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

def welcome_page() -> rx.Component:
    """Welcome page with links to other pages."""
    return rx.box(
        rx.vstack(
            rx.heading("Welcome to Math App - WELCOME!", size="4", font_family="Inter", mb="1em"),
            rx.text(
                "Explore competition math problems, generate exercises, and track your progress.",
                size="4",  # Changed from "lg" to "4"
                font_family="Inter",
                mb="2em",
            ),
            rx.hstack(
                rx.link(
                    rx.button("AIME Test", size="3", color_scheme="blue"),  # Changed from "lg" to "3"
                    href="/aime",
                ),
                rx.link(
                    rx.button("All Problems", size="3", color_scheme="green"),  # Changed from "lg" to "3"
                    href="/allproblems",
                ),
                rx.link(
                    rx.button("Login / Signup", size="3", color_scheme="teal"),  # Changed from "lg" to "3"
                    href="/login",
                ),
                rx.link(
                    rx.button("About", size="3", color_scheme="purple"),  # Changed from "lg" to "3"
                    href="/about",
                ),
                spacing="3",  # Changed from "1em" to "3"
            ),
            justify="center",
            align="center",
            padding="4em",
        ),
        font_family="sans serif",
        text_align="center",
    )

def index() -> rx.Component:
    return rx.box(
        navbar(),
        rx.box(
            aime_content(),
            margin_top="calc(50px + 2em)",
            padding="4em",
        ),
        font_family='sans serif'
    )

app = rx.App(
    theme=rx.theme(
        appearance="light", has_background=True, radius="large", accent_color="cyan"
    ),
    stylesheets=["https://fonts.googleapis.com/css?family=Inter"],
)

app.add_page(
    welcome_page,
    route="/",
    on_load=State.on_load,
    title="Welcome to Math App",
    description="Explore competition math problems and track your progress.",
)

app.add_page(
    index,
    route="/aime",
    title="AIME Test",
    description="Try AIME competition math problems.",
)

app.add_page(about)
app.add_page(userdashboard, route="/userdashboard")
app.add_page(allproblems, route="/allproblems")
app.add_page(login, route="/login")
app.add_page(signup, route="/signup")