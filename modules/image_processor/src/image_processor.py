from PIL import Image, ImageDraw, ImageFont
import io
from src.logger import logger


def process_image(image_bytes: bytes, description: str) -> bytes:
    try:
        image = Image.open(io.BytesIO(image_bytes))

        try:
            font = ImageFont.truetype("./fonts/Arial.ttf", 12)
        except OSError:
            logger.warning("Arial font not found. Using default font.")
            font = ImageFont.load_default()

        draw = ImageDraw.Draw(image)
        max_width = image.width - 20

        lines = []
        for line in description.splitlines():
            words = line.split()
            current_line = ""
            for word in words:
                test_line = current_line + word + " "
                if draw.textsize(test_line, font=font)[0] <= max_width:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = word + " "
            lines.append(current_line.strip())

        text_height = sum([draw.textsize(line, font=font)[1] for line in lines]) + 10
        new_height = image.height + text_height + 10

        result_image = Image.new("RGB", (image.width, new_height))
        result_image.paste(image, (0, 0))

        draw = ImageDraw.Draw(result_image)
        draw.rectangle([0, image.height, image.width, new_height], fill="black")

        y_text = image.height + 5
        for line in lines:
            draw.text((10, y_text), line, font=font, fill="white")
            y_text += draw.textsize(line, font=font)[1]

        output = io.BytesIO()
        result_image.save(output, format="JPEG")
        output.seek(0)

        return output.getvalue()

    except Exception as e:
        logger.error(f"Ошибка при обработке изображения: {e}")
        raise
