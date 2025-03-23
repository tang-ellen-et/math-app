from sqlmodel import select
import reflex as rx

from mathapp.models import UserMathItem, MathProblem, User
from mathapp.user_state import UserState
from mathapp.data_loading import load_user_problems, load_all_problems
from pandas import DataFrame 
from mathapp.data_graph import UserStats
from mathapp.user_state import UserState

USER_MATH_MODEL = UserMathItem
MATH_MODEL = MathProblem 
# USER_SORT_FIELDS = list(['Source', 'Year', 'Type', 'Competition', 'Difficulty', 'Result'])

# Result values
RESULT_CORRECT = 'correct'
RESULT_WRONG="wrong"
RESULT_NA=""

data_file_path = "data_sources/mathv4_processed_3.csv"

class State(rx.State):
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
    
    # User authentication state
    is_authenticated: bool = False
    current_user: str = ""
    error_message: str = ""
    signup_error_message: str = ""

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
            self.items_by_type= UserStats.transform_problems_by_type(self.items)
            self.items_by_result = UserStats.transform_problems_by_result(self.items)
            
    
    def sort_values(self, sort_value: str):
        self.sort_value = sort_value
        self.load_entries()

    def get_item(self, item: USER_MATH_MODEL):
        self.current_item = item

    def update_item(self):
        """This is now a no-op since we handle the update in handle_update_submit"""
        pass

    def generate_new_problemset(self):
        # Check authentication using the current state's values
        print (f'@@@@@@@@@@ generate_new_problemset is_authenticated: {self.is_authenticated}')
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
        # Check if the database is empty
        
        with rx.session() as session:
            # Attempt to retrieve the first entry in the MODEL table
            first_problem = session.exec (select(MATH_MODEL)).first()
            if first_problem is None and data_file_path != "":
                self.df_problems = load_all_problems(data_file_path=data_file_path, math_model=MATH_MODEL, load_to_db=True)
            else:
                self.df_problems = load_all_problems(data_file_path=data_file_path, math_model=MATH_MODEL, load_to_db=False)
            
            # always regnerate user problems when page load or relad
            # load_user_problems(user=USER, df_problems=df_problems, user_problems_model= USER_MATH_MODEL)
            first_entry = session.exec(select(USER_MATH_MODEL)).first()
            if first_entry is None:
                self.generate_new_problemset()
            else:
                # find the max problemset
                self.set_last_problemset()


            # # If nothing was returned load data from the csv file
            # if first_entry is None:
            #     load_user_problems(user=USER, df_problems=df_problems, user_problems_model= USER_MATH_MODEL)

        self.load_entries()

    def handle_login(self, form_data: dict):
        """Handle user login."""
        username = form_data.get("username", "").strip()
        password = form_data.get("password", "").strip()
        
        if not username or not password:
            self.error_message = "Please enter both username and password"
            return None
            
        # Hash the password for comparison
        import hashlib
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        with rx.session() as session:
            user = session.exec(
                select(User).where(
                    (User.username == username) & (User.password_hash == password_hash)
                )
            ).first()
            
            if user:
                self.is_authenticated = True
                self.current_user = username
                self.error_message = ""
                return rx.redirect("/")
            else:
                self.error_message = "Invalid username or password"
                return None

    def handle_signup(self, form_data: dict):
        """Handle user signup."""
        username = form_data.get("username", "").strip()
        email = form_data.get("email", "").strip()
        password = form_data.get("password", "").strip()
        confirm_password = form_data.get("confirm_password", "").strip()
        
        # Basic validation
        if not username or not email or not password or not confirm_password:
            self.signup_error_message = "All fields are required"
            return None
            
        if password != confirm_password:
            self.signup_error_message = "Passwords do not match"
            return None
            
        if len(password) < 6:
            self.signup_error_message = "Password must be at least 6 characters long"
            return None

        # Check if username or email already exists
        with rx.session() as session:
            existing_user = session.exec(
                select(User).where(
                    (User.username == username) | (User.email == email)
                )
            ).first()
            
            if existing_user:
                self.signup_error_message = "Username or email already exists"
                return None

            # Create new user
            from datetime import datetime
            import hashlib
            
            # Hash the password (in a real app, use a proper password hashing library)
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            new_user = User(
                username=username,
                email=email,
                password_hash=password_hash,
                created_at=datetime.now().isoformat()
            )
            
            session.add(new_user)
            session.commit()
            
            # Set user as authenticated
            self.is_authenticated = True
            self.current_user = username
            self.signup_error_message = ""
            return rx.redirect("/")

    def handle_logout(self):
        """Handle user logout."""
        self.is_authenticated = False
        self.current_user = ""
        return rx.redirect("/")


