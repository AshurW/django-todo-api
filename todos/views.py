from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from rest_framework import generics, viewsets, permissions, status, exceptions
from rest_framework.response import Response
from .models import TodoList, Todo
from rest_framework.permissions import AllowAny
from .permissions import IsOwner, IsTodoListOwner
from .serializers import TodoListSerializer, TodoSerializer, UserSerializer, UserRegisterSerializer

# Create your views here.
class ApiOverview(generics.ListAPIView):
    def list(self, request, *args, **kwargs):
        api_urls = {
            'todolists/',
            'todolists/<int:pk>/',
            'todolists/<int:list_pk>/todos/',
            'todolists/<int:list_pk>/todos/<int:pk>/',
            'users/',
            'users/<int:pk>/',
        }
        return Response(api_urls)

class TodoLists(generics.ListCreateAPIView):
    queryset = TodoList.objects.all()
    serializer_class = TodoListSerializer
    permission_classes = [IsOwner]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(owner=request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class TodoListDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TodoList.objects.all()
    serializer_class = TodoListSerializer
    permission_classes = [IsOwner]

class Todos(generics.ListCreateAPIView):
    queryset= TodoList.objects.all()
    serializer_class = TodoSerializer
    lookup_url_kwarg = 'list_pk'
    permission_classes = [IsTodoListOwner]

    def list(self, request, *args, **kwargs):
        list_pk = kwargs['list_pk']
        queryset = Todo.objects.filter(todoList=list_pk, owner=request.user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        newTodo = request.data.copy()
        newTodo['todoList'] = kwargs['list_pk']
        tempTodoList = TodoList.objects.get(pk=kwargs['list_pk'])
        if self.request.user != tempTodoList.owner:
            raise exceptions.PermissionDenied(detail='You cant do that')
        serializer = self.get_serializer(data=newTodo)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    

class TodoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = []
    serializer_class = TodoSerializer
    permission_classes = [IsOwner]

    def retrieve(self, request, *args, **kwargs):
        list_pk = kwargs['list_pk']
        pk = kwargs['pk']
        todo = Todo.objects.get(id=pk, todoList=list_pk)
        serializer = self.get_serializer(todo, many=False)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        list_pk = kwargs['list_pk']
        pk = kwargs['pk']
        instance = Todo.objects.get(id=pk, todoList=list_pk)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        list_pk = kwargs['list_pk']
        pk = kwargs['pk']
        instance = Todo.objects.get(id=pk, todoList=list_pk)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserRegister(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]