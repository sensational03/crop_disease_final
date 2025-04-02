from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import UploadedImage
from .forms import ImageUploadForm
from PIL import Image
import google.generativeai as genai
import os

class ImageUploadAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.save()
            img_path = uploaded_image.image.path
            
            # Process the image
            img = Image.open(img_path)
            
            # Configure Google Generative AI
            genai.configure(api_key="AIzaSyBbjN14KetOqbaK7w_BXPiFKGtaH1FKVy8")
            model = genai.GenerativeModel('gemini-2.0-flash')
            
            response = model.generate_content([
                img, 
                """Your task is to identify the crop in this image and return the following as JSON response.
                crop_name: str,
                disease_present: bool,
                disease_name: str,
                disease_description: str,
                disease_treatments: str"""
            ])
            
            return Response({
                "success": True,
                "message": "Image processed successfully",
                "data": response.text
            })
        
        return Response({"success": False, "message": "Invalid form submission"}, status=400)
