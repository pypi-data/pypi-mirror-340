# Screen Text Recognizer

A Python package to capture and recognize text from a specific screen area using mss and ddddocr.

## Installation

```bash


pip install dong-screen-orc2txt

如果失败，pip install opencv-python-headless --prefer-binary

```

```python

from dong-screen-orc2txt import orc2txt

recognizer = orc2txt()
text = recognizer.capture_and_recognize(100, 100, 300, 200) # x,y,width,height
print("Recognized text:", text)


```


