from django.db import models

# Create your models here.
class TodoList(models.Model):
    title = models.CharField(max_length=250)
    owner = models.ForeignKey('auth.User', related_name='todoLists', on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Todo(models.Model):
    todoList = models.ForeignKey(TodoList, related_name='todos', on_delete=models.CASCADE)
    owner = models.ForeignKey('auth.User', related_name='todoOwner', on_delete=models.CASCADE)
    todo = models.CharField(max_length=200)
    checked = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.todo

