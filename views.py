from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from .models import TextData
from .serializers import TextDataSerializer
import os
import random
import string
from PIL import Image, ImageDraw, ImageFont
from cryptography.fernet import Fernet
import os
import random
import string
from PIL import Image, ImageDraw, ImageFont
from cryptography.fernet import Fernet
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


SECRET_KEY = b'FCLKZFCzV7p3i42jJIjEvFxqhem9pJJZgBdYrny17a8='
cipher = Fernet(SECRET_KEY)

def hello_world(request):
    return JsonResponse({"message": "Hello, API!"})

class TextDataView(APIView):

    def get(self, request):
        texts = TextData.objects.all()
        serializer = TextDataSerializer(texts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TextDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class GenerateCaptchaView(View):
    def post(self, request):
        # Get parameters from the POST request or set defaults
        text_length = int(request.POST.get("text_length", 5))
        width = int(request.POST.get("width", 200))
        height = int(request.POST.get("height", 70))
        font_size = int(request.POST.get("font_size", 40))

        # Generate random text
        text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=text_length))

        # Create an image with white background
        image = Image.new('RGB', (width, height), 'white')
        draw = ImageDraw.Draw(image)

        # Load a font
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()

        # Calculate text size
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
        text_x = (width - text_width) // 2
        text_y = (height - text_height) // 2

        # Draw the text
        draw.text((text_x, text_y), text, font=font, fill='black')

        # Add noise (lines and dots)
        for _ in range(10):
            x1 = random.randint(0, width)
            y1 = random.randint(0, height)
            x2 = random.randint(0, width)
            y2 = random.randint(0, height)
            draw.line(((x1, y1), (x2, y2)), fill="orange", width=1)

        for _ in range(100):
            x = random.randint(0, width)
            y = random.randint(0, height)
            draw.point((x, y), fill="orange")

        # Ensure the directory exists
        output_dir = "captchas"
        os.makedirs(output_dir, exist_ok=True)

        # Count existing files in the directory to determine the next file name
        existing_files = os.listdir(output_dir)
        next_file_number = len(existing_files) + 1
        file_name = f"{next_file_number}.png"
        file_path = os.path.join(output_dir, file_name)

        # Save the image
        image.save(file_path)

        # Encrypt the text
        encrypted_text = cipher.encrypt(text.encode()).decode()

        # Return JSON response
        return JsonResponse({"image_path": file_path, "encrypted_text": encrypted_text})


@method_decorator(csrf_exempt, name='dispatch')
class ValidateCaptchaView(View):
    def post(self, request):
        # Get parameters from the POST request
        encrypted_text = request.POST.get("encrypted_text")
        user_input = request.POST.get("user_input")

        if not encrypted_text or not user_input:
            return JsonResponse({"status": "fail", "message": "Both encrypted_text and user_input are required"}, status=400)

        try:
            # Decrypt the text
            decrypted_text = cipher.decrypt(encrypted_text.encode()).decode()

            # Compare the decrypted text with user input
            if decrypted_text == user_input:
                return JsonResponse({"status": "success", "message": "Validation successful"})
            else:
                return JsonResponse({"status": "fail", "message": "Validation failed"})
        except Exception as e:
            # Handle decryption errors
            return JsonResponse({"status": "fail", "message": "Invalid encrypted_text or decryption failed", "error": str(e)}, status=400)
