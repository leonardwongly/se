from service import export_account

def handle_export(authenticated_session, account_id):
    return export_account(authenticated_session.actor_id, account_id)
