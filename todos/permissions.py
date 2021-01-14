from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # if request.method in permissions.SAFE_METHODS:
        #     return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user

class IsTodoListOwner(permissions.BasePermission):

    def has_permission(self, request, view, **kwargs):
        list_pk = view.kwargs['list_pk']
        queryset = view.get_queryset()

        todo_list = queryset.get(pk=list_pk)

        return view.request.user == todo_list.owner    