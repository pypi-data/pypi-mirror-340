import os

__version__ = '0.1.2'
__all__ = [
    'get_fonts'
]


def get_fonts(font_name):
    # 获取当前文件的目录
    current_dir = os.path.dirname(__file__)
    # 字体文件目录
    fonts_dir = os.path.join(current_dir, 'fonts')

    # 常见的字体文件扩展名
    font_extensions = [
        '.ttf',
        '.ttc',
        '.otf',
        ''
    ]

    # 在字体目录中查找匹配的字体文件
    for ext in font_extensions:
        font_file = font_name + ext
        font_path = os.path.join(fonts_dir, font_file)
        if os.path.isfile(font_path):
            return font_path

    # 如果没有找到匹配的字体文件，抛出异常
    raise ValueError(f"Font '{font_name}' not found in supported formats: {font_extensions}")
