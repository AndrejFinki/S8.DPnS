from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

from .models import Image, Word
from .forms import ImageForm


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

        form = ImageForm()
        return render(request, "add.html", {"form": form})


class ListView(View):

    def get(self, request):
        images = Image.objects.all()
        
        return render(request, "list.html", {"images": images})
    
    
class SingleView(View):
    def get(self, request, id):
        image = Image.objects.get(id=id)
        words = Word.objects.filter(image=image)
        
        words_concat = ' '.join([word.word for word in words])
        
        if words_concat == '':
            if not image.is_processed:
                words_concat = 'Still Processing'
            else:
                words_concat = 'No words found'
        
        status = 'Done' if image.is_processed else 'Processing'
        
        return render(request, "view.html", {"image": image, "words": words_concat, "status": status})
