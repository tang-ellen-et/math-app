import reflex as rx
from mathapp.state import State

def welcome_page() -> rx.Component:
    """Welcome page with a top navbar and centered content."""
    return rx.box(
        rx.fragment(
            # NAVBAR
            rx.hstack(
                # Left side buttons
                rx.hstack(
                    rx.link(rx.button("Mock AIME", size="4", color_scheme="cyan", variant="ghost", font_weight="bold"), href="/quiz"),
                    rx.link(rx.button("All Problems", size="4", color_scheme="cyan", variant="ghost", font_weight="bold"), href="/allproblems"),
                    rx.link(rx.button("Search", size="4", color_scheme="cyan", variant="ghost", font_weight="bold"), href="/search"),
                    spacing="6",
                    padding="0.5em 1em",
                    background_color=rx.color_mode_cond("teal.400", "teal.600"),
                    border_radius="md",
                ),
                rx.spacer(),
                rx.text(
                    "[placeholder title]",
                    font_size="4xl",
                    font_weight="bold",
                    color="cyan.700",
                    letter_spacing="-0.03em",
                    text_align="center",
                    flex="0 0 auto",
                ),
                rx.spacer(),
                # Right side buttons
                rx.hstack(
                    rx.link(rx.button("Dashboard", size="4", color_scheme="teal", variant="ghost", font_weight="bold"), href="/userdashboard"),
                    rx.link(rx.button("Resources", size="4", color_scheme="teal", variant="ghost", font_weight="bold"), href="/resources"),
                    rx.link(rx.button("Report a Bug", size="4", color_scheme="teal", variant="ghost", font_weight="bold"), href="/bug"),
                    rx.cond(
                        State.is_authenticated,
                        rx.link(
                            rx.button("Logout", size="4", color_scheme="red", variant="ghost"),
                            on_click=State.handle_logout,
                        ),
                        rx.link(
                            rx.button("Login / Signup", size="4", color_scheme="blue", variant="ghost"),
                            href="/login",
                        ),
                    ),
                    spacing="6",
                    padding="0.5em 1em",
                    background_color=rx.color_mode_cond("cyan.400", "cyan.600"),
                    border_radius="md",
                ),
                padding="1.5em 3em",
                background_color="white",
                border_bottom="1px solid #e2e8f0",
                position="sticky",
                top="0",
                z_index="10",
                align_items="center",
                width="100%",
            ),

            # HERO SECTION
            rx.center(
                rx.vstack(
                    rx.heading(
                        "Welcome to [placeholder name]",
                        size="9",
                        font_family="Inter",
                        font_weight="900",
                        color="white",
                        text_align="center",
                    ),
                    rx.text(
                        "Mock AMCs and AIME with thousands of fresh problems you haven't seen before.",
                        size="6",
                        color="white",
                        text_align="center",
                        font_weight="bold",
                        mt="1em",
                    ),
                    rx.vstack(
                        rx.text("• Original AMC 8/10/12 and AIME-style problems not from the MAA archive", color="white", text_align="center"),
                        rx.text("• Get a realistic estimate of your performance without score inflation", color="white", text_align="center"),
                        rx.text("• Mock exams with customizable difficulty perfect for pre-contest practice", color="white", text_align="center"),
                        rx.text("• Handcrafted problem sets, topic-specific practice, and more soon!", color="white", text_align="center"),
                        spacing="1",
                        mt="1em",
                    ),
                    rx.hstack(
                        rx.link(
                            rx.button("Start Practicing", size="4", color_scheme="green", padding_x="2em"),
                            href="/quiz"
                        ),
                        rx.link(
                            rx.button("Browse All Problems", size="4", color_scheme="cyan", padding_x="2em"),
                            href="/allproblems"
                        ),
                        spacing="6",
                        mt="2em"
                    ),
                    spacing="4",
                    padding="5em 2em",
                    background="linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%)",
                    border_radius="0",
                    width="100%",
                ),
                width="100%",
                padding="0",
            ),

            # FEATURE CARDS SECTION
            rx.center(
                rx.hstack(
                    rx.box(
                        rx.vstack(
                            rx.text("Mock AIME", font_weight="bold", font_size="lg", mb="2"),
                            rx.text("Take full-length Mock AIME exams with fresh problems.", font_size="sm", mb="2"),
                            rx.spacer(),
                            rx.spacer(),
                            rx.spacer(),
                            rx.spacer(),
                            rx.spacer(),
                            rx.link(
                                rx.button("Practice Now", size="3", color_scheme="green"),
                                href="/quiz",
                                margin_top="auto"
                            )
                        ),
                        display="flex",
                        flex_direction="column",
                        padding="1.5em",
                        border_radius="md",
                        box_shadow="md",
                        background_color="white",
                        width="250px",
                        cursor="pointer",
                        height="250px",
                    ),
                    rx.box(
                        rx.vstack(
                            rx.text("All Problems", font_weight="bold", font_size="lg", mb="2"),
                            rx.text("Browse thousands of unique AMC and AIME-style problems.", font_size="sm", mb="2"),
                            rx.spacer(),
                            rx.spacer(),
                            rx.spacer(),
                            rx.link(
                                rx.button("Browse", size="3", color_scheme="cyan"),
                                href="/allproblems",
                                margin_top="auto"
                            )
                        ),
                        display="flex",
                        flex_direction="column",
                        padding="1.5em",
                        border_radius="md",
                        box_shadow="md",
                        background_color="white",
                        width="250px",
                        cursor="pointer",
                        height="250px",
                    ),
                    rx.box(
                        rx.vstack(
                            rx.text("Search", font_weight="bold", font_size="lg", mb="2"),
                            rx.text("Quickly find problems by topic or difficulty.", font_size="sm", mb="2"),
                            rx.spacer(),
                            rx.spacer(),
                            rx.spacer(),
                            rx.spacer(),
                            rx.spacer(),
                            rx.link(
                                rx.button("Search", size="3", color_scheme="blue"),
                                href="/search",
                                margin_top="auto"
                            )
                        ),
                        display="flex",
                        flex_direction="column",
                        padding="1.5em",
                        border_radius="md",
                        box_shadow="md",
                        background_color="white",
                        width="250px",
                        cursor="pointer",
                        height="250px",
                    ),
                    spacing="2",
                    padding="2em",
                    width="100%",
                    justify_content="center",
                ),
                width="100%",
                background_color="#f5f7fa",
                padding="2em 0",
            ),
        ),
    )
