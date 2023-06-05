from rest_framework.permissions import BasePermission

class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj): #имеет и запрос доступ к этому обьекту
        return request.user.is_authenticated and request.user == obj.user #ЯВЛЯЕТСЯ ЛИ ПОЛЬЗОВАТЕЛЬ ВЛАДЕЛЬЦЕМ ОБЬЕКТА 
    