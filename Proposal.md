## ITS - Issue Tracking System

I will build an Issue Tracking System (ITS) for technical and customer issue tracking. The ITS will provide basic CRUD functionality to allow submission, listing, updating and deleting a users’ own issues. Authorization will vary with user role.

The user interface will allow for sorting the issue list by column header.
Added functionality could be a searchable knowledge base of help articles.

The ITS will be used by employees of a co-operative grocery retailer.

The application backend will provide a RESTful JSON API to serve issue and user information to the frontend app.

There is no sensitive data involved, however, proper authentication and authorization will be implemented, allowing users to edit/delete only issues they have created.

I _may_ use the Twilio API for sending notification email.

---

Database schema is primarily users, issues, comments. The submitting user and assigned user are foreign keys to the users table. One user can be associated with many issues, one issues can be associated with many comments, one user can be associated with many comments.

https://dbdiagram.io/d/5ee914719ea313663b3aa4e9

- Ref: roles.role_id < users.role

- Ref: issues.priority > priority.priority_code
- Ref: issues.status > status.status_code

- Ref: issues.assignee > users.user_id
- Ref: issues.reporter > users.user_id

- Ref: comments.comment_user > users.user_id
- Ref: comments.comment_issue > issues.issue_id

---

### General functionality:

- User registration, login, logout, edit or delete account.
- Create issue, default status “Submitted”, default priority “Medium”
- Read issue, user can views issues on login, sortable by display column
- Update issue, the original body of the issue will be editable, however, new information will be added to issues via comments. Users will be able to change ticket status to “Closed”, in order to facilitate some level of user control over their own tickets.
- Delete issue

User roles:

- Admin: user management, issue management
- Resolver: users who can have issues assigned to them
- Normal user: CRUD for their own issues
