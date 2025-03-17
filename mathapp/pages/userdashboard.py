import reflex as rx

def userdashboard():
    return rx.box(
        rx.heading("User Exercise Dashboard"),
        rx.section( rx.text("Placeholder-User Exercise Dashboard")),
        rx.link("Home", href="/")
    )