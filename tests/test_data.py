from collections import Counter 
from dataclasses import dataclass

@dataclass
class User(object):
    """The user model."""

    name: str
    email: str
    gender: str
    state: str 


users: list[User] = [
        User(name="Danilo Sousa", email="danilo@example.com", gender="Male", state="AZ"),
        User(name="Apple T.", email="a@example.com", gender="Female", state="CA"),
        User(name="Banana C.", email="b@example.com", gender="Male", state="AK"),
        User(name="Peach S.", email="p@example.com", gender="Female", state="AZ"),
        User(name="Zahra Ambessa", email="d@example.com", gender="Female", state="CA"),
        User(name="O Sousa", email="e@example.com", gender="Male", state="AZ"),
        User(name="C T.", email="a1@example.com", gender="Female", state="AZ"),
        User(name="D C.", email="b2@example.com", gender="Male", state="AK"),
        User(name="W S.", email="p3@example.com", gender="Female", state="CA"),
        User(name="SSS Q", email="232zahra@example.com", gender="Female", state="CA")
    ]


def test_counter():
    gender_counter = Counter( f"{user.gender}-{user.state}" for user in users)
    print (gender_counter)
    
    
    users_data_for_graph = [
            {
                "name": a,
                "value": count
            }
            for a, count in gender_counter.items()
            
        ]
    print('==============')
    print(users_data_for_graph)
    
    assert (len(gender_counter) == 4)