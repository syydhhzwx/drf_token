from django.urls import path
from rest_framework_jwt import views as view

from api import views

urlpatterns = [
    # 通过jwt完成登录并签发token  依赖于django默认的auth_user
    path("login/", view.ObtainJSONWebToken.as_view()),
    # path("login/", view.obtain_jwt_token),
    path("users/", views.UserDetailAPIVIew.as_view()),
    path("user/", views.LoginAPIView.as_view()),
]
