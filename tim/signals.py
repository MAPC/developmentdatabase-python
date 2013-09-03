# from mailers import send_new_pending_edit, send_new_published_edit, send_edit_completed

def notify_municipal_user(sender, **kwargs):

    print(kwargs)

    # if kwargs['instance']:
    #     moderated_project = kwargs['instance']
    #     user = moderated_project.edited_by

    #     # TODO: Write User#is_municipal and User#is_trusted helpers
    #     # Then refactor this EVERYWHERE.
    #     if user.profile.is_trusted or user.profile.is_municipal
    #         send_new_pending_edit()
    #     else:
    #         send_new_published_edit()

