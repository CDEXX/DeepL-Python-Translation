import requests
import time
import sys

# DeepL API key
DEEPL_API_KEY = "your api key"
DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"

def translate_word(word, target_lang):
    params = {
        "auth_key": DEEPL_API_KEY,
        "text": word,
        "target_lang": target_lang
    }
    try:
        response = requests.get(DEEPL_API_URL, params=params)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.json()["translations"][0]["text"]
    except requests.exceptions.RequestException as e:
        print(f"Error translating '{word}': {e}")
        return None

def create_word_dict():
    common_french_words = [
        "le", "de", "un", "à", "être", "et", "en", "avoir", "que", "pour",
 ]
    word_list = []
    for i, french_word in enumerate(common_french_words, 1):
        english_translations = translate_word(french_word, "EN")
        if english_translations:
            # Ensure english_translations is a list
            if isinstance(english_translations, str):
                english_translations = [english_translations]

            turkish_translations = []
            for english_translation in english_translations:
                turkish_translation = translate_word(english_translation, "TR")
                # Ensure turkish_translation is a list
                if isinstance(turkish_translation, str):
                    turkish_translation = [turkish_translation]
                turkish_translations.extend(turkish_translation)

            word_dict = {
                "french": french_word,
                "english": ", ".join(english_translations),
                "turkish": ", ".join(turkish_translations)
            }
            word_list.append(word_dict)
        time.sleep(0)  # To avoid hitting API rate limits
    return word_list

def save_to_file(word_list):
    with open("french_words_translated.py", "w", encoding="utf-8") as f:
        f.write("words = [\n")
        for word in word_list:
            f.write(f"    {word},\n")
        f.write("]\n")

if __name__ == "__main__":
    # Redirect stdout to a file
    with open("translation_output.txt", "w", encoding="utf-8") as f:
        original_stdout = sys.stdout  # Save a reference to the original standard output
        sys.stdout = f  # Redirect standard output to the file
        try:
            print("Starting translation process...")
            word_list = create_word_dict()
            save_to_file(word_list)
            print("Translation process completed.")
        finally:
            sys.stdout = original_stdout  # Reset standard output to its original value
