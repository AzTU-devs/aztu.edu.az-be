import re
import unicodedata

# Azerbaijani-specific character map
_AZ_MAP = str.maketrans({
    'ə': 'e', 'Ə': 'E',
    'ü': 'u', 'Ü': 'U',
    'ö': 'o', 'Ö': 'O',
    'ğ': 'g', 'Ğ': 'G',
    'ı': 'i', 'İ': 'I',
    'ç': 'c', 'Ç': 'C',
    'ş': 's', 'Ş': 'S',
})


def make_slug(title: str) -> str:
    """Convert a title to a URL-safe slug.

    Handles Azerbaijani characters (ə→e, ü→u, ö→o, ğ→g, ı→i, ç→c, ş→s)
    before normalising remaining unicode to ASCII.
    """
    text = title.translate(_AZ_MAP)
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore').decode('ascii')
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-')
