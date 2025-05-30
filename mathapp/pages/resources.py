import reflex as rx

# Placeholder for Resources page
def resources() -> rx.Component:
    return rx.container(
        rx.heading("Resources", size="6"),
        rx.text("Useful guides, formulas, and external links will be added here."),
        padding="4em",
    )