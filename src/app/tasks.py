import os
from celery import shared_task

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

import cv2
from easyocr import Reader

from .models import Image, Word

BORDER_COLOR = (0, 255, 0)  # Green (BGR format)
BORDER_THICKNESS = 2
FONT_COLOR = (0, 0, 255)  # Red (BGR format)
FONT_SIZE = 1

def clean_text(text):
    """
    Clean the text by removing unwanted characters.
    """
    text = text.strip()
    text = text.lower()

    return ''.join([c for c in text if c.isalnum() or c.isspace()])


def extract_result(image_path, result):
    """
    Extract the result from the OCR process and draw rectangles around the detected words.
    """

    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    words = []

    for (bbox, text, prob) in result:
        x1, y1, x2, y2 = bbox[0][0], bbox[0][1], bbox[2][0], bbox[2][1]
        cleaned_text = clean_text(text)

        if cleaned_text:
            words.append(cleaned_text)

            cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), BORDER_COLOR, BORDER_THICKNESS)
            cv2.putText(image, cleaned_text, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, FONT_COLOR, FONT_SIZE)

    return image, words


@shared_task
def easy_ocr_task(id, image_path):
    """
    Task to process an image using EasyOCR and save the results.
    """
    # Initialize the OCR reader
    reader = Reader(['en'], gpu=False)

    # Read the image
    result = reader.readtext(
        image_path,
        paragraph=False,
        width_ths=0
    )

    # Process the result
    image, words = extract_result(image_path, result)

    # Save the words to the database
    image_obj = Image.objects.get(id=id)

    for word in words:
        word_obj = Word(image=image_obj, word=word)
        word_obj.save()

    # Save the processed image
    _, buffer = cv2.imencode('.jpg', image)

    image_obj.image.save(
        os.path.basename(image_path),
        ContentFile(buffer.tobytes()),
        save=False
    )

    image_obj.is_processed = True
    image_obj.save()


