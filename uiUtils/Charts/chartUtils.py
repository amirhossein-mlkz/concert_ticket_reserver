class Font:
    def __init__(self, font: str = None, font_size: int = None, bold: bool = None) -> None:
        if font:
            self.font = font
        else:
            self.font = 'Arial'

        if font_size:
            self.font_size = font_size
        else:
            self.font_size = 8

        if bold:
            self.bold = bold
        else:
            self.bold = False