from PIL import Image, ImageDraw, ImageFont
import textwrap
import random

def get_contrast_color(bg_color):
    # Формула контрасту за WCAG
    r, g, b = bg_color
    luminance = (0.299 * r + 0.587 * g + 0.114 * b)
    return (0, 0, 0) if luminance > 186 else (255, 255, 255)

def generate_gradient(size, color1, color2):
    """Вертикальний градієнт від color1 до color2"""
    width, height = size
    base = Image.new("RGB", (width, height), color1)
    top = Image.new("RGB", (width, height), color2)

    # Створюємо вертикальну маску (альфа-канал)
    mask = Image.new("L", (width, height))
    for y in range(height):
        alpha = int(255 * (y / height))
        for x in range(width):
            mask.putpixel((x, y), alpha)

    base.paste(top, (0, 0), mask)
    return base

def create_image_post(text: str, output_path="post.png"):
    width, height = 1080, 1080
    font_paths = [
"fonts\segoeprb.ttf",

    ]
    font = ImageFont.truetype(random.choice(font_paths), size=60)

    # Випадкові кольори для градієнта
    color1 = tuple(random.randint(0, 255) for _ in range(3))
    color2 = tuple(random.randint(0, 255) for _ in range(3))

    image = generate_gradient((width, height), color1, color2)
    draw = ImageDraw.Draw(image)

    text_color = get_contrast_color(color1)  # беремо перший колір для контрасту

    # Автоматичне перенесення рядків
    padding = 100
    max_width = width - 2 * padding

    # Переносимо текст за шириною
    lines = wrap_text_by_pixel(draw, text, font, max_width)

    # Обчислюємо загальну висоту тексту
    total_text_height = sum(draw.textbbox((0, 0), line, font=font)[3] for line in lines)

    # Початкове Y-значення з центруванням + padding
    y = max(padding, (height - total_text_height) // 2)

    # Малюємо кожен рядок
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x = max(padding, (max_width - text_width) // 2)  # центрування
        draw.text((x, y), line, font=font, fill="black")
        y += bbox[3] - bbox[1] + 10  # відступ між рядками
    image = add_rounded_corners(image, radius=150)
    image.save(output_path, format="PNG")
    return output_path

def wrap_text_by_pixel(draw, text, font, max_width):
    """Розбиває текст на рядки, які вміщаються у max_width"""
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        line = ""
        for word in words:
            test_line = line + " " + word if line else word
            width = draw.textlength(test_line, font=font)
            if width <= max_width:
                line = test_line
            else:
                if line:
                    lines.append(line)
                line = word
        if line:
            lines.append(line)
        lines.append("")  # абзац
    return lines

def add_rounded_corners(im: Image.Image, radius: int) -> Image.Image:
    """Додає скруглені кути до зображення"""
    # Створюємо маску з прозорими кутами
    mask = Image.new("L", im.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), im.size], radius=radius, fill=255)
    
    # Додаємо альфа-канал до оригінального зображення
    im = im.convert("RGBA")
    im.putalpha(mask)
    return im