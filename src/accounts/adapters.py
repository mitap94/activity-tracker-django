from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from django.contrib.auth import get_user_model


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    """Social account adapter used to populate the new user instance with more data.
    Create a name field from first and last name."""
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)

        user.name = f'{data.get("first_name")} {data.get("last_name")}'

        return user