def is_assignee(current_user):
    """Is the user an assignee?"""

    if current_user.role == 'assignee':
        return True

    return False

def is_admin(current_user):
    """Is the user an admin?"""

    if current_user.role == 'admin':
        return True

    return False