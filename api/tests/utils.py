def delete_user(session, user):
    session.delete(user)
    session.commit()