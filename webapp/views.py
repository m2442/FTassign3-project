from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .models import Member
from .serializers import MemberSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics    # for generic class view
from rest_framework import mixins     # for generic class view
from rest_framework.authentication import SessionAuthentication, TokenAuthentication, BasicAuthentication   # For authentication purposes. In this project only Token Authentication is being used
from rest_framework.permissions import IsAuthenticated  # For authentication

from rest_framework.views import APIView

# REST Framework Viewsets and Router has been used to serve the purpose of this project

from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
 # Uses ModelViewSet
class MemberViewSet(viewsets.ModelViewSet):
                    serializer_class = MemberSerializer
                    queryset =Member.objects.all()
                    lookup_field = 'id'
                    authentication_classes = [TokenAuthentication]
                    permission_classes = [IsAuthenticated]
                    # Fetch all the activity periods assosiated with a member
                    # Specify the method for which this action should be called.
                    @action(detail=True, methods= ['GET'])
                    def activity_periods(self, request, id=None):
                        member = self.get_object()
                        activity_periods = Activity_period.objects.filter(member=member)
                        serializer = Activity_periodSerializer(activity_periods, many=True)
                        return Response(serializer.data, status=200)
                    # Specify the method for which the action should be called.
                    @action(detail=True, methods= ['POST'])
                    def activity_period(self, request, id=None):
                        member = self.get_object()
                        data = request.data
                        data['member'] = member.id
                        serializer = Activity_periodSerializer(data=data)
                        if serializer.is_valid():
                            serializer.save()
                            return Response(serializer.data, status=201)
                        return Response(serializer.errors, status=400)
