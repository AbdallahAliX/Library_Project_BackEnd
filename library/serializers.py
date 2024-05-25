from rest_framework import serializers
from .models import Bookitem
from .models import User
from .models import Borrowedbook
from .models import CurrentUser

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookitem
        fields = ['id', 'title', 'author', 'year', 'category', 'image']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'role', 'username', 'email', 'password']

class BorrowedbookSerializer(serializers.ModelSerializer):
    book = BookSerializer()
    class Meta:
        model = Borrowedbook
        fields = ['id', 'user', 'book']

class CurrentUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = CurrentUser
        fields = ['id', 'user']