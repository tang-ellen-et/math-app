import reflex as rx

def search() -> rx.Component:
    return rx.container(
        rx.heading("Search", size="6"),
        rx.text("Search through problems or concepts."),
        padding="4em",
    )