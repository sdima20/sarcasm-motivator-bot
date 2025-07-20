from PIL import Image, ImageDraw, ImageFont
import textwrap
import hashlib

def get_color_from_text(text, lightness=200):
    """Генерує колір на основі хешу тексту."""
    h = hashlib.md5(text.encode()).hexdigest()
    r = (int(h[:2], 16) + lightness) % 256
    g = (int(h[2:4], 16) + lightness) % 256
    b = (int(h[4:6], 16) + lightness) % 256
    return (r, g, b)

def create_image_post(text: str, output_path='post.png'):
    WIDTH, HEIGHT = 1080, 1080
    MARGIN = 80
    RADIUS = 40

    # Генерація кольору фону та тексту з тексту
    bg_color = get_color_from_text(text, 180)
    text_color = get_color_from_text(text[::-1], 40)

    # Створення зображення з рамкою
    base = Image.new('RGB', (WIDTH, HEIGHT), (255, 255, 255))
    image = Image.new('RGB', (WIDTH - 2 * MARGIN, HEIGHT - 2 * MARGIN), bg_color)

    # Заокруглення кутів (опційно)
    mask = Image.new("L", image.size, 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.rounded_rectangle((0, 0, image.size[0], image.size[1]), RADIUS, fill=255)

    image.putalpha(mask)
    base.paste(image, (MARGIN, MARGIN), mask=image)

    draw = ImageDraw.Draw(base)
    font = ImageFont.truetype("arial.ttf", size=60)

    # Обчислення рядків із переносом
    max_width = WIDTH - 2 * MARGIN * 1.5
    lines = []
    for paragraph in text.split('\n'):
        wrapped = textwrap.wrap(paragraph, width=30)
        lines.extend(wrapped)
    
    # Центрування тексту
    total_text_height = sum(draw.textbbox((0, 0), line, font=font)[3] for line in lines) + len(lines)*10
    y = (HEIGHT - total_text_height) // 2

    for line in lines:
        line_width = draw.textlength(line, font=font)
        x = (WIDTH - line_width) // 2
        draw.text((x, y), line, font=font, fill=text_color)
        bbox = draw.textbbox((0, 0), line, font=font)
        line_height = bbox[3] - bbox[1]
        y += line_height + 10

    base.save(output_path)
    return output_path