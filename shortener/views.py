from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import Http404
from django.shortcuts import redirect

from .serializers import urlserializer
from .models import short_url
# Create your views here.
@api_view(['POST'])
def posturls(request):
    url=request.data.get("original")
    serializer=urlserializer(data={"original":url})
    
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)
@api_view(["GET"])
def getall(request):
    urls=short_url.objects.all()
    serializer=urlserializer(urls,many=True)
    return Response(serializer.data)
@api_view(["GET"])
def Urlredirect(request,shorted):
    try:
        # Attempt to retrieve the URL by the shortened version
        url = short_url.objects.get(short=shorted)
        return redirect(url.original)
    except short_url.DoesNotExist:
        # If the URL is not found, raise Http404
        raise Http404("URL doesn't exist")