from django.urls import path
from .views import login_view, logout_view, SignUpView

app_name = 'login'

urlpatterns = [
    path('', login_view, name="login_view"),
    path('logout/', logout_view, name="logout_view"),
    path('signup/', SignUpView.as_view(), name="signup_view"),
]