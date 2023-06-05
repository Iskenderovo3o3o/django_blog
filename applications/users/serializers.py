from rest_framework import serializers
from django.contrib.auth import get_user_model,authenticate
from .utils import send_activation_code,create_activation_code

User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):  
    password_confirm = serializers.CharField()
    class Meta: #мы используем тако метод так как там есть все методы которые нам нужны
        model = User 
        fields = ('username','email','password','password_confirm')
        write_only_fields = ['password']

    def validate(self,attrs:dict): #проверка совпадает ли код 
        print(attrs)
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('ПАРОЛИ НЕ СОВПАДАЮТ')
        return attrs
    
    def validate_email(self,email): # проверка на существование почты 
        if User.objects.filter(email = email).exists(): #если такая потча в базе данных существует 
            raise serializers.ValidationError('ТАКАЯ ПОЧТА СУЩЕСТВУЕТ')
        return email
    
    def create(self,validated_data): #если все проверки были пройдены успешно то attrs превращается в validated data
        user = User.objects.create_user(**validated_data)
        create_activation_code(user)
        send_activation_code(user)
        return user


class ActivationSerializer(serializers.Serializer):
    activation_code = serializers.CharField(max_length=10)

    def validate_activation_code(self,activation_code):
        if User.objects.filter(activation_code=activation_code).exists(): # существует ли такой код 
            return activation_code
        raise serializers.ValidationError('Неверно указан код') # если такого кода не сузествует поднять ошибку:
    
    def activate(self):
        code = self.validated_data.get('activation_code') #ЩДЕСЬ ХРАНЯТСЯ ДАННЫЕ КОТОРЫЕ ПРОШЛИ ПРОВЕРКИ 
        user = User.objects.get(activation_code = code)
        user.is_active = True
        user.activation_code = '' #обнуление пароля 
        user.save()

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


    def validate_usernam(self,username): #есть и такой пользователь 
        if not User.objects.filter(username=username).exists(): #если такого пользоватея нет то
            raise serializers.ValidationError('Неверно указан username')
        return username 
    
    def validate(self, attrs):
        request = self.context.get('request')
        username = attrs.get('username')
        password = attrs.get('password')
        if username and password:
            user = authenticate(username=username,password=password,request=request)        
            if not user:
                raise serializers.ValidationError('Неправильно указан логин или пароль ')
        else:
            raise serializers.ValidationError('Укажите логин и пароль')
        attrs['user'] = user 
        return attrs 