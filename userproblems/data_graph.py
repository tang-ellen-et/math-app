from collections import Counter 
from dataclasses import dataclass
from userproblems.models import UserMathItem, MathProblem
import reflex as rx

class UserStats :
    # def __init__(self, user_problems: list[UserMathItem]):
    #     self.user_problems = user_problems
    #     self.users_problems_for_graph: list[dict] = []

    @classmethod
    def transform_problems_by_type( cls, user_problems: list[UserMathItem])->list[dict]:
        problem_type_counts = Counter(problem.Type for problem in user_problems)
        users_problems_by_type = [
            {
                "name": t,
                "value": count
            }
            for t, count in problem_type_counts.items()
            
        ]
        return users_problems_by_type

    @classmethod
    def graph(cls, data_for_graph: list[dict]):
        return rx.recharts.bar_chart(
            rx.recharts.bar(
                data_key="value",
                stroke=rx.color("accent", 9),
                fill=rx.color("accent", 8),
            ),
            rx.recharts.x_axis(data_key="name"),
            rx.recharts.y_axis(),
            data=data_for_graph,
            width="100%",
            height=250,
    )

