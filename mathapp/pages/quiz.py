import reflex as rx

from mathapp.data_graph import UserMetricStats
from mathapp.state import State
from mathapp.state import State, USER_MATH_MODEL
from mathapp.components.navbar import navbar

USER_SORT_FIELDS = list(['Source', 'Year', 'Type', 'Competition', 'Difficulty', 'Result'])
USER_DISPLAY_FIELDS = list(['Problem', 'My Answer', 'Result'])

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
            UserMetricStats.graph(State.items_by_type),
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
                        ),
                        width="100%",
                        padding_x="2em",
                        padding_bottom="1em",
                        justify="end",
                    ),
                    rx.table.root(
                        rx.table.header(
                            rx.table.row(
                                rx.table.column_header_cell("Id#"),
                                rx.table.column_header_cell("Problem"),
                                rx.table.column_header_cell("My Answer"),
                                rx.table.column_header_cell("Result"),
                            ),
                        ),
                        rx.table.body(
                            rx.foreach(
                                State.items,
                                lambda item: rx.table.row(
                                    rx.table.cell(rx.avatar(fallback=f'#{getattr(item, "ProblemId")}')),
                                    rx.table.cell(rx.markdown(getattr(item, "Problem"))),
                                    rx.table.cell(
                                        rx.input(
                                            placeholder="Enter your answer",
                                            name=f"response_{item.ProblemId}",
                                            default_value=item.Response,
                                            width="100%",
                                            size="2",
                                        )
                                    ),
                                    rx.table.cell(rx.avatar(src=f'{getattr(item, "Result")}.png', fallback=getattr(item, "Result"))),
                                )
                            )
                        ),
                        size="3",
                        width="100%",
                    ),
                    width="100%",
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