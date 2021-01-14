from django.urls import path
from .views import ApiOverview, TodoLists, TodoListDetail, Todos, TodoDetail, UserList, UserDetail, UserRegister

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', ApiOverview.as_view()),
    path('todolists/', TodoLists.as_view(), name='todoListsView'),
    path('todolists/<int:pk>/', TodoListDetail.as_view(), name='todoListDetail'),
    path('todolists/<int:list_pk>/todos/', Todos.as_view(), name='todoView'),
    path('todolists/<int:list_pk>/todos/<int:pk>/', TodoDetail.as_view()),
    path('users/', UserList.as_view(), name='userListView'),
    path('users/<int:pk>/', UserDetail.as_view()),
    path('users/register/', UserRegister.as_view(), name='registerUser'),
    
    path('token/', TokenObtainPairView.as_view(), name='loginUser'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]