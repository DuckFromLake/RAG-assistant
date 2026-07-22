import re

STOP_WORDS = {
    'и', 'в', 'во', 'не', 'что', 'он', 'на', 'я', 'с', 'со', 'как',
    'а', 'то', 'все', 'она', 'так', 'его', 'но', 'да', 'ты', 'к',
    'у', 'же', 'вы', 'за', 'бы', 'по', 'только', 'ее', 'мне', 'было',
    'вот', 'от', 'меня', 'еще', 'нет', 'о', 'из', 'ему', 'теперь',
    'когда', 'даже', 'ну', 'вдруг', 'ли', 'если', 'уже', 'или', 'ни',
    'быть', 'был', 'была', 'были', 'это', 'для', 'при', 'над', 'об',
    'один', 'один', 'раз', 'два', 'три', 'также', 'через', 'после', 'этот'
}

def clean_text(text):
    text = text.lower()
    
    text = re.sub(r'[^а-яёa-z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def tokenize(text):
    return text.split()

def remove_stop_words(tokens):
    return [token for token in tokens if token not in STOP_WORDS]

def preprocess_text(text):

    cleaned = clean_text(text)
    tokens = tokenize(cleaned)
    tokens = remove_stop_words(tokens)
    return ' '.join(tokens)

if __name__ == '__main__':
    test_text = "Этот фильм — просто ШЕДЕВР!!! Всем рекомендую посмотреть. 10/10"
    print(f"Исходный: {test_text}")
    print(f"После обработки: {preprocess_text(test_text)}")