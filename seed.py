from app import app
from models import db, connect_db, User, Issue, Comment, Role, Priority, Resolution, Status

db.drop_all()
db.create_all()

# Sample users.

u1 = User(
    email="user1@example.com",
    first_name="Admin",
    last_name="User",
    password="password"
)

u2 = User(
    email="user2@example.com",
    first_name="Regular",
    last_name="User",
    password="password"
)

u3 = User(
    email="user3@example.com",
    first_name="Assignee",
    last_name="User",
    password="password"
)

# Sample issues

i1 = Issue(
    title="Sample Issue 1",
    summary="Short description of Issue 1",
    text="Longer description text describing Issue 1.  This is a text field, so can contain much text."
)

i2 = Issue(
    title="Sample Issue 2",
    summary="Short description of Issue 2",
    text="Longer description text describing Issue 2.  So much text can fit here, you wouldn't believe it."
)

i3 = Issue(
    title="Sample Issue 3",
    summary="Short description of Issue 2",
    text="Longer description text describing Issue 3.  Look at all of this text!  Holy Cow!"
)

c1 = Comment(

)


db.session.add_all([])
db.session.commit()
