# Screen Text Recognizer

A Python package to capture and recognize text from a specific screen area using mss and ddddocr.

## Installation

```bash


pip install dong-screen-orc2txt

如果失败，先 pip install opencv-python-headless --prefer-binary

```

```python

from dong_screen_orc2txt import Orc2txt

orc2txt = Orc2txt()
text = orc2txt.capture_and_recognize(100, 100, 300, 200) # x,y,width,height
print("text:", text)


```
