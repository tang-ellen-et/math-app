from sqlmodel import select
import reflex as rx
import json

from mathapp.models import UserMathItem, MathProblem
from mathapp.user_state import UserState
from mathapp.data_loading import load_user_problems, load_all_problems
from pandas import DataFrame 
from mathapp.data_graph import UserMetricStats

USER_MATH_MODEL = UserMathItem
MATH_MODEL = MathProblem 
# USER_SORT_FIELDS = list(['Source', 'Year', 'Type', 'Competition', 'Difficulty', 'Result'])

# Result values
RESULT_CORRECT = 'correct'
RESULT_WRONG="wrong"
RESULT_NA=""

data_file_path = "data_sources/mathv4_processed_3.csv"

class State(UserState):
    """The app state."""

    items: list[USER_MATH_MODEL] = []
    problems: list[MATH_MODEL] = []
    items_by_type: list[dict] = []
    items_by_result: list[dict] = []
    
    sort_value: str = ""
    num_items: int
    num_problems: int 
    current_item: USER_MATH_MODEL = USER_MATH_MODEL()
    current_math_problem: MATH_MODEL = MATH_MODEL()
    current_problemset = ''
    
    df_problems: DataFrame = DataFrame()

    def handle_add_submit(self, form_data: dict):
        """Handle the form submit."""
        print(f'###### handle_add_submit: {form_data}')
        self.current_item = form_data

    def handle_update_submit(self, form_data: dict):
        """Handle the form submit."""
        print (f'$$- handle_update_submit form_data: {form_data} ')
        
        self.current_item.Response = form_data['Response']
        
        print(f'$$-current_item: {self.current_item}')
        
        #find current math problem by current_math_problem problemId in problem
        self.current_math_problem = rx.session().exec(
                select(MATH_MODEL).where(MATH_MODEL.id == self.current_item.ProblemId)
            ).first()

        print(f'$$-current math problem: {self.current_math_problem}')
        
        if(self.current_item.Response.strip()==''):
            self.current_item.Result =  RESULT_NA
        elif(self.current_item.Response == self.current_math_problem.Answer):
            self.current_item.Result = RESULT_CORRECT
        else:
            print('$$ - Result: Wrong!')
            self.current_item.Result = RESULT_WRONG
        
        print(f'$$ - Result: {self.current_item.Result}!')
        
        # Update the item in the database
        with rx.session() as session:
            print (f'@@@@@@@@@@ update_item current_item: {str(self.current_item)} model: {USER_MATH_MODEL.id}')
            
            item = session.exec(
                select(USER_MATH_MODEL).where(USER_MATH_MODEL.id == self.current_item.id)
            ).first()

            item.Response = self.current_item.Response 
            item.Result = self.current_item.Result
            
            session.add(item)
            session.commit()
        
        # Refresh the entries to update the UI
        self.load_entries()

    def load_entries(self) -> list[USER_MATH_MODEL]:
        """Get all items from the database."""
        with rx.session() as session:
            self.items = session.exec(select(USER_MATH_MODEL).where(USER_MATH_MODEL.ProblemSet == self.current_problemset)).all()
            self.num_items = len(self.items)
            self.num_problems = len(self.problems)
            
            # session.exec (select(USER_MATH_MODEL.ProblemSet).distinct().order_by())

            if self.sort_value:
                self.items = sorted(
                    self.items,
                    key=lambda item: getattr(item, self.sort_value),
                )
            
            self.problems = session.exec(select(MATH_MODEL)).all()
            self.items_by_type= UserMetricStats.transform_problems_by_type(self.items)
            self.items_by_result = UserMetricStats.transform_problems_by_result(self.items)
            
    
    def sort_values(self, sort_value: str):
        self.sort_value = sort_value
        self.load_entries()

    def get_item(self, item: USER_MATH_MODEL):
        self.current_item = item

    def update_item(self):
        """This is now a no-op since we handle the update in handle_update_submit"""
        pass

    def generate_new_problemset(self):
        # Check authentication using UserState
        if not self.is_authenticated:
            return
            
        with rx.session() as session:            
            # always regenerate user problems when page load or reload
            self.current_problemset = load_user_problems(user=self.current_user, df_problems=self.df_problems, user_problems_model=USER_MATH_MODEL)
            first_entry = session.exec(USER_MATH_MODEL.select().where(USER_MATH_MODEL.ProblemSet == self.current_problemset)).first()
            
            self.load_entries()
    
    def set_last_problemset(self):
        with rx.session() as session:
            self.current_problemset = session.exec(select(USER_MATH_MODEL.ProblemSet).distinct().order_by(USER_MATH_MODEL.ProblemSet.desc())).first()
            
            self.load_entries()

    def reset_problems_db(self):
        """Reset the problems database by clearing all user problems and regenerating them."""
        with rx.session() as session:
            # Delete all existing user problems
            problems = session.exec(select(MATH_MODEL))
            for problem in problems:
                session.delete(problem)
            session.commit()
            print('$$ - problems deleted')
            
            self.on_load()
                # Generate a new problemset
        

    def on_load(self):
        """Check authentication on page load."""
        # Check if user is authenticated using UserState
        if self.check_auth_storage():
            # Check if the database is empty
            with rx.session() as session:
                # Attempt to retrieve the first entry in the MODEL table
                first_problem = session.exec(select(MATH_MODEL)).first()
                if first_problem is None and data_file_path != "":
                    self.df_problems = load_all_problems(data_file_path=data_file_path, math_model=MATH_MODEL, load_to_db=True)
                else:
                    self.df_problems = load_all_problems(data_file_path=data_file_path, math_model=MATH_MODEL, load_to_db=False)
                
                first_entry = session.exec(select(USER_MATH_MODEL)).first()
                if first_entry is None:
                    self.generate_new_problemset()
                else:
                    # find the max problemset
                    self.set_last_problemset()

            self.load_entries()


