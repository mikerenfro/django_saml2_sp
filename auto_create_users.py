from django.contrib.auth.models import User  # pyright: ignore reportMissingModuleSource
def run():
    usernames = [u.get_username() for u in User.objects.all()]
    if 'superuser' not in usernames:
        # Create superuser
        user = User.objects.create_superuser(username='superuser',
                                            email='superuser@vagrant.vagrant',
                                            password='superuser')
    if 'user' not in usernames:
        # Create normal user
        user = User.objects.create_user(username='user',
                                        email='user@vagrant.vagrant',
                                        password='user')
