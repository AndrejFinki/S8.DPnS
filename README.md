# DPnS Project (Summer 2024-25) 
Дигитално Процесирање на Слика - Препознавање на текст со користење на OCR

# Data Source
We use the TextOCR Dataset, which is hosted on Kaggle ([link](https://www.kaggle.com/datasets/robikscube/textocr-text-extraction-from-images-dataset)).

# Pre-Setup

To run the application you will need to install pre-required software, which is given below (for Linux).

```bash
sudo apt install redis
sudo systemctl enable redis-server
sudo systemctl start redis-server

sudo apt install tesseract-ocr
sudo apt install libtesseract-dev
```

Moreover, it is recommended to create a venv env using the requirements.txt.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt 
```

# Contributing
- Andrej Shekerov  [216050, FCSE - Skopje]
- Nikola Petrovski [216051, FCSE - Skopje]