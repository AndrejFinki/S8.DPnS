from django.db import models

# Create your models here.
class Image(models.Model):
    algorithm_choices = [
        ('EASYOCR', 'EasyOCR'),
        ('PYTESSERACT', 'Pytesseract'),
        ('KERASOCR', 'KerasOCR')
    ]
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    algorithm = models.CharField(max_length=100, choices=algorithm_choices)
    
    image = models.ImageField()
    
    processed_image = models.ImageField(upload_to='processed_images/', blank=True, null=True)
    is_processed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} - {self.algorithm}'
    
class Word(models.Model):
    id = models.AutoField(primary_key=True)
    word = models.CharField(max_length=255)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='words')
    
    def __str__(self):
        return self.word