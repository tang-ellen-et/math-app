import reflex as rx
from mathapp.data_graph import UserMetricStats

from mathapp.state import State, MATH_MODEL
# from ..state import AuthState

PROBLEM_SORT_FIELDS = list(['Source', 'Year', 'Type', 'Competition', 'Difficulty'])

def show_item(item: MATH_MODEL):
    """Show an item in a table row."""
    
    return rx.table.row(
        # rx.table.cell(rx.avatar(fallback="DA")),
        rx.table.cell(rx.avatar(fallback=f'#{getattr(item, "id")}')),
        rx.table.cell(rx.markdown (getattr(item, "Problem"))),
        *[
            rx.table.cell(getattr(item, field))
            for field in MATH_MODEL.get_fields()
            if field != "id" and field != "Problem"   
        ]
        # *[get_result_logo(item)],
        # rx.table.cell( rx.avatar(src=f'{getattr(item, "Result")}.png', fallback=getattr(item, "Result")) ),
        # rx.table.cell(
        #     update_item_ui(item),
        # )
    )

def content():
    return rx.fragment(
        rx.vstack(
            rx.divider(),
            rx.hstack(
                rx.heading(
                    f"Total: {State.num_problems} Problems",
                    size="5",
                    font_family="Inter",
                ),
                rx.link("Home", href="/"),
                rx.spacer(),
                rx.select(
                    # [*[field for field in USER_MATH_MODEL.get_fields() if field != "id" ]],
                    [*[field for field in PROBLEM_SORT_FIELDS ]],
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
            # UserStats.graph(State.items_by_type),
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Id#"),
                        *[
                            rx.table.column_header_cell(field)
                            for field in MATH_MODEL.get_fields()
                            if field != "id"  
                        ]
                        # rx.table.column_header_cell("Delete"),
                    ),
                ),
                rx.table.body(rx.foreach(State.problems, show_item)),
                size="3",
                width="100%",
            ),
        ),
    )

def allproblems() -> rx.Component:
    return rx.box(
        content(),
        margin_top="calc(50px + 2em)",
        padding="4em",
        # font_family="Inter",
        font_family = "sans serif",
    )