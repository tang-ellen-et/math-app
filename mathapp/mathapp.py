"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from mathapp.models import UserMathItem, MathProblem
from mathapp.data_graph import UserStats
from mathapp.state import State, USER_MATH_MODEL, MATH_MODEL

USER_SORT_FIELDS = list(['Source', 'Year', 'Type', 'Competition', 'Difficulty', 'Result'])
USER_DISPLAY_FIELDS = list(['Problem', 'Response', 'Result'])

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

def update_fields_and_attrs(field, attr):
    return rx.flex(
        rx.text(
            field,
            as_="div",
            size="2", 
            mb="1",
            weight="bold",
        ),
        rx.input(
            placeholder=attr,
            name=field,
            default_value=attr,
        ),
        direction="column",
        spacing="2",
    )

def update_item_ui(item):
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon("square_pen", width=24, height=24),
                color="white",
                on_click=lambda: State.get_item(item),
            ),
        ),
        rx.dialog.content(
            rx.dialog.title(f"Try Problem #{getattr(item, 'ProblemId')}"),
            rx.dialog.description(
                rx.markdown(getattr(item,"Problem")),
                size="4",
                mb="4",
                padding_bottom="1em",
            ),
            rx.form(
                rx.flex(
                    *[
                        update_fields_and_attrs(
                            field, getattr(State.current_item, field)
                        )
                        for field in USER_MATH_MODEL.get_fields()
                        if field == "Response" 
                    ],
                    rx.box(
                        rx.button(
                            "Update",
                            type="submit",
                            on_click=State.update_item,
                        ),
                    ),
                    direction="column",
                    spacing="3",
                ),
                on_submit=State.handle_update_submit,
                reset_on_submit=True,
            ),
            rx.flex(
                rx.dialog.close(
                    rx.button(
                        "Close",
                        variant="soft",
                        color_scheme="gray",
                    ),
                ),
                padding_top="1em",
                spacing="3",
                mt="4",
                justify="end",
            ),
            style={"max_width": 450},
            box_shadow="lg",
            padding="1em",
            border_radius="25px",
        ),
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
                    color='green',
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
                    State.is_authenticated,
                    rx.hstack(
                        rx.text(
                            f"Welcome, {State.current_user}",
                            color="green",
                            font_weight="bold",
                            size="3",
                        ),
                        rx.button(
                            "Logout",
                            on_click=State.handle_logout,
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

def show_item(item: USER_MATH_MODEL):
    """Show an item in a table row."""
    return rx.table.row(
        rx.table.cell(rx.avatar(fallback=f'#{getattr(item, "ProblemId")}')),
        *[
            rx.table.cell(
                rx.markdown(getattr(item, field)) if field == "Problem" 
                else rx.avatar(src=f'{getattr(item, field)}.png', fallback=getattr(item, field)) if field == "Result"
                else getattr(item, field)
            )
            for field in USER_DISPLAY_FIELDS
        ],
        rx.table.cell(
            update_item_ui(item),
        )
    )

def content():
    return rx.fragment(
        rx.vstack(
            rx.divider(),
            rx.hstack(
                rx.heading(
                    f"Total: {State.num_items} Problems - Exercise#_{State.current_problemset}",
                    size="5",
                    font_family="Inter",
                ),
                rx.link("User Dashboard", href="/userdashboard"),
                rx.spacer(),
                rx.select(
                    [*[field for field in USER_SORT_FIELDS ]],
                    placeholder="Sort By: Problem Type",
                    size="3",
                    on_change=lambda sort_value: State.sort_values(sort_value),
                    font_family="Inter",
                ),
                width="100%",
                padding_x="2em",
                padding_top="2em",
                padding_bottom="1em",
            ),
            UserStats.graph(State.items_by_type),
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Id#"),
                        *[
                            rx.table.column_header_cell(field)
                            for field in USER_DISPLAY_FIELDS
                        ],
                        rx.table.column_header_cell("Try"),
                    ),
                ),
                rx.table.body(rx.foreach(State.items, show_item)),
                size="3",
                width="100%",
            ),
        ),
    )

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
                        State.signup_error_message != "",
                        rx.text(State.signup_error_message, color="red"),
                        None,
                    ),
                    rx.button("Sign Up", type="submit"),
                    spacing="4",
                ),
                on_submit=State.handle_signup,
            ),
            spacing="4",
            align="center",
            padding="2em",
        ),
        margin_top="calc(50px + 2em)",
    )

def index() -> rx.Component:
    return rx.box(
        navbar(),
        rx.box(
            content(),
            margin_top="calc(50px + 2em)",
            padding="4em",
        ),
        font_family='sans serif'
    )

app = rx.App(
    theme=rx.theme(
        appearance="light", has_background=True, radius="large", accent_color="grass"
    ),
    stylesheets=["https://fonts.googleapis.com/css?family=Inter"],
)

app.add_page(
    index,
    on_load=State.on_load,
    title="Math App",
    description="Try Competition Math Problem sets Here!",
)

from mathapp.pages.about import about
from mathapp.pages.userdashboard import userdashboard
from mathapp.pages.allproblems import allproblems

app.add_page(about)
app.add_page(userdashboard, route="/userdashboard")
app.add_page(allproblems, route="/allproblems")
app.add_page(login, route="/login")
app.add_page(signup, route="/signup")