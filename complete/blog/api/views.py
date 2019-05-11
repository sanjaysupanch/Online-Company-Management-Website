# import django generic views


from  rest_framework import generics
from blog.models import post

from .serializers import postserializer


class BlogPostRudView(generics.RetrieveUpdateDestroyAPIView): #DetailVoew

    pass

    lookup_field =   'pk'   #id   <int:pk>

    serializer_class = postserializer
    #queryset    = BlogPost.objects.all()

    def  get_queryset(self):
        return  post.objects.all()

    # def get_object(self):
    #     pk = self.kwargs.get("pk")
    #     return  post.objects.get(pk=pk)
