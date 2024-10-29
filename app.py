from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from PIL import Image, ImageDraw, ImageFont
import os

app = Flask(__name__)

# Define the upload folder
UPLOAD_FOLDER = 'uploads/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the 'overlay' field exists in the request
        overlay_file = request.files.get('overlay')  # Use get to avoid KeyError
        background_file = request.files.get('background')  # Use get to avoid KeyError

        if not background_file:
            return "Background file is required.", 400  # Handle error for missing background

        # Differentiate based on the presence of 'overlay'
        if overlay_file:
            name = request.form.get('name', '')  # Get name, default to empty string
            designation = request.form.get('designation', '')  # Get designation, default to empty string

            # Handle the overlay image case
            background_path = os.path.join(UPLOAD_FOLDER, 'background.jpg')
            overlay_path = os.path.join(UPLOAD_FOLDER, 'overlay.png')
            background_file.save(background_path)
            overlay_file.save(overlay_path)

            output_filename = f"{name.replace(' ', '_')}.jpg" if name else "output_image.jpg"
            output_path = os.path.join(UPLOAD_FOLDER, output_filename)

            overlay_images(background_path, overlay_path, output_path, name, designation)

            return render_template('upload.html', success=True, filename=output_filename, name=name, designation=designation)

        else:
            # Handle the case for the first form (Generate Image with Text)
            text = request.form.get('text', '')
            highlight = request.form.get('highlight', '')

            # Process the first form (image generation) here...
            output_filename = generate_image_with_text(background_file, text, highlight)
            return render_template('upload.html', success=True, filename=output_filename)

    return render_template('upload.html')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


def overlay_images(background_path, overlay_path, output_path, name, designation):
    background = Image.open(background_path)
    overlay = Image.open(overlay_path)
    overlay = overlay.resize(background.size, Image.LANCZOS)

    background.paste(overlay, (0, 0), overlay)

    draw = ImageDraw.Draw(background)
    font_path = 'assets/fonts/poppins-Bold.ttf'  # Ensure this path is correct

    # Font for name (large)
    name_font_size = 50
    name_font = ImageFont.truetype(font_path, name_font_size)

    # Draw the name only if provided
    if name:
        name_text = f"{name}"
        name_bbox = draw.textbbox((0, 0), name_text, font=name_font)

        center_x_name = (background.width - (name_bbox[2] - name_bbox[0])) // 2
        center_y_name = (background.height // 2) - ((name_bbox[3] - name_bbox[1]) // 2) + 300

        shadow_offset = 8
        draw.text((center_x_name + shadow_offset, center_y_name + shadow_offset), name_text, fill="black", font=name_font)

        rgb_color = (6, 40, 86)
        stroke_width = 5
        draw.text(
            (center_x_name, center_y_name),
            name_text,
            fill=rgb_color,
            font=name_font,
            stroke_fill="white",
            stroke_width=stroke_width
        )

    # Font for designation (small)
    designation_font_size = 30
    designation_font = ImageFont.truetype(font_path, designation_font_size)

    # Draw the designation below the name if provided
    if designation:
        designation_text = designation
        designation_bbox = draw.textbbox((0, 0), designation_text, font=designation_font)

        center_x_designation = (background.width - (designation_bbox[2] - designation_bbox[0])) // 2
        center_y_designation = center_y_name + 75  # Adjust the y position as needed

        draw.text(
            (center_x_designation, center_y_designation),
            designation_text,
            fill=rgb_color,
            font=designation_font
        )

    background.save(output_path)

def generate_image_with_text(background_file, text, highlight):
    # Generate an image based on the text input
    background_path = os.path.join(UPLOAD_FOLDER, 'background.jpg')
    background_file.save(background_path)

    output_filename = "generated_image.jpg"  # Default filename for generated image
    output_path = os.path.join(UPLOAD_FOLDER, output_filename)

    # Open the image
    background = Image.open(background_path)
    draw = ImageDraw.Draw(background)
    font_path = 'assets/fonts/poppins-Bold.ttf'  # Ensure this path is correct
    font_size = 100
    font = ImageFont.truetype(font_path, font_size)

    # Define padding and line height
    padding = 50
    max_width = background.width - (2 * padding)  # Max width for text
    line_height = font_size * 2  # Increase line height (20% more than font size)

    # Wrap text into multiple lines
    wrapped_text = []
    words = text.split()
    line = ""

    for word in words:
        # Check if adding the next word exceeds max width
        test_line = f"{line} {word}".strip()
        # Get bounding box for the test line
        line_bbox = draw.textbbox((0, 0), test_line, font=font)

        line_width = line_bbox[2] - line_bbox[0]  # width of the text

        if line_width <= max_width:
            line = test_line
        else:
            wrapped_text.append(line)
            line = word  # Start a new line with the current word

    # Add the last line if any
    if line:
        wrapped_text.append(line)

    # Calculate total height needed for the text
    total_height = sum(draw.textbbox((0, 0), line, font=font)[3] - draw.textbbox((0, 0), line, font=font)[1] for line in wrapped_text)

    # Calculate starting Y position to center the text vertically and adjust upward
    current_y = (background.height - total_height) // 2 - (line_height // 4)  # Shift upward

    # Draw the wrapped text on the image, centered horizontally
    for line in wrapped_text:
        line_bbox = draw.textbbox((0, 0), line, font=font)
        line_width = line_bbox[2] - line_bbox[0]  # width of the text
        x = (background.width - line_width) // 2  # Center horizontally
        draw.text((x, current_y), line, fill="white", font=font)
        current_y += line_height  # Move down for the next line with increased line height

    # Save the modified image
    background.save(output_path)
    return output_filename

if __name__ == '__main__':
    app.run(debug=True)
