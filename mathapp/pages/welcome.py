import reflex as rx

def welcome_page() -> rx.Component:
    """Welcome page with links to other pages."""
    return rx.center(
        rx.vstack(
            rx.container(
                rx.heading(
                    "Math App",
                    size="9",
                    font_family="Inter",
                    font_weight="900",
                    color="white",
                    text_align="center",
                    letter_spacing="-0.03em",
                ),
                width="100%",
                padding="2em",
                background="linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%)",
                border_radius="lg",
                mb="2em",
            ),
            rx.text(
                "Explore competition math problems, generate exercises, and track your progress.",
                size="5",
                font_family="Inter",
                mb="4em",
                text_align="center",
                max_width="800px",
                line_height="1.5",
                color="gray.700",
                white_space="nowrap",
                overflow="hidden",
                text_overflow="ellipsis",
            ),
            rx.hstack(
                # rx.link(
                #     rx.button(
                #         "AIME Test",
                #         size="4",
                #         color_scheme="blue",
                #         font_weight="600",
                #         padding_x="2em",
                #     ),
                #     href="/aime",
                # ),
                rx.link(
                    rx.button(
                        "AIME Quiz",
                        size="4",
                        color_scheme="cyan",
                        font_weight="600",
                        padding_x="2em",
                    ),
                    href="/quiz",
                ),
                rx.link(
                    rx.button(
                        "All Problems",
                        size="4",
                        color_scheme="green",
                        font_weight="600",
                        padding_x="2em",
                    ),
                    href="/allproblems",
                ),
                rx.link(
                    rx.button(
                        "Login / Signup",
                        size="4",
                        color_scheme="teal",
                        font_weight="600",
                        padding_x="2em",
                    ),
                    href="/login",
                ),
                rx.link(
                    rx.button(
                        "About",
                        size="4",
                        color_scheme="purple",
                        font_weight="600",
                        padding_x="2em",
                    ),
                    href="/about",
                ),
                spacing="8",
                wrap="wrap",
                justify="center",
            ),
            justify="center",
            align="center",
            spacing="8",
            padding="4em",
            max_width="1000px",
        ),
        width="100%",
        height="100vh",
        display="flex",
        align_items="center",
        justify_content="center",
        font_family="sans serif",
        background="linear-gradient(135deg, #f8fafc 0%, #ffffff 100%)",
    ) 