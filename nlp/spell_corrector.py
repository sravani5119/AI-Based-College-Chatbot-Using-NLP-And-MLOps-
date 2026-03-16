from spellchecker import SpellChecker

spell = SpellChecker()

# -------------------------
# Load domain words
# -------------------------
domain_words = set()

with open("data/structured/domain_words.txt", "r") as f:
    for line in f:
        word = line.strip().lower()
        if word:
            domain_words.add(word)

# Add them to spellchecker vocabulary
spell.word_frequency.load_words(domain_words)


def correct_spelling(text: str):

    words = text.split()
    corrected_words = []

    for word in words:

        lower_word = word.lower()

        # If domain word → keep it
        if lower_word in domain_words:
            corrected_words.append(word)
            continue

        # Otherwise try correction
        corrected = spell.correction(lower_word)

        if corrected:
            corrected_words.append(corrected)
        else:
            corrected_words.append(word)

    return " ".join(corrected_words)