import reflex as rx

from mathapp.data_graph import UserMetricStats
from mathapp.state import State
from mathapp.state import State, USER_MATH_MODEL

USER_SORT_FIELDS = list(['Source', 'Year', 'Type', 'Competition', 'Difficulty', 'Result'])
USER_DISPLAY_FIELDS = list(['Problem', 'Response', 'Result'])

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
                            field, getattr(item, field)
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

def aime_content():
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