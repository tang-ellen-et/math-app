import reflex as rx
from sqlmodel import select
from datetime import datetime
import hashlib

from mathapp.models import User

class UserState(rx.State):
    """The user authentication state."""

    is_authenticated: bool = False
    current_user: str = ""
    error_message: str = ""
    signup_error_message: str = ""

    def handle_login(self, form_data: dict):
        """Handle user login."""
        username = form_data.get("username", "").strip()
        password = form_data.get("password", "").strip()
        
        if not username or not password:
            self.error_message = "Please enter both username and password"
            return None
            
        # Hash the password for comparison
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