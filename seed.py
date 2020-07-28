from app import app
from models import db, connect_db, User, Issue, Comment, Role, Priority, Resolution, Status, Category

db.drop_all()
db.create_all()

# Sample users.

u1 = User(
    id=1111,
    email="user1@example.com",
    first_name="Admin",
    last_name="User",
    password="password",
    role="admin"
)

u2 = User(
    id=2222,
    email="user2@example.com",
    first_name="Regular",
    last_name="User",
    password="password"
)

u3 = User(
    id=2222,
    email="user2@example.com",
    first_name="Regular",
    last_name="User",
    password="password"
)

u4 = User(
    id=3333,
    email="user3@example.com",
    first_name="Assignee",
    last_name="User",
    password="password"
)

# Priority

p1 = Priority(
    priority_id=0,
    priority_label="Low"
)

p2 = Priority(
    priority_id=1,
    priority_label="Medium"
)

p3 = Priority(
    priority_id=2,
    priority_label="High"
)

p4 = Priority(
    priority_id=3,
    priority_label="Urgent"
)

# Status

s1 = Status(
    status_id=0,
    status_label="Submitted"
)

s2 = Status(
    status_id=1,
    status_label="Assigned"
)

s3 = Status(
    status_id=2,
    status_label="Resolved"
)

# Resolution

r1 = Resolution(
    resolution_id=0,
    resolution_label="Open"
)

r2 = Resolution(
    resolution_id=1,
    resolution_label="Resolved"
)

r3 = Resolution(
    resolution_id=2,
    resolution_label="Closed"
)

# Category

c1 = Category(
    category_id=0,
    category_label="Technical Issue"
)

c2 = Category(
    category_id=1,
    category_label="Customer Complaint"
)

c3 = Category(
    category_id=2,
    category_label="Product Request"
)

ro1 = Role(
    role_id=0,
    role_label="user"
)

ro2 = Role(
    role_id=1,
    role_label="assignee"
)

ro3 = Role(
    role_id=2,
    role_label="admin"
)

# Sample issues

# i1 = Issue(
#     title="Sample Issue 1",
#     summary="Short description of Issue 1",
#     text="Longer description text describing Issue 1.  This is a text field, so can contain much text."
# )

# i2 = Issue(
#     title="Sample Issue 2",
#     summary="Short description of Issue 2",
#     text="Longer description text describing Issue 2.  So much text can fit here, you wouldn't believe it."
# )

# i3 = Issue(
#     title="Sample Issue 3",
#     summary="Short description of Issue 2",
#     text="Longer description text describing Issue 3.  Look at all of this text!  Holy Cow!"
# )


db.session.add_all([p1,p2,p3,p4,s1,s2,s3,r1,r2,r3,c1,c2,c3])
db.session.commit()


