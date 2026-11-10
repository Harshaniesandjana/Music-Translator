
import time
from deep_translator import GoogleTranslator


def translate_lines(original_lines):
    """
    Vertaal originele regels naar Engels in batches.
    Behoud de volgorde en het aantal regels.
    """

    translator = GoogleTranslator(source="auto", target="en")
    translated_lines = []

    batch_size = 5

    for start in range(0, len(original_lines), batch_size):
        batch = original_lines[start:start + batch_size]

        try:
            translations = translator.translate_batch(batch)

            if len(translations) != len(batch):
                raise ValueError("Het aantal vertalingen komt niet overeen.")

            translated_lines.extend([
                translation if translation else "[Translation unavailable]"
                for translation in translations
            ])

        except Exception as error:
            raise RuntimeError(
                "De vertaling is tijdelijk niet beschikbaar. "
                "Probeer het later opnieuw."
            ) from error

        # Korte pauze tussen batches
        if start + batch_size < len(original_lines):
            time.sleep(1)

    return translated_lines
