from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .models import Article, Tag, Comment, Like
from .serializers import ArticleSerializer, ArticleListSerializer, TagSerializer, CommentSerializer, RatingSerializer, LikeSerializer
from .permissions import IsAuthor


""" 
@api_view - вьюшки на функциях
rest_framework.views.APIView - вьюшки на классах без функционала

rest_framework.generic - вьюшки на готовых класах

rest_framework - класс для обработки всех операций CRUD
"""

class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = [filters.SearchFilter,DjangoFilterBackend]
    filtered_fields = ['tag','status']
    search_fields = ['title','tag__title']
    # permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request':self.request})
        return context

    def get_permissions(self):
        if self.request.method == 'POST': # если пользователь хочет сделать одно из эти действий то у него бкдет проверяться токен
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['PUT','PATCH','DELETE']:
            self.permission_classes = [IsAuthor] #обновлять и удалять может тольок автор 
        return super().get_permissions()
    
    def get_serializer_class(self):
        if self.action == 'comment':
            return CommentSerializer
        return super().get_serializer_class()
    
    @action(methods=['POST','DELETE'],detail=True) #DETAIL TRUE ЗАПРАШИВАЕТ ID
    def comment(self,request,pk=None):
        article = self.get_object()# по pk получает статью к которой обращается 
        # Article.objects.get(pk=pk)
        if self.request.method == 'POST':
            serializer = CommentSerializer(data=request.data,context = {'request': request})
            serializer.is_valid(raise_exception=True)#правильные ли все входные данные
            serializer.save(user=request.user,article=article)
            return Response(serializer.data)
        # return Response{'TODO':'ДОБАВИТЬ УДАЛЕНИЕ КОМЕНТА'}

     
    @action(methods=['POST'], detail=True, url_path='rate')
    def rate_article(self, request, pk=None) -> Response:
        article = self.get_object()
        serializer = RatingSerializer(data=request.data, context={'request': request, 'article': article})
        serializer.is_valid(raise_exception=True)
        serializer.save(article=article)
        return Response(serializer.data)
    
    @action(methods = {'POST'},detail = True)
    def Like(self,request,pk=None):
        article = self.get_object()# получаем статью 
        like =  Like.objects.filter(user = request.user,article = article)
        if Like.exist():
            like.delete() #если существует то удали его 
            return Response({'Liked':False}) 
        else:
            Like.objects.create(user = request.user,article=article).save()
            return Response({'Liked':True})  
    

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated] #передан ли токен 
        elif self.action in ['update','destroy']:
            self.permission_classes = [IsAuthor]  # автор ли он коментария 
        return super().get_permissions()
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context



""" 
actions - действия пользователя
list
retrieve - получение одного обьекта 
create
update
delete


"""


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    # pagination_class = 

#TODO: ПЕРЕКЛЮЧАТЬ МЕТОД get_permission_classes в TagViewSet,так чтобы только залогиненные пользователи могли создавать тэги
#TODO: наполнить сайт контентом 