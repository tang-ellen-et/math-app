"""Welcome to Reflex! This file outlines the steps to create a basic app."""

# from sqlmodel import select
import reflex as rx

from mathapp.models import   UserMathItem, MathProblem
from mathapp.data_graph import UserStats


USER_SORT_FIELDS = list(['Source', 'Year', 'Type', 'Competition', 'Difficulty', 'Result'])


from mathapp.state import State, USER_MATH_MODEL, MATH_MODEL

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
                        "Cancel",
                        variant="soft",
                        color_scheme="gray",
                    ),
                ),
                rx.dialog.close(
                    rx.button(
                        "Submit Answer",
                        on_click=State.update_item,
                        variant="solid",
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

# font_family = "Comic Sans MS",
# rx.link("Example", href="/docs/library")
def navbar():
    return rx.hstack(
        rx.vstack(
            # rx.heading("Math App - Problems", size="8", font_family="Comic Sans MS", color='green'),
            rx.heading(rx.link("Math App - Problems", href="/about"), size="8", font_family="Comic Sans MS", color='green'),
        ),
        rx.spacer(),
        rx.button("Generate a Exercise!", on_click= State.generate_new_problemset),
        # add_item_ui(),
        rx.avatar(src='math_app_logo.png',  size="8"),
        rx.color_mode.button(),
        position="fixed",
        width="100%",
        top="0px",
        z_index="1000",
        padding_x="4em",
        padding_top="2em",
        padding_bottom="1em",
        backdrop_filter="blur(10px)",
    )


def show_item(item: USER_MATH_MODEL):
    """Show an item in a table row."""
    
    return rx.table.row(
        # rx.table.cell(rx.avatar(fallback="DA")),
        rx.table.cell(rx.avatar(fallback=f'#{getattr(item, "ProblemId")}')),
        rx.table.cell(rx.markdown (getattr(item, "Problem"))),
        *[
            rx.table.cell(getattr(item, field))
            for field in USER_MATH_MODEL.get_fields()
            if field != "id" and field != "Problem"  and field !="ProblemId" and field!="User" and field !="TestDate" and field != "ProblemSet" and field != "Result"
        ],
        # *[get_result_logo(item)],
        rx.table.cell( rx.avatar(src=f'{getattr(item, "Result")}.png', fallback=getattr(item, "Result")) )
        ,
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
                    # [*[field for field in USER_MATH_MODEL.get_fields() if field != "id" ]],
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
                            for field in USER_MATH_MODEL.get_fields()
                            if field != "id" and field !="ProblemId" and field!="User" and field !="TestDate" and field != "ProblemSet" 
                        ],
                        
                        rx.table.column_header_cell("Try"),
                        # rx.table.column_header_cell("Delete"),
                    ),
                ),
                rx.table.body(rx.foreach(State.items, show_item)),
                size="3",
                width="100%",
            ),
        ),
    )


# def custom():
#     return rx.text("Custom Route")

def index() -> rx.Component:
    return rx.box(
        navbar(),
        rx.box(
            content(),
            margin_top="calc(50px + 2em)",
            padding="4em",
        ),
        # font_family="Inter",
        font_family = "Comic Sans MS",
    )


# Create app instance and add index page.
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

app.add_page(about)
app.add_page(userdashboard, route="/userdashboard")