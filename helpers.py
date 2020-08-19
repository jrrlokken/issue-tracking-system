def is_assignee(current_user):
    """Is the user an assignee?"""

    if user.role == 'assignee':
        return True

    return False

def is_admin(current_user):
    """Is the user an assignee?"""

    if user.role == 'admin':
        return True

    return False