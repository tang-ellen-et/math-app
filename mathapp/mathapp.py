"""Welcome to Reflex! This file outlines the steps to create a basic app."""

from sqlmodel import select
import reflex as rx

from mathapp.models import   UserMathItem, MathProblem

from mathapp.data_loading import load_user_problems, load_all_problems
from pandas import DataFrame 
from mathapp.data_graph import UserStats

USER_MATH_MODEL = UserMathItem
MATH_MODEL = MathProblem 
USER_SORT_FIELDS = list(['Source', 'Year', 'Type', 'Competition', 'Difficulty', 'Result'])

# Result values
RESULT_CORRECT = 'correct'
RESULT_WRONG="wrong"
RESULT_NA=""

data_file_path = "data_sources/mathv4_processed_3.csv"

USER = 'Ellen'



class State(rx.State):
    """The app state."""

    items: list[USER_MATH_MODEL] = []
    problems: list[MATH_MODEL] = []
    items_by_type: list[dict] = []
    
    sort_value: str = ""
    num_items: int
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

    def load_entries(self) -> list[USER_MATH_MODEL]:
        """Get all items from the database."""
        with rx.session() as session:
            self.items = session.exec(select(USER_MATH_MODEL).where(USER_MATH_MODEL.ProblemSet == self.current_problemset)).all()
            self.num_items = len(self.items)
            
            # session.exec (select(USER_MATH_MODEL.ProblemSet).distinct().order_by())

            if self.sort_value:
                self.items = sorted(
                    self.items,
                    key=lambda item: getattr(item, self.sort_value),
                )
            
            self.problems = session.exec(select(MATH_MODEL)).all()
            self.items_by_type= UserStats.transform_problems_by_type(self.items)
    
    def sort_values(self, sort_value: str):
        self.sort_value = sort_value
        self.load_entries()

    def get_item(self, item: USER_MATH_MODEL):
        self.current_item = item

    def update_item(self):

        """Update an item in the database."""
        with rx.session() as session:
            print (f'@@@@@@@@@@ update_item current_item: {str(self.current_item)} model: {USER_MATH_MODEL.id}')
            
            item = session.exec(
                select(USER_MATH_MODEL).where(USER_MATH_MODEL.id == self.current_item.id)
            ).first()

            # for field in MODEL.get_fields():
            #     # if field != "id":
            #     if field == "Response":
            #         setattr(item, field, self.current_item[field])
            item.Response = self.current_item.Response 
            item.Result = self.current_item.Result
            
            
            session.add(item)
            session.commit()
        self.load_entries()
        content()


    def generate_new_problemset(self):
        with rx.session() as session:            
            # always regnerate user problems when page load or relad
            self.current_problemset = load_user_problems(user=USER, df_problems= self.df_problems, user_problems_model= USER_MATH_MODEL)
            first_entry = session.exec(USER_MATH_MODEL.select().where(USER_MATH_MODEL.ProblemSet == self.current_problemset)).first()
            
            self.load_entries()
    
    def set_last_problemset(self):
        with rx.session() as session:
            self.current_problemset = session.exec(select(USER_MATH_MODEL.ProblemSet).distinct().order_by(USER_MATH_MODEL.ProblemSet.desc())).first()
            
            self.load_entries()

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


def add_fields(field):
    return rx.flex(
        rx.text(
            field,
            as_="div",
            size="2",
            mb="1",
            weight="bold",
        ),
        rx.input(
            placeholder=field,
            name=field,
        ),
        direction="column",
        spacing="2",
    )


def update_fields_and_attrs(field, attr):
    return rx.flex(
        rx.text(
            field,
            as_="div",
            size="2",
            mb="1",
            weight="bold",
        ),
        rx.input(
            placeholder=attr,
            name=field,
            default_value=attr,
        ),
        direction="column",
        spacing="2",
    )

def update_item_ui(item):
    print (f' ============  update_item_ui:  {item}')
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon("square_pen", width=24, height=24),
                color="white",
                on_click=lambda: State.get_item(item),
            ),
        ),
        rx.dialog.content(
            rx.dialog.title(f"Try Problem #{getattr(item, 'ProblemId')}"),
            rx.dialog.description(
                rx.markdown(getattr(item,"Problem")),
                size="4",
                mb="4",
                padding_bottom="1em",
            ),
            rx.form(
                rx.flex(
                    *[
                        update_fields_and_attrs(
                            field, getattr(State.current_item, field)
                        )
                        for field in USER_MATH_MODEL.get_fields()
                        if field == "Response" 
                    ],
                    rx.box(
                        rx.button(
                            "Update",
                            type="submit",
                        ),
                    ),
                    direction="column",
                    spacing="3",
                ),
                on_submit=State.handle_update_submit,
                reset_on_submit=True,
            ),
            rx.flex(
                rx.dialog.close(
                    rx.button(
                        "Cancel",
                        variant="soft",
                        color_scheme="gray",
                    ),
                ),
                rx.dialog.close(
                    rx.button(
                        "Submit Answer",
                        on_click=State.update_item,
                        variant="solid",
                    ),
                ),
                padding_top="1em",
                spacing="3",
                mt="4",
                justify="end",
            ),
            style={"max_width": 450},
            box_shadow="lg",
            padding="1em",
            border_radius="25px",
        ),
    )

# font_family = "Comic Sans MS",
# rx.link("Example", href="/docs/library")
def navbar():
    return rx.hstack(
        rx.vstack(
            # rx.heading("Math App - Problems", size="8", font_family="Comic Sans MS", color='green'),
            rx.heading(rx.link("Math App - Problems", href="/about"), size="8", font_family="Comic Sans MS", color='green'),
        ),
        rx.spacer(),
        rx.button("Generate a Exercise!", on_click= State.generate_new_problemset),
        # add_item_ui(),
        rx.avatar(src='math_app_logo.png',  size="8"),
        rx.color_mode.button(),
        position="fixed",
        width="100%",
        top="0px",
        z_index="1000",
        padding_x="4em",
        padding_top="2em",
        padding_bottom="1em",
        backdrop_filter="blur(10px)",
    )


def show_item(item: USER_MATH_MODEL):
    """Show an item in a table row."""
    
    return rx.table.row(
        # rx.table.cell(rx.avatar(fallback="DA")),
        rx.table.cell(rx.avatar(fallback=f'#{getattr(item, "ProblemId")}')),
        rx.table.cell(rx.markdown (getattr(item, "Problem"))),
        *[
            rx.table.cell(getattr(item, field))
            for field in USER_MATH_MODEL.get_fields()
            if field != "id" and field != "Problem"  and field !="ProblemId" and field!="User" and field !="TestDate" and field != "ProblemSet" and field != "Result"
        ],
        # *[get_result_logo(item)],
        rx.table.cell( rx.avatar(src=f'{getattr(item, "Result")}.png', fallback=getattr(item, "Result")) )
        ,
        rx.table.cell(
            update_item_ui(item),
        )
    )


def content():
    return rx.fragment(
        rx.vstack(
            rx.divider(),
            rx.hstack(
                rx.heading(
                    f"Total: {State.num_items} Problems - Exercise#_{State.current_problemset}",
                    size="5",
                    font_family="Inter",
                ),
                rx.spacer(),
                rx.select(
                    # [*[field for field in USER_MATH_MODEL.get_fields() if field != "id" ]],
                    [*[field for field in USER_SORT_FIELDS ]],
                    placeholder="Sort By: Problem Type",
                    size="3",
                    on_change=lambda sort_value: State.sort_values(sort_value),
                    font_family="Inter",
                ),
                width="100%",
                padding_x="2em",
                padding_top="2em",
                padding_bottom="1em",
            ),
            UserStats.graph(State.items_by_type),
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Id#"),
                        *[
                            rx.table.column_header_cell(field)
                            for field in USER_MATH_MODEL.get_fields()
                            if field != "id" and field !="ProblemId" and field!="User" and field !="TestDate" and field != "ProblemSet" 
                        ],
                        
                        rx.table.column_header_cell("Try"),
                        # rx.table.column_header_cell("Delete"),
                    ),
                ),
                rx.table.body(rx.foreach(State.items, show_item)),
                size="3",
                width="100%",
            ),
        ),
    )


# def custom():
#     return rx.text("Custom Route")

def index() -> rx.Component:
    return rx.box(
        navbar(),
        rx.box(
            content(),
            margin_top="calc(50px + 2em)",
            padding="4em",
        ),
        # font_family="Inter",
        font_family = "Comic Sans MS",
    )


# Create app instance and add index page.
app = rx.App(
    theme=rx.theme(
        appearance="light", has_background=True, radius="large", accent_color="grass"
    ),
    stylesheets=["https://fonts.googleapis.com/css?family=Inter"],
)

app.add_page(
    index,
    on_load=State.on_load,
    title="Math App",
    description="Try Competition Math Problem sets Here!",
)
from mathapp.pages.about import about
from mathapp.pages.userdashboard import userdashboard

app.add_page(about)
app.add_page(userdashboard, route="/userdashboard")