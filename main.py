import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageOps
import io
import textwrap

# Load template image (you can replace this with a URL or use a local file)
TEMPLATE_PATH = "greeting_template.png"  # Use / instead of \ for compatibility

# Title
st.title("🎉 Automatic Card Generator")

# Upload form
with st.form("greeting_form"):
    name = st.text_input("Your Name")
    position = st.text_input("Your Position")
    quote = st.text_input("Enter a Quote")
    uploaded_image = st.file_uploader("Upload Your Face Image", type=["jpg", "jpeg", "png"])
    submitted = st.form_submit_button("Generate Greeting Card")

# When submitted
if submitted and uploaded_image and name and position and quote:
    try:
        # Load base template
        template = Image.open(TEMPLATE_PATH).convert("RGBA")

        # Load uploaded image and make it circular
        user_img = Image.open(uploaded_image).convert("RGBA")
        user_img = user_img.resize((150, 150))
        
        # Create circular mask
        mask = Image.new("L", user_img.size, 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.ellipse((0, 0, 150, 150), fill=255)
        user_img.putalpha(mask)

        # Paste the circular face image onto the template
        template.paste(user_img, (645, 620), user_img)

        # Draw text
        draw = ImageDraw.Draw(template)

        # Fonts (adjust paths as needed)
        font_bold = ImageFont.truetype("arialbd.ttf", size=30)   # Bold for quote
        font_regular = ImageFont.truetype("arial.ttf", size=30)  # Regular for name
        font_italic = ImageFont.truetype("ariali.ttf", size=30)  # Italic for position

        # Wrap the quote text if it's too long (set max width)
        max_width =350  # Set your max width for the quote
        wrapped_quote = textwrap.fill(quote, width=50)  # Wrap text within a limit

        # Draw wrapped quote
        draw.text((100, 290), wrapped_quote, fill="black", font=font_bold)

        # Draw other texts (name, position)
        draw.text((450, 450), name, fill="black", font=font_regular)
        draw.text((450, 480), position, fill="black", font=font_italic)

        # Display result
        st.image(template, caption="Your Greeting Card", use_column_width=True)

        # Save to buffer
        buf = io.BytesIO()
        template.save(buf, format="PNG")
        byte_im = buf.getvalue()

        # Download button
        st.download_button(
            label="📥 Download Greeting Card",
            data=byte_im,
            file_name=f"{name}_card.png",
            mime="image/png"
        )

    except Exception as e:
        st.error(f"Something went wrong: {e}")
else:
    st.info("Fill out the form and upload an image to generate your card.")
