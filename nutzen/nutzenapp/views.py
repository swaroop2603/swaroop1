from django.contrib.auth.hashers import make_password, check_password
from rest_framework import status
from .models import User
from .Serializers import userserializers
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from django.db import IntegrityError
from rest_framework.exceptions import AuthenticationFailed
import jwt,datetime
class token(GenericAPIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = User.objects.filter(email=email).first()
        if user:
            if check_password(password, user.password):
                serializer = userserializers(user)

                payload={
                    'id':serializer.data.get('user_id'),
                    'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=15),
                    'iat':datetime.datetime.utcnow()
                }
                token=jwt.encode(payload,'secret',algorithm='HS256')
                response=Response()
                response.set_cookie(key='jwt',value=token,httponly=True)
                response.data={
                    'jwt':token
                }
                return response
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            raise AuthenticationFailed('User not found')
class login(GenericAPIView):
    def get(self,request):
        token=request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('unautheticated')
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise  AuthenticationFailed('Unauthenticated')
        user=User.objects.get(user_id=payload['id'])
        serializer=userserializers(user)
        return Response(serializer.data)
class logout(GenericAPIView):
    def post(self,request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('unautheticated')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')
        user = User.objects.get(user_id=payload['id'])
        serializer = userserializers(user)
        username=serializer.data.get('username')
        response=Response()
        response.delete_cookie('jwt')
        response.data={
            'message':f'{username} logged out successfully'
        }
        return response
class Signup(GenericAPIView):
    def post(self, request):
        serilizer = userserializers(data=request.data)
        if serilizer.is_valid():
            email = request.data.get("email")
            password = request.data.get("password")
            username = request.data.get('username')
            hash_password = make_password(password)
            try:
                user = User.objects.create(email=email, password=hash_password, username=username)
            except IntegrityError:

                return Response({"error": "User with this email already exists."},status=status.HTTP_400_BAD_REQUEST)

            serializer= userserializers(user)

            return Response({"message":"sigin successful"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serilizer.errors, status=status.HTTP_400_BAD_REQUEST)
class updateemail(GenericAPIView):
    def put(self,request):
        email = request.data.get('email')
        password = request.data.get('password')
        username = request.data.get('username')
        user = User.objects.filter(email=email).first()
        if user:
            if check_password(password, user.password):
                new_email=request.data.get('new_email')
                user.email=new_email
                user.save()
                serializer=userserializers(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
class updateepassword(GenericAPIView):
    def put(self,request):
        email = request.data.get('email')
        password = request.data.get('password')
        username = request.data.get('username')
        user = User.objects.filter(email=email).first()
        if user:
            if check_password(password, user.password):
                new_password=request.data.get('new_password')
                user.password=make_password(new_password)
                user.save()
                serializer=userserializers(user)
                return Response("password updated sucessfully", status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
