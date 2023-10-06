import mimetypes
import os
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, renderer_classes, action
from rest_framework import permissions, status
from apps.users.permissions import IsContentMaker, IsAudiobookOwner
from apps.audiobooks.models import Audiobooks, PendingAudiobooks
from apps.audiobooks.serializer import AudioBookSerializer
from apps.users.models import ContentMaker
from rest_framework.permissions import IsAuthenticated


# @api_view(['GET'])
# @permission_classes

