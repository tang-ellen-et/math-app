import reflex as rx

def bug_report() -> rx.Component:
    return rx.container(
        rx.heading("Report a Bug", size="6"),
        rx.text("Let us know what's broken or could be improved."),
        padding="4em",
    )
