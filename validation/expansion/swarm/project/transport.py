from service import archive_account

def handle_archive(authenticated_session, account_id, query):
    return archive_account(authenticated_session.actor_id, account_id, query.get("tenant"))
