import reflex as rx

# from ..state import AuthState

def about():
    return rx.box(
        rx.heading("About Math App"),
        rx.section( rx.text("Math Lover can find quality math problems from various competitions with the right difficulty level to practice.\nThey can also see their performance history.")),
        rx.link("Home", href="/")
    )
