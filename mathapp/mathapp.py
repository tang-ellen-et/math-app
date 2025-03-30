"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from mathapp.models import UserMathItem, MathProblem
from mathapp.data_graph import UserMetricStats
from mathapp.state import State
from mathapp.pages.about import about
from mathapp.pages.userdashboard import userdashboard
from mathapp.pages.allproblems import allproblems
from mathapp.pages.login import login
from mathapp.pages.signup import signup
from mathapp.state import State
from mathapp.user_state import UserState
from mathapp.pages.aime import aime_page
from mathapp.pages.aimev2 import aimev2_page
from mathapp.pages.welcome import welcome_page


app = rx.App(
    theme=rx.theme(
        appearance="light", has_background=True, radius="large", accent_color="cyan"
    ),
    stylesheets=["https://fonts.googleapis.com/css?family=Inter"],
)

app.add_page(
    welcome_page,
    route="/",
    on_load=State.on_load,
    title="Welcome to Math App",
    description="Explore competition math problems and track your progress.",
)

app.add_page(
    aime_page,
    route="/aime",
    title="AIME Test",
    description="Try AIME competition math problems.",
)

app.add_page(
    aimev2_page,
    route="/aimev2",
    title="AIME v2",
    description="Try AIME competition math problems v2.",
)

app.add_page(about)
app.add_page(userdashboard, route="/userdashboard")
app.add_page(allproblems, route="/allproblems")
app.add_page(login, route="/login")
app.add_page(signup, route="/signup")