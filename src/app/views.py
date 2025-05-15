from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

from .models import Image, Word
from .forms import ImageForm
from .tasks import easy_ocr_task, pytesseract_task, keras_ocr_task


class IndexView(View):

    def get(self, request):
        return render(request, "index.html")

    def post(self, request):
        return render(request, "index.html")


class ImageView(View):

    def get(self, request):
        form = ImageForm()
        return render(request, "add.html", {"form": form})

    def post(self, request):
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            
            item.is_processed = False
            item.image = form.cleaned_data['image']
            
            item.save()

            # Call the task to process the image
            if item.algorithm.lower() == 'easyocr':
                easy_ocr_task.delay(item.id, item.image.path)

            elif item.algorithm.lower() == 'pytesseract':
                pytesseract_task.delay(item.id, item.image.path)

            elif item.algorithm.lower() == 'kerasocr':
                keras_ocr_task.delay(item.id, item.image.path)

        form = ImageForm()
        return render(request, "add.html", {"form": form})


class ListView(View):

    def get(self, request):
        images = Image.objects.all()
        
        return render(request, "list.html", {"images": images})
    
    
class SingleView(View):
    def get(self, request, id):
        image_obj = Image.objects.get(id=id)
        words = Word.objects.filter(image=image_obj)
        
        words_concat = ', '.join([word.word.capitalize() for word in words])
        
        if not image_obj.is_processed:
            words_concat = 'Still Processing'

        elif words_concat == '':
            words_concat = 'No words found'
        
        status = 'Done' if image_obj.is_processed else 'Processing'

        
        image_to_show = image_obj.image 
        if status == 'Done' and image_obj.processed_image:
            image_to_show = image_obj.processed_image

        return render(request, "view.html", {
            "image_obj": image_obj, 
            "image_to_show": image_to_show, 
            "words": words_concat, 
            "status": status
            }
        )
