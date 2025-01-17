async def getCredentials(form):
    email = form['email']
    password = form['password']
    confirm_password = form['confirm-password']

    return { 'email': email, 'password': password }