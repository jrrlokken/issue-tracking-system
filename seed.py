from app import app
from models import db, connect_db, User, Issue, Comment, Priority, Status, Category, Role

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


db.session.add_all([p1,p2,p3,p4,s1,s2,s3,c1,c2,c3,ro1,ro2,ro3])
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
    first_name="Assignee",
    last_name="User",
    password="password"
)

u1.role = 2
u3.role = 1

db.session.commit()

# Sample issues

i1 = Issue(
    title="Printer on fire!",
    text="Huge flames are shooting out of paper tray 1!!! Please bring fire extinguisher ASAP!!!",
    reporter=2,
    assignee=3
)

i2 = Issue(
    title="Computer not responding",
    text="My PC is showing the loading spinner and will not respond to keyboard or mouse input.  It has been doing this for 6 weeks.",
    reporter=2,
    assignee=3
)

i3 = Issue(
    title="Please bring in nacho flavored Beanfields chips",
    text="We're not saying you're going to get addicted to our slamming NACHO, but we're also not going to say you won't. Nacho-lly we're biased since it is our best seller. NACHO just has unmatched taste that makes being cheesy, well, cool and vegan. The kinda vegan you want at your barbecue so you can say, 'yeah NACHO came with me. We're good like that.' Nacho average tortilla chip.",
    category=2,
    reporter=3,
    assignee=3
)

i4 = Issue(
    title="Clerk was rude and dismissive",
    text="She told me to wear a mask, and I don't wanna!",
    category=1,
    reporter=3,
    assignee=3
)

db.session.add_all([i1,i2,i3,i4])
db.session.commit()
