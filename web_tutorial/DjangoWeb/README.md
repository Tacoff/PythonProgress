# account
admin/admin4zhutou

# question
## q1
    setting.py  LOGIN_REDIRECT_URL args meaning
    Here’s what LoginView does:
    If called via GET, it displays a login form that POSTs to the same URL. More on this in a bit.
    If called via POST with user submitted credentials, it tries to log the user in. If login is successful, the view redirects to the URL specified in next. If next isn’t provided, it redirects to settings.LOGIN_REDIRECT_URL (which defaults to /accounts/profile/). If login isn’t successful, it redisplays the login form.

