import reflex as rx

# Id,Problem,Answer,Solution,Source,Year,Type,Competition,Difficulty,Img

class MathProblem(rx.Model, table=True):
    """The math problem model."""
    Problem: str
    Answer: str
    Solution: str
    Source: str
    Year: str
    Type: str
    Competition: str
    Difficulty: str
    Img: str


class UserMathItem(rx.Model, table=True):
    """The math problem table view summary model."""
    Problem: str
    Source: str
    Year: str
    Type: str
    Competition: str
    Difficulty: str
    Response: str
    Result: str 
    User: str 
    ProblemSet: str
    TestDate: str
    ProblemId: str 





