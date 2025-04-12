import base64
from typing import List
from pathlib import Path
import anywidget
import traitlets
from io import BytesIO


def base64_to_pil(base64_string):
    """Convert a base64 string to PIL Image"""
    from PIL import Image

    # Remove the data URL prefix if it exists
    if 'base64,' in base64_string:
        base64_string = base64_string.split('base64,')[1]

    # Decode base64 string
    img_data = base64.b64decode(base64_string)

    # Create PIL Image from bytes
    return Image.open(BytesIO(img_data))


class Draw(anywidget.AnyWidget):
    """Initialize a Draw widget based on tldraw.
    """
    _esm = Path(__file__).parent / 'static' / 'draw.js'
    _css = Path(__file__).parent / 'static' / 'draw.css'
    width = traitlets.Int(800).tag(sync=True)
    height = traitlets.Int(500).tag(sync=True)
    base64 = traitlets.Unicode("").tag(sync=True)

    def __init__(self, width: int = 800, height: int = 500, **kwargs) -> None:
        super().__init__(width=width, height=height, **kwargs)
    
    def get_pil(self):
        if not self.base64:
            raise ValueError("No base64 image data available, make sure you draw something first.")
        return base64_to_pil(self.base64)

    def get_base64(self) -> str:
        return self.base64