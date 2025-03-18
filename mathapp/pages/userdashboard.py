import reflex as rx
from mathapp.data_graph import UserStats
from mathapp.state import State

def userdashboard():
    return rx.box(
        rx.section(
            rx.center(rx.heading("User Exercise Dashboard"))
        ),
        rx.section(
            UserStats.graph_table(State.items_by_result)
    
        ),
        rx.section(
                rx.flex (
                UserStats.graph_pie( State.items_by_result),
                UserStats.graph(State.items_by_type)
            )
        ),
        rx.section(
            rx.center(rx.link("Home", href="/"))
        ),
        
        width = "70%"
        
    )