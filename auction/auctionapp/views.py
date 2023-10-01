from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .serializer import userserializer
from rest_framework import status
from .models import User
from rest_framework import viewsets
class ApiView(GenericAPIView):
    def post(self, request):
        serializer = userserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(f"Serializer errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get_object(self, id):
        try:
            return User.objects.get(pk=id)
        except User.DoesNotExist:
            return None
    def get(self, request, id=None):
        queryset=User.objects.all()
        if id is not None:
            target = self.get_object(id)
            if target is not None:
                serializer = userserializer(target)
                return Response(serializer.data)
            return Response({"detail": "Target not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            user=User.objects.all()
            serializer=userserializer(user,many=True)
            return Response(serializer.data)
    def put(self, request,id=None): 
        if id is not None:
            try:
                target = User.objects.get(pk=id)
            except User.DoesNotExist:
                return Response({"detail": "Target not found."}, status=status.HTTP_404_NOT_FOUND)
            serializer = userserializer(target, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, id=None):
            if id is not None:
                try:
                    target = User.objects.get(pk=id)
                    target.delete()  # Delete the target
                    return Response({"detail": "Target deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
                except User.DoesNotExist:
                    return Response({"detail": "Target not found."}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"detail": "Invalid request."}, status=status.HTTP_400_BAD_REQUEST)
