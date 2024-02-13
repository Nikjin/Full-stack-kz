# api/view.py
from django.shortcuts import render
from rest_framework.views import APIView
from .models import Item
from .serializers import ItemSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from django.views import View
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.db.models import Q
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)


class UserRegistrationView(APIView):
    authentication_classes = []  # Exempt from CSRF protection
    permission_classes = [AllowAny]

    def get(self, request):
        # Render the registration form
        return render(request, 'registration.html')

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not username or not email or not password:
            return Response({'message': 'Username, email, and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if username or email is already in use
        if User.objects.filter(username=username).exists():
            return Response({'username': ['Username is already in use']}, status=status.HTTP_409_CONFLICT)
        elif User.objects.filter(email=email).exists():
            return Response({'email': ['Email is already in use']}, status=status.HTTP_409_CONFLICT)

        # Create new user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        # Redirect to the login page after successful registration
        return redirect('login')


class LoginView(APIView):
    authentication_classes = []  # Exempt from CSRF protection
    permission_classes = [AllowAny]

    template_name = 'login.html'
    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('item-dashboard')
            # return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, self.template_name)


class ItemDashboardView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        items = Item.objects.all()
        return render(request, 'item_dashboard.html', {'items': items})

    def post(self, request):
        logger.debug(f"Request Data: {request.data}")  # Log the request data
        serializer = ItemSerializer(data=request.data)  # Use request.data instead of request.POST
        # print("Request Data:", request.data)  # Debug print statement
        if serializer.is_valid():
            # print("Serializer is valid. Saving...")  # Debug print statement
            logger.debug(f"Processed Tags Data: {serializer.validated_data.get('tags')}")

            serializer.save()
            # print("Item saved successfully.")  # Debug print statement
            return redirect('item-dashboard')  # Redirect back to item dashboard after creating the item
        else:
            # print("Serializer errors:", serializer.errors)  # Debug print statement
            # If the form is invalid, render the item dashboard template with error messages
            items = Item.objects.all()
            return render(request, 'item_dashboard.html', {'items': items, 'errors': serializer.errors})
    def delete(self, request, sku):
        try:
            item = Item.objects.filter(SKU=sku).first()
            if item:
                item.delete()  # Delete the item
                return JsonResponse({'message': 'Item deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return JsonResponse({'error': 'Item not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({'error': 'Failed to delete item.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ItemListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        queryset = Item.objects.all()
        search_query = request.query_params.get('search', '')
        category = request.query_params.get('category', '')
        tag = request.query_params.get('tag', '')
        stock_status = request.query_params.get('stock_status', '')
        sort_by = request.query_params.get('sort', 'name')

        if search_query:
            queryset = queryset.filter(Q(name__icontains=search_query) | Q(SKU__icontains=search_query))
        if category:
            queryset = queryset.filter(category__name=category)
        if tag:
            queryset = queryset.filter(tags__name=tag)
        if stock_status:
            queryset = queryset.filter(stock_status=stock_status)

        queryset = queryset.order_by(sort_by)

        serializer = ItemSerializer(queryset, many=True)
        return Response(serializer.data)
