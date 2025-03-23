from collections import Counter 
from mathapp.models import UserMathItem
import reflex as rx

class UserStats :
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
    def get_color(cls, name: str, names: list[str]=list([]))->str:
        print (f"{name}, {names}")
        COLORS = list(['yellow', 'red', 'green','blue','white','brown', 'orange'])
        for i, n in enumerate(names):
            if n == name:
                return COLORS[i]
        # i = names.index(name) 
        
        return "red"

    @classmethod
    def transform_problems_by_result( cls, user_problems: list[UserMathItem])->list[dict]:
        problem_type_counts = Counter(problem.Result for problem in user_problems)
        keys: list[str] = list(problem_type_counts.keys())
        print (f"keys: {keys} type: {type(keys)} ")
                
        users_problems_by_type = [
            {
                "name": t,
                "value": count,
                "fill": UserStats.get_color(t, keys)
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
    
    @classmethod
    def graph_table(cls, data_for_graph: list[dict]): 
        return rx.data_table(
            data=data_for_graph,
            columns=["name", "value"],
            pagination=True,
            search=True,
            sort=True,
        )

        
        
    @classmethod
    def graph_pie(cls, data_for_graph: list[dict]):

        
        return rx.recharts.pie_chart(
            rx.recharts.pie(
                data=data_for_graph,
                data_key="value",
                name_key="name",
                fill="#8884d8",
                label=True,
                label_line= False
            ),
            width="100%",
            height=300,
        )
