### HITS - Harmony Issue Tracking System

I will build an Issue Tracking System (ITS), primarily in Python.  The organization I currently work for needs an ITS for technical and customer issue tracking.  The ITS will provide basic CRUD functionality to allow submission, listing, updating and deleting a users’ own issues.
Authorization will vary with user role.

<span style="color:red">As this will be a live app, used by a client, I’m not sure that anything beyond basic CRUD is necessary/required.</span>  An idea for added functionality would be to add a searchable knowledge base of help articles.

The ITS will be used by fellow employees of a co-operative grocery retailer.

The application backend will provide a RESTful JSON API to serve ticket and user information to the frontend app.

Database schema is primarily users, issues, comments.  The submitting user and assigned user are foreign keys to the users table -- one user can be associated with many tickets, one ticket can be associated with many comments, one user can be associated with many comments, a single comment has a one-to-one relationship with users.

There is no sensitive data involved, however, proper authentication and authorization will be implemented, allowing users to edit/delete only issues they have created.  <span style="color:red">Users may be able to see tickets created by others (?)</span>


