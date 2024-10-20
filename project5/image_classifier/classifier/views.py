import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import numpy as np

model = MobileNetV2(weights='imagenet')  # Load pre-trained MobileNetV2 model


# Create your views here.
from django.shortcuts import render
from .forms import ImageUploadForm

def classify_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the image
            img = form.cleaned_data['image']
            img_path = 'temp_image.jpg'
            
            # Save the uploaded image temporarily
            with open(img_path, 'wb+') as destination:
                for chunk in img.chunks():
                    destination.write(chunk)
            
            # Preprocess the image for the model
            img = image.load_img(img_path, target_size=(224, 224))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = preprocess_input(img_array)

            # Make prediction
            predictions = model.predict(img_array)
            results = decode_predictions(predictions, top=3)[0]
            
            return render(request, 'result.html', {'results': results})

    else:
        form = ImageUploadForm()

    return render(request, 'upload.html', {'form': form})
