from app import app
from models import db, connect_db, User, Issue, Comment,  Priority, Resolution, Status, Category

db.drop_all()
db.create_all()

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

# ro1 = Role(
#     role_id=0,
#     role_label="user"
# )

# ro2 = Role(
#     role_id=1,
#     role_label="assignee"
# )

# ro3 = Role(
#     role_id=2,
#     role_label="admin"
# )


db.session.add_all([p1,p2,p3,p4,s1,s2,s3,c1,c2,c3])
db.session.commit()

# Sample users.

u1 = User.register(
    email="user1@example.com",
    first_name="Admin",
    last_name="User",
    password="password"
)

u2 = User.register(
    email="user2@example.com",
    first_name="Regular",
    last_name="User",
    password="password"
)

u3 = User.register(
    email="user3@example.com",
    first_name="Regular",
    last_name="User",
    password="password"
)

u4 = User.register(
    email="user4@example.com",
    first_name="Assignee",
    last_name="User",
    password="password"
)

u1.role = 'admin'
u4.role = 'assignee'

db.session.commit()

# Sample issues

i1 = Issue(
    title="Sample Issue 1",
    text="Longer description text describing Issue 1.  This is a text field, so can contain much text.",
    reporter=2,
    assignee=4
)

i2 = Issue(
    title="Sample Issue 2",
    text="Longer description text describing Issue 2.  So much text can fit here, you wouldn't believe it.",
    reporter=2,
    assignee=4
)

i3 = Issue(
    title="Sample Issue 3",
    text="Longer description text describing Issue 3.  Look at all of this text!  Holy Cow!",
    reporter=3,
    assignee=4
)

i4 = Issue(
    title="Sample Issue 4",
    text="Longer description text describing Issue 4.  Look at all of this text!  Holy Cow!",
    reporter=3,
    assignee=4
)

db.session.add_all([i1,i2,i3,i4])
db.session.commit()
