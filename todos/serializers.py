from django.contrib.auth.models import User
from rest_framework import serializers
from .models import TodoList, Todo

from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator

class TodoListSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = TodoList
        fields = [
            'id',
            'title',
            'owner',
            'createdAt',
            'todos'
        ]

class TodoSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Todo
        fields = [
            'id',
            'todo',
            'checked',
            'createdAt',
            'todoList',
            'owner',
        ]

class UserSerializer(serializers.ModelSerializer):
    todoLists = serializers.PrimaryKeyRelatedField(many=True, queryset=TodoList.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'todoLists']


class UserRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['username', 'password']


    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username']
        )

        
        user.set_password(validated_data['password'])
        user.save()

        return user