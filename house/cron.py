from django.core.management import call_command

def update_review_cnt():
    call_command('update_review_cnt', verbosity=0, interactive=False)
    return

def update_yelpId():
    call_command('update_yelpId', verbosity=0, interactive=False)
    return
