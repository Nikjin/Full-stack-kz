from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Item  # Import your Item model
from .serializers import ItemSerializer  # Import your ItemSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny  # Import AllowAny permission


class UserRegistrationView(APIView):
    authentication_classes = []  # Exempt from CSRF protection
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not username or not email or not password:
            return Response({'message': 'Username, email, and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if username or email is already in use
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            return Response({'message': 'Username or email is already in use'}, status=status.HTTP_409_CONFLICT)

        # Create new user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    authentication_classes = []  # Exempt from CSRF protection
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)



class ItemDashboardView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ItemListView(APIView):
    def get(self, request):
        # Retrieve query parameters for search, filtering, and sorting
        search_query = request.query_params.get('search')
        category = request.query_params.get('category')
        sort_by = request.query_params.get('sort_by')

        # Filter queryset based on search query and category
        queryset = Item.objects.all()
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        if category:
            queryset = queryset.filter(category=category)

        # Sort queryset based on sort_by parameter
        if sort_by:
            queryset = queryset.order_by(sort_by)

        # Serialize queryset and return response
        serializer = ItemSerializer(queryset, many=True)
        return Response(serializer.data)


# Create your views here.
