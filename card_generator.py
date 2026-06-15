import io
import urllib.request
from PIL import Image, ImageDraw, ImageFont


def download_image(url: str) -> Image.Image:
    if not url:
        return Image.new("RGBA", (150, 150), (100, 100, 100, 255))
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            data = resp.read()
        img = Image.open(io.BytesIO(data))
        img = img.convert("RGBA")
        return img
    except Exception:
        return Image.new("RGBA", (150, 150), (100, 100, 100, 255))


def round_crop(img: Image.Image, size: int, radius: int = 75) -> Image.Image:
    img = img.resize((size, size), Image.Resampling.LANCZOS)
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse([(0, 0), (size, size)], fill=255)
    result = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    result.paste(img, (0, 0))
    result.putalpha(mask)
    return result


def format_count(n: int) -> str:
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n / 1_000:.1f}K"
    return str(n)


def generate_card(data: dict) -> bytes:
    W, H = 600, 500
    BG_COLOR = (15, 15, 20, 255)
    CARD_BG = (25, 25, 35, 255)
    ACCENT = (0, 180, 255, 255)
    VERIFIED_BLUE = (0, 120, 255, 255)
    TEXT_WHITE = (255, 255, 255, 255)
    TEXT_GRAY = (180, 180, 190, 255)
    STATS_COLOR = (220, 220, 230, 255)

    img = Image.new("RGBA", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    draw.rounded_rectangle([(20, 20), (W - 20, H - 20)], radius=30, fill=CARD_BG)

    pfp_size = 120
    pfp_raw = download_image(data.get("profile_pic_url", ""))
    pfp = round_crop(pfp_raw, pfp_size, radius=60)
    pfp_pos = (50, 50)
    img.paste(pfp, pfp_pos, pfp)

    username = data.get("username", "unknown")
    full_name = data.get("full_name", "")

    try:
        username_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32)
        name_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
        stat_label_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
        stat_num_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
        bio_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 17)
        badge_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
    except Exception:
        username_font = ImageFont.load_default()
        name_font = username_font
        stat_label_font = username_font
        stat_num_font = username_font
        bio_font = username_font
        badge_font = username_font

    text_x = pfp_pos[0] + pfp_size + 30

    y = 55
    username_text = f"@{username}"
    draw.text((text_x, y), username_text, font=username_font, fill=TEXT_WHITE)

    if data.get("is_verified"):
        badge_x = text_x + username_font.getlength(username_text) + 10
        draw.text((badge_x, y + 5), "✓", font=badge_font, fill=VERIFIED_BLUE)

    y = 95
    if full_name:
        draw.text((text_x, y), full_name, font=name_font, fill=TEXT_GRAY)

    stats_y = 140
    followers = data.get("followers", 0)
    following = data.get("following", 0)
    posts = data.get("posts", 0)

    stat_box_w = 140
    gap = 20
    start_x = text_x

    for i, (label, value) in enumerate([
        ("Posts", format_count(posts)),
        ("Followers", format_count(followers)),
        ("Following", format_count(following))
    ]):
        x = start_x + i * (stat_box_w + gap)
        draw.text((x, stats_y), label, font=stat_label_font, fill=TEXT_GRAY)
        draw.text((x, stats_y + 20), str(value), font=stat_num_font, fill=TEXT_WHITE)

    divider_y = stats_y + 60
    draw.line([(text_x, divider_y), (W - 50, divider_y)], fill=(60, 60, 80, 255), width=1)

    bio = data.get("bio", "")
    bio_lines = []
    if bio:
        bio_y = divider_y + 20
        bio_lines = wrap_text(bio, bio_font, 45, draw)
        for i, line in enumerate(bio_lines[:4]):
            draw.text((text_x, bio_y + i * 26), line, font=bio_font, fill=TEXT_GRAY)

    external_url = data.get("external_url", "")
    if external_url and len(bio_lines) <= 3:
        url_y = divider_y + 20 + len(bio_lines) * 26 + 15
        if url_y < H - 50:
            draw.text((text_x, url_y), f"🔗 {external_url[:50]}", font=stat_label_font, fill=ACCENT)

    if data.get("is_private"):
        lock_y = H - 70
        draw.rounded_rectangle([(text_x, lock_y), (text_x + 110, lock_y + 35)], radius=8, fill=(50, 50, 60, 255))
        draw.text((text_x + 15, lock_y + 7), "🔒 Private Account", font=badge_font, fill=TEXT_GRAY)

    output = io.BytesIO()
    img.save(output, format="PNG")
    return output.getvalue()


def wrap_text(text: str, font: ImageFont.ImageFont, max_chars: int, draw: ImageDraw.ImageDraw) -> list:
    words = text.split()
    lines = []
    current = ""
    for word in words:
        test = current + " " + word if current else word
        if draw.textlength(test, font=font) < max_chars * 7:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines