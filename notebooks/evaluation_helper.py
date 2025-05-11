import easyocr

def clean_word(word: str) -> str:
    """
    Cleans a word by removing any non-alphanumeric characters and converting it to lowercase.
    """
    
    return ''.join(char for char in word if char.isalnum()).lower()


def extract_words(reader: easyocr.Reader, image_path: str) -> list:
    """
    Extracts words from an image using EasyOCR.
    
    Args:
        reader (easyocr.Reader): The EasyOCR reader object.
        image_path (str): The path to the image file.
        
    Returns:
        list: A list of cleaned words extracted from the image.
    """
    
    results = reader.readtext(image_path, paragraph=False, width_ths=0)
    
    words = []
    for (bbox, text, prob) in results:
        cleaned_word = clean_word(text)
        
        if cleaned_word:
            words.append(cleaned_word)
    
    return words
    