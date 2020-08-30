from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers, viewsets
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from user import views

app_name = 'user'


class DefaultRouterWithSimpleViews(routers.DefaultRouter):
    """
    Extends functionality of DefaultRouter adding possibility
    to register simple API views, not just Viewsets.
    """

    def get_routes(self, viewset):
        """
        Checks if the viewset is an instance of ViewSet,
        otherwise assumes it's a simple view and does not run
        original `get_routes` code.
        """
        if issubclass(viewset, viewsets.ViewSetMixin):
            return super(DefaultRouterWithSimpleViews, self).get_routes(viewset)

        return []

    def get_urls(self):
        """
        Append non-viewset views to the urls
        generated by the original `get_urls` method.
        """    
        # URLs for simple views
        ret = []
        for prefix, viewset, basename in self.registry:

            # Skip viewsets
            if issubclass(viewset, viewsets.ViewSetMixin):
                continue

            # URL regex
            regex = '{prefix}{trailing_slash}$'.format(
                prefix=prefix,
                trailing_slash=self.trailing_slash
            )

            # The view name has to have suffix "-list" due to specifics
            # of the DefaultRouter implementation.
            ret.append(url(
                regex, viewset.as_view(),
                name='{0}-list'.format(basename)
            ))

        # Format suffixes
        ret = format_suffix_patterns(ret, allowed=['json', 'html'])

        # Prepend URLs for viewsets and return
        return super(DefaultRouterWithSimpleViews, self).get_urls() + ret


router = DefaultRouterWithSimpleViews()
router.register('users', views.UserViewSet, 'users')
router.register('create', views.CreateUserView, 'create')
router.register('token', views.CreateTokenView, 'token')
router.register('google_token', views.GoogleLogin, 'google_token')
router.register('me', views.ManageUserView, 'me')

urlpatterns = router.urls
