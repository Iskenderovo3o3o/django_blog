from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token 
from .serializers import RegistrationSerializer,ActivationSerializer,LoginSerializer
from rest_framework.views import APIView

class RegistrationView(CreateAPIView):
    serializer_class = RegistrationSerializer 


    def create(self, request:Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({'message':'Спасибо за регистрацию'})
    
class ActivationView(CreateAPIView):
    serializer_class = ActivationSerializer
    def post(self, request:Request, *args, **kwargs):  
        serializer = ActivationSerializer(data = request.data)
        serializer.is_valid(raise_exception=True) # метод is valid запускает все методы в названии которых valid
        serializer.activate()
        return Response({'message':'Аккаунт успешно активирован'})
    

class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self,request:Request) -> Response:
        Token.objects.get(user=request.user).delete #мы удаляем токен юзера тем самым он выходит с сайта 
        return Response({'message':'Logged out'})
    
# TODO: ВОССТАНОВЛЕНИЕ ПАРОЛЯ
# TODO: ИЗМЕНЕНИЕ ПАРОЛЯ 