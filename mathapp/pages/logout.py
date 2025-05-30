def logout() -> rx.Component:
    return rx.container(
        rx.heading("You have been logged out", size="6"),
        rx.text("Thanks for visiting. Redirecting to home..."),
        padding="4em",
    )