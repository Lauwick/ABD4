
from vdm.serializers import ReservationSerializer
from vdm.models import Reservation
from braces.views import CsrfExemptMixin
from rest_framework.generics import CreateAPIView
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status

@csrf_exempt
@api_view(['POST'])
def ReservationView(request, version):
    """
    Insert reservation in DB.
    """
    if request.method == 'POST':
        serializer = ReservationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print('--- Everything worked just fine ---')
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
