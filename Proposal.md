## ITS - Issue Tracking System

I will build an Issue Tracking System (ITS) for technical and customer issue tracking. The ITS will provide basic CRUD functionality to allow submission, listing, updating and deleting issues. Authorization will vary with user role.

The user interface will allow for sorting the issue list by column header.
Added functionality could be a searchable knowledge base of help articles.

The ITS will be used by employees of a co-operative grocery retailer.

The application backend will provide a RESTful JSON API to serve issue and user information to the frontend app.

There is no sensitive data involved, however, proper authentication and authorization will be implemented, allowing users to edit/delete only issues they have created.

---

Database schema is primarily users, issues, comments. The submitting user and assigned user are foreign keys to the users table. One user can be associated with many issues, one issues can be associated with many comments, one user can be associated with many comments.

https://dbdiagram.io/d/5ee914719ea313663b3aa4e9

---

### General functionality:

- Regular user registration, login, logout, edit account.
- Create issue, default status “Submitted”, default priority “Medium”
- Read issue, user can views issues on login, sortable by display column
- Update issue, the original body of the issue will be editable, however, new information will be added to issues via comments. 
- Regular users will be unable to change ticket status or delete any issues.


- Assignee role will be able to view and update any issues assigned to them.
- Assignee role can also submit new issues.


- Admin role will have full CRUD authorization for users and issues.