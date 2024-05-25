from django.http import JsonResponse
from .models import Bookitem
from .models import User
from .serializers import BookSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from .models import Borrowedbook
from .serializers import BorrowedbookSerializer
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import check_password
from .serializers import CurrentUserSerializer
from .models import CurrentUser



@api_view(['GET', 'POST', 'PUT'])
def book_list(request):
    if request.method == 'GET':
        books = Bookitem.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        book_id = request.data.get('book_id')
        if not book_id:
            return Response({'error': 'book_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        book = Bookitem.objects.get(pk=book_id)
        serializer = BookSerializer(book, data=request.data, partial=True)  # partial=True allows partial updates
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET','PUT','DELETE'])
def book_detail(request, id):

    try:
        book = Bookitem.objects.get(pk=id)
    except Bookitem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = BookSerializer(book)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = BookSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET','POST'])
def user_list(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'DELETE'])
def borrowedbook_list(request):
    if request.method == 'GET':
        user_id = request.query_params.get('user_id')
        if user_id is None:
            return Response({'error': 'User ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        borrowedbooks = Borrowedbook.objects.filter(user=user)
        serializer = BorrowedbookSerializer(borrowedbooks, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        user_id = request.data.get('user_id')
        book_id = request.data.get('book_id')

        # Validate user_id and book_id
        if not user_id or not book_id:
            return Response({'error': 'user_id and book_id are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(pk=user_id)
            book = Bookitem.objects.get(pk=book_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Bookitem.DoesNotExist:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user has already borrowed the book
        if Borrowedbook.objects.filter(user=user, book=book).exists():
            return Response({'error': 'User has already borrowed this book'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new borrowed book entry
        borrowed_book = Borrowedbook.objects.create(user=user, book=book)
        serializer = BorrowedbookSerializer(borrowed_book)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    elif request.method == 'DELETE':
        user_id = request.query_params.get('user_id')
        book_id = request.query_params.get('book_id')

        if not user_id or not book_id:
            return Response({'error': 'user_id and book_id are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(pk=user_id)
            book = Bookitem.objects.get(pk=book_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Bookitem.DoesNotExist:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            borrowed_book = Borrowedbook.objects.get(user=user, book=book)
        except Borrowedbook.DoesNotExist:
            return Response({'error': 'Borrowed book not found'}, status=status.HTTP_404_NOT_FOUND)

        borrowed_book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def current_user(request):
    if request.method == 'GET':
        # Handle get current user data
        try:
            current_user_instance = CurrentUser.objects.select_related('user').get()
            serializer = CurrentUserSerializer(current_user_instance)
            return Response(serializer.data)
        except CurrentUser.DoesNotExist:
            return Response({'error': 'No user logged in'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        action = request.data.get('action')
        email = request.data.get('email')
        password = request.data.get('password')

        if action == 'login':
            # Handle login
            try:
                user = User.objects.get(email=email)
                if user.password != password:
                    raise User.DoesNotExist
            except User.DoesNotExist:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

            CurrentUser.objects.all().delete()  # Clear existing current user
            current_user = CurrentUser.objects.create(user=user)
            serializer = CurrentUserSerializer(current_user)
            return Response(serializer.data)

        elif action == 'signup':
            # Handle signup
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                CurrentUser.objects.all().delete()  # Clear existing current user
                current_user = CurrentUser.objects.create(user=user)
                current_user_serializer = CurrentUserSerializer(current_user)
                return Response(current_user_serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        # Handle update user data
        try:
            current_user_instance = CurrentUser.objects.select_related('user').get()
            user = current_user_instance.user
        except CurrentUser.DoesNotExist:
            return Response({'error': 'No user logged in'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # Handle logout and delete profile
        try:
            current_user_instance = CurrentUser.objects.select_related('user').get()
            user = current_user_instance.user
            action = request.data.get('action')

            if action == 'logout':
                current_user_instance.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            elif action == 'delete_profile':
                user.delete()
                current_user_instance.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            
            return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)

        except CurrentUser.DoesNotExist:
            return Response({'error': 'No user logged in'}, status=status.HTTP_400_BAD_REQUEST)