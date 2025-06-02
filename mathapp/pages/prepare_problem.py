import reflex as rx
from mathapp.components.navbar import navbar
from mathapp.state import State

from mathapp.state import State, ProblemCompare

def show_item(item: ProblemCompare):
    """Show an item in a table row."""
    
    return rx.table.row(
        # rx.table.cell(rx.avatar(fallback="DA")),
        rx.table.cell(rx.avatar(fallback=f'#{getattr(item, "id", "")}')),
        rx.table.cell(
            rx.text(getattr(item, "Problem"), font_size="small"),
            style={"maxWidth": "500px", "whiteSpace": "normal", "wordBreak": "break-word"}
        ),
        rx.table.cell(
            rx.text(getattr(item, "modified_problem"), font_size="small"),
            style={"maxWidth": "500px", "whiteSpace": "normal", "wordBreak": "break-word"}
        ),
        *[
            rx.table.cell(rx.text(getattr(item, field)))
            for field in ProblemCompare.get_fields()
            if field != "id" and field != "Problem" and field != "modified_problem"
        ]
    )

def prepare_problem() -> rx.Component:
    # Get all field names from the first item, or use the model fields if empty
    fields = ["Problem", "Answer", "modified_problem", "AIME_Answer"]
    return rx.box(
        navbar(),
        rx.container(
            rx.heading("Problems Preparation", size="6"),
            rx.text("Prepare and customize your own problem sets here. More features coming soon!"),
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Id#"),
                        *[
                            rx.table.column_header_cell(field)
                            for field in ProblemCompare.get_fields()
                            if field != "id"  
                        ]
                        # rx.table.column_header_cell("Delete"),
                    ),
                ),
                rx.table.body(rx.foreach(State.problem_compare, show_item)),
                size="3",
                width="1800px",
                max_width="100vw",
                sticky_header=True,
            ),
 
            padding="4em",
            width="1900px",
            max_width="100vw",
        )
    ) 