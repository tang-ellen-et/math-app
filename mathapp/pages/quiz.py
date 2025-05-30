import reflex as rx

from mathapp.data_graph import UserMetricStats
from mathapp.state import State
from mathapp.state import State, USER_MATH_MODEL
from mathapp.components.navbar import navbar
import urllib.parse

USER_SORT_FIELDS = list(['Source', 'Year', 'Type', 'Competition', 'Difficulty', 'Result'])
USER_DISPLAY_FIELDS = list(['Problem', 'My Answer', 'Result'])


def show_item(item: USER_MATH_MODEL):
    """Show an item in a table row."""
    return rx.table.row(
        rx.table.cell(rx.avatar(fallback=f'#{getattr(item, "ProblemId")}')),
        *[
            rx.table.cell(
                rx.badge(
                    getattr(item, "Result"),
                    color_scheme="green" if getattr(item, "Result") == "Correct" else "red",
                    variant="solid",
                )
            )
            for field in USER_DISPLAY_FIELDS
        ]
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

def response_input(item: USER_MATH_MODEL):
    """Create an input field for the response."""
    return rx.input(
        placeholder="Enter your answer",
        name=f"response_{item.ProblemId}",
        default_value=item.Response,
        width="100%",
        size="2",
    )

def quiz_content():
    return rx.fragment(
        rx.vstack(
            rx.divider(),
            rx.hstack(
                rx.heading(
                    f"Exercise ID: {State.current_problemset}",
                    size="3",
                    font_family="Inter",
                ),
                rx.link(
                rx.button(
                    "User Dashboard",
                    size="2",
                    color_scheme="gray",
                    variant="soft",
                ),
                href="/userdashboard",
                style={"textDecoration": "none"},
            ), 
                rx.spacer(),
                width="100%",
                padding_x="2em",
                padding_top="2em",
                padding_bottom="1em",
            ),
            rx.form(
                rx.vstack(
                    rx.hstack(
                        rx.button(
                            "Submit All Answers",
                            type="submit",
                            color_scheme="blue",
                            size="2",
                            font_weight="bold",
                            padding="1em 2em",
                            background="blue.500",
                            _hover={"background": "blue.600"},
                            box_shadow="lg",
                            style={"marginTop": "-4em"},
                        ),
                        width="100%",
                        padding_x="2em",
                        padding_bottom="1em",
                        justify="end",
                    ),
                    rx.table.root(
                        rx.table.header(
                            rx.table.row(
                                rx.table.column_header_cell("Id#", style={"fontSize": "20px", "fontWeight": "bold"}),
                                rx.table.column_header_cell("Source", style={"fontSize": "20px", "fontWeight": "bold"}),
                                rx.table.column_header_cell("Problem", style={"fontSize": "20px", "fontWeight": "bold"}),
                                rx.table.column_header_cell("Answer", style={"fontSize": "20px", "fontWeight": "bold"}),
                            ),
                        ),
                        rx.table.body(
                            rx.foreach(
                                State.items,
                                lambda item: rx.table.row(
                                    rx.table.cell(rx.avatar(fallback=f'#{getattr(item, "ProblemId")}')),
                                    rx.table.cell(
                                        rx.text(getattr(item, "Source"), style={"fontSize": "18px"})
                                    ),
                                    rx.table.cell(
                                        rx.box(
                                            rx.markdown(
                                                getattr(item, "Problem"),
                                                font_size="22px",  # or use a specific size like "20px"
                                                line_height="1.6",  # optional: improves readability
                                            ),  
                                            max_width="900px",
                                            white_space="normal",
                                            word_break="break-word",
                                            padding_y="2",
                                        )
                                    ),
                                    rx.table.cell(
                                        rx.input(
                                            placeholder="Enter your answer",
                                            name=f"response_{item.ProblemId}",
                                            default_value=item.Response,
                                            width="100%",
                                            size="3",
                                        )
                                    ),
                                )
                            )
                        ),
                        size="3",
                        width="100%",
                        sticky_header=True,
                    ),
                    width="100%",
                    mx="auto",
                    spacing="4",
                ),
                on_submit=State.submit_all_answers,
            ),
        ),
    )

def quiz_page() -> rx.Component:
    return rx.box(
        navbar(),
        rx.box(
            quiz_content(),
            margin_top="calc(50px + 2em)",
            padding="4em",
        ),
        font_family='sans serif'
    ) 