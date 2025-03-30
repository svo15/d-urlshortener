from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken ,AccessToken
from .models import urls
import jwt

from .serializers import userSerializer ,urlsSerializer
from django.conf import settings
# Create your views here.

def set_token_to_cookie(response, request,refresh,access_token):
    response.set_cookie('refresh_token', str(refresh), httponly=True, secure=True, samesite='Lax' ,max_age=600 )

    response.set_cookie('access_token', str(access_token), httponly=True, secure=True, samesite='Lax',max_age=300)

class RegisterView(APIView):
    permission_classes=[AllowAny]

    def post(self ,request):
        serializer=userSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response=Response()
            user=authenticate(username=request.data['username'],password=request.data['password'])

            refresh=RefreshToken.for_user(user)
            access_token=refresh.access_token
            set_token_to_cookie(response,request,refresh,access_token)
            serializer=userSerializer(user)
            response.data=serializer.data
            return response
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes=[AllowAny]

    def post(self,request):
        user=authenticate(username=request.data['username'],password=request.data['password'])

        if user is not None:
            response=Response()
            refresh=RefreshToken.for_user(user)
            access_token=refresh.access_token
            set_token_to_cookie(response,request,refresh,access_token)
            serializer=userSerializer(user)
            response.data=serializer.data
            return response
        return Response({"Invalid" : "Invalid username or password!!"}, status=status.HTTP_404_NOT_FOUND)
    
class Logout(APIView):
    permission_classes=[AllowAny]

    def get(self,request):
        response=Response()

        response.set_cookie('refresh_token', httponly=True, secure=True, samesite='Lax' ,max_age=0)
        response.set_cookie('access_token', httponly=True, secure=True, samesite='Lax',max_age=0)

        return response

class GetUserData(APIView):
    permission_classes=[AllowAny]

    def get(self,request):
        refresh_token=request.COOKIES.get('refresh_token')
        

        if refresh_token is None:
            return Response({'detail': 'Refresh token is missing!'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            refresh_token_bytes = refresh_token.encode('utf-8') 
            refresh=RefreshToken(refresh_token_bytes)
            access_token=refresh.access_token
            response=Response()
            response.set_cookie('access_token', str(access_token), httponly=True, secure=True, samesite='Lax',max_age=300)
            dam=str(access_token)
            obj=jwt.decode(dam,settings.SECRET_KEY,algorithms=["HS256"])


            user=User.objects.get(id=obj['user_id'])
            serializer=userSerializer(user)
            
            response.data={'user':serializer.data}

            return response

        except Exception as e:
            print(e)
            return Response({'detail': 'Invalid refresh token!'}, status=status.HTTP_400_BAD_REQUEST)


  
class ShortenedUrlsCreating(APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request):
        if request.user.is_authenticated:
            serializer = urlsSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save() 
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)
        
class GetallUserurls(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
        if request.user.is_authenticated:
            urlsUser=urls.objects.filter(user=request.user)
            if urlsUser:
                serializer=urlsSerializer(urlsUser,many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response({"error":"this user not have any urls"},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error":"Authentication required"},status=status.HTTP_401_UNAUTHORIZED)
class Redirect(APIView):
    permission_classes=[AllowAny]

    def get(self,request,pk):
        url=urls.objects.get(shortened_url=pk)
        if url.original_url:
            return redirect(url.original_url)
        else:
            return Response({'error'," Don't have any url "},status=status.HTTP_404_NOT_FOUND)
