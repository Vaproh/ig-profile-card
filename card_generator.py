import io
import urllib.request
from PIL import Image, ImageDraw, ImageFont


def download_image(url: str) -> Image.Image:
    if not url:
        return Image.new("RGBA", (150, 150), (200, 200, 200, 255))
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            data = resp.read()
        img = Image.open(io.BytesIO(data))
        img = img.convert("RGBA")
        return img
    except Exception:
        return Image.new("RGBA", (150, 150), (200, 200, 200, 255))


def round_crop(img: Image.Image, radius: int = 75) -> Image.Image:
    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), img.size], radius=radius, fill=255)
    result = img.copy()
    result.putalpha(mask)
    return result


def format_count(n: int) -> str:
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n / 1_000:.1f}K"
    return str(n)


def generate_card(data: dict) -> bytes:
    W, H = 600, 400
    BG_COLOR = (10, 10, 15, 255)
    ACCENT_COLOR = (0, 150, 255, 255)
    TEXT_COLOR = (255, 255, 255, 255)
    GRAY_COLOR = (150, 150, 150, 255)
    PRIVATE_COLOR = (255, 200, 0, 255)

    img = Image.new("RGBA", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    pfp_size = 150
    pfp_raw = download_image(data.get("profile_pic_url", ""))
    pfp = pfp_raw.resize((pfp_size, pfp_size), Image.Resampling.LANCZOS)
    pfp = round_crop(pfp, radius=75)
    pfp_pos = (40, 40)
    img.paste(pfp, pfp_pos, pfp)

    username = data.get("username", "unknown")
    full_name = data.get("full_name", "")

    try:
        username_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
        name_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
        stats_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
        bio_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
        badge_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
    except Exception:
        username_font = ImageFont.load_default()
        name_font = ImageFont.load_default()
        stats_font = ImageFont.load_default()
        bio_font = ImageFont.load_default()
        badge_font = ImageFont.load_default()

    text_x = pfp_pos[0] + pfp_size + 30

    draw.text((text_x, 50), f"@{username}", font=username_font, fill=TEXT_COLOR)

    name_y = 95
    if full_name:
        draw.text((text_x, name_y), full_name, font=name_font, fill=GRAY_COLOR)

    stats_y = 145
    followers = data.get("followers", 0)
    following = data.get("following", 0)
    posts = data.get("posts", 0)

    draw.text((text_x, stats_y), f"Posts: {format_count(posts)}", font=stats_font, fill=TEXT_COLOR)
    draw.text((text_x + 130, stats_y), f"Followers: {format_count(followers)}", font=stats_font, fill=TEXT_COLOR)
    draw.text((text_x + 300, stats_y), f"Following: {format_count(following)}", font=stats_font, fill=TEXT_COLOR)

    badge_y = 190
    if data.get("is_verified"):
        draw.text((text_x, badge_y), "✓ Verified", font=badge_font, fill=ACCENT_COLOR)
    if data.get("is_private"):
        draw.text((text_x + 120, badge_y), "🔒 Private", font=badge_font, fill=PRIVATE_COLOR)

    bio = data.get("bio", "")[:200]
    if bio:
        bio_y = 230
        for i, line in enumerate(wrap_text(bio, bio_font, 50, draw)):
            draw.text((40, bio_y + i * 25), line, font=bio_font, fill=GRAY_COLOR)

    external_url = data.get("external_url", "")
    if external_url:
        url_y = 320 if bio else 280
        draw.text((40, url_y), f"🔗 {external_url[:60]}", font=stats_font, fill=ACCENT_COLOR)

    output = io.BytesIO()
    img.save(output, format="PNG")
    return output.getvalue()


def wrap_text(text: str, font: ImageFont.ImageFont, max_chars: int, draw: ImageDraw.ImageDraw) -> list:
    words = text.split()
    lines = []
    current = ""
    for word in words:
        test = current + " " + word if current else word
        if draw.textlength(test, font=font) < max_chars * 6:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines[:4]