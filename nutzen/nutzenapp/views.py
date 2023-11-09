from django.contrib.auth.hashers import make_password, check_password
from rest_framework import status
from .models import User,Offer
from .Serializers import userserializers,offer_serializers
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from django.db import IntegrityError
from rest_framework.exceptions import AuthenticationFailed
import jwt,datetime
from datetime import datetime
from dateutil import parser as date_parser
from rest_framework import serializers


from .pagination import CustomPagination


class login(GenericAPIView):
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

class offer_details(GenericAPIView):
    pagination_class = CustomPagination
    def post(self,request):
        offer_type=request.data.get('offer_type')

        amount=request.data.get('amount')
        start_date_str=request.data.get('start_date')
        end_date_str=request.data.get('end_date')
        description=request.data.get('description','')
        user_id=request.data.get('user_id')
        try:
            start_date = date_parser.parse(start_date_str)

        except ValueError:
            start_date=None

        try:
            end_date = date_parser.parse(end_date_str)
        except ValueError:
            end_date=None


        user_obj=User.objects.get(user_id=user_id)
        overlapping_offers = Offer.objects.filter(
            user_id=user_obj,
            start_date__lte=end_date,
            end_date__gte=start_date
        )

        if overlapping_offers.exists():
            raise serializers.ValidationError("Offer overlaps with existing offers.")

        obj=Offer(

            user_id=user_obj,
            offer_type=offer_type,
            amount=amount,
            start_date=start_date,
            end_date=end_date,
            description=description
        )
        obj.save()
        serilizer=offer_serializers(obj)
        return Response(serilizer.data,status=status.HTTP_201_CREATED)

    def get(self,request):
        user_id=request.query_params.get('user_id')
        offer_type=request.query_params.get('offer_type')
        amount=request.query_params.get('amount')
        start_date_str=request.query_params.get('start_date')
        end_date_str=request.query_params.get('end_date')

        queryset=Offer.objects.all()
        if user_id:
            queryset = queryset.filter(user_id=user_id)

        if offer_type:
            queryset = queryset.filter(offer_type=offer_type)

        if amount:
            queryset = queryset.filter(amount=amount)
        if start_date_str and end_date_str:
            start_date = date_parser.parse(start_date_str)
            end_date = date_parser.parse(end_date_str)
            queryset = queryset.filter(start_date__range=[start_date, end_date])

        page = self.paginate_queryset(queryset)
        serializer = offer_serializers(page, many=True)
        offer_details_list = serializer.data

        return Response(offer_details_list)


    def put(self,request):
        offer_id=request.data.get('offer_id')


        try:
            target = Offer.objects.get(offer_id=offer_id)
        except Offer.DoesNotExist:
            return Response({"detail": " not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = offer_serializers(target, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request):
        offer_id = request.query_params.get('offer_id')
        try:
            target = Offer.objects.get(offer_id=offer_id)
            target.delete()

            return Response({'message': 'offer deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Offer.DoesNotExist:
            return Response({"detail": " not found."}, status=status.HTTP_404_NOT_FOUND)



        Re


