import reflex as rx
from mathapp.components.navbar import navbar
from mathapp.state import State

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
                        *[rx.table.column_header_cell(field) for field in fields]
                    )
                ),
                rx.table.body(
                    rx.foreach(
                        State.problem_compare,
                        lambda item: rx.table.row([
                            rx.table.cell(
                                rx.text(getattr(item, "Problem"), font_size="large"),
                                style={"maxWidth": "350px", "whiteSpace": "normal", "wordBreak": "break-word"}
                            ),
                            rx.table.cell(getattr(item, "Answer")),
                            rx.table.cell(
                                rx.text(getattr(item, "modified_problem"), font_size="large"),
                                style={"maxWidth": "350px", "whiteSpace": "normal", "wordBreak": "break-word"}
                            ),
                            rx.table.cell(getattr(item, "AIME_Answer")),
                        ])
                    )
                ),
                size="3",
                width="1600px",
                sticky_header=True,
            ),
            padding="4em",
            width="1700px",
            max_width="100vw",
        )
    ) 