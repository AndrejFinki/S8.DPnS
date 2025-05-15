from django import forms
from .models import Image, Word

class ImageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Image
        fields = ['name', 'algorithm', 'image']
        
        name_widget = forms.TextInput(
            attrs={
                'id': 'name',
                'class': 'form-control my-2',
                'placeholder': 'Image Name',
                'required': 'required',
            }
        )
        
        algorithm_widget = forms.Select(
            attrs={
                'id': 'algorithm',
                'label': 'Algorithm',
                'class': 'form-control my-2',
                'placeholder': 'Select Algorithm',
            }
        )
        
        image_widget = forms.ClearableFileInput(
            attrs={
                'id': 'image',
                'multiple': False,
                'class': 'form-control my-2',
                'placeholder': 'Upload Image',
            }
        )
        
        widgets = {
            'name': name_widget,
            'algorithm': algorithm_widget,
            'image': image_widget,
        }