import logging

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(funcName)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def slugify(text):
    """
    Returns a slug string valid for URLs.
    """
    ascii_text = unidecode.unidecode(text)
    return re.sub(r'[-\s]+', '-',
                  (re.sub(r'[^\w\s-]', '', ascii_text).strip().lower()))

