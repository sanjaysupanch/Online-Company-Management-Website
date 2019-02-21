from rest_framework import serializers
from blog.models import post



class postserializer(serializers.ModelSerializer):   #forms.ModelForm

    class Meta:
        model=post
        fields=[
            'title',
            'content',
            'timestamp',
            'author',
            'team_details',
            ]
        read_only_fields=['author']   # pk is by default read only mode

# What does serializer do?

#converts to JSON

#validations for data passed

    def validate_title(self,value):
        posts = post.objects.filter(title__iexact=value)

        if self.instance:
            posts=posts.exclude(pk=self.instance.pk)

        if posts.exists():

            raise serializers.ValidationError(" The title has already been used ")
