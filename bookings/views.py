from django.shortcuts import render
from .models import ClassList,Client
from .serializers import ClassListSerializer,BookingSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger('booking')


class ClassListView(APIView):
    def get(self,request):
        classes = ClassList.objects.all()
        logger.info(f"{len(classes)} classes fetched.")
        serializer = ClassListSerializer(classes,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


class BookingView(APIView):
    def post(self, request):

        # Serializer validation
        serializer = BookingSerializer(data=request.data)
        if not serializer.is_valid():
            logger.error(f"Booking failed: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        class_id = data['class_id']
        client_name = data['client_name']
        client_email = data['client_email']

        if not (class_id and client_name and client_email):
            logger.warning(f"Booking Failed: Missing fields in booking request - {request.data}")
            return Response({"error":"class_id or client_name or client_email is missing"},status=status.HTTP_400_BAD_REQUEST)
        
        try:
            fitness_class = ClassList.objects.get(id=class_id)
        except ClassList.DoesNotExist:
            logger.error(f"Booking Failed: Fitness class with ID: {class_id} is not found.")
            return Response({"error":f"Fitness class with ID: {class_id} is not found. Please check /classes ."},status=status.HTTP_404_NOT_FOUND)
        
        if fitness_class.available_slots <= 0:
            logger.warning(f"Booking Failed: Overbooking attempt for class ID {class_id}.")
            return Response({"error":"Booking failed due to overbooking. No available slots left for this class."},status=status.HTTP_400_BAD_REQUEST)
        
        client,created = Client.objects.get_or_create(email=client_email,defaults={'client':client_name})
        
        if not created and client.client != client_name:
            logger.warning(f"Booking Failed: Client name does not match.")
            return Response({"error": "Client name does not match the existing record"}, status=status.HTTP_400_BAD_REQUEST)
        
        if fitness_class in client.enrolled_classes.all():
            logger.warning(f"Booking Failed: Client is already enrolled in this class.")
            return Response({"error": "Client is already enrolled in this class"},status=status.HTTP_400_BAD_REQUEST)
        
        client.enrolled_classes.add(fitness_class)
        fitness_class.available_slots -= 1
        fitness_class.save()
        logger.info(f"Booking successful for {client_email} in class {fitness_class.class_name}")

        return Response({
            "message":"Booking successfull !!",
            "class_id":fitness_class.id,
            "client_name":client.client,
            "client_email":client.email,
            "available_slots":fitness_class.available_slots
        })
        
class ClientView(APIView):

    def get(self,request):
        client_email = request.query_params.get("email")
        if not client_email:
            logger.error("Bookings List: Email is missing")
            return Response({"error": "Email is required."},status=status.HTTP_400_BAD_REQUEST)
        try:
            client = Client.objects.get(email=client_email)
        except Client.DoesNotExist:
            logger.warning(f"No client found with email: {client_email}")
            return Response({"error": f"No client found with email: {client_email}"},status=status.HTTP_404_NOT_FOUND)

        classes = client.enrolled_classes.all()
        logger.info(f"Client {client_email} fetched {len(classes)} enrolled classes.")
        serializer = ClassListSerializer(classes,many=True)

        return Response(serializer.data,status=status.HTTP_200_OK)