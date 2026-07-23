import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

import joblib
from src.text_preprocessing import preprocess_text


def predict_sentiment(text):
    vectorizer = joblib.load(str(project_root) + '/models/tfidf_vectorizer_v1.pkl')
    model = joblib.load(str(project_root) + '/models/logreg_v1.pkl')
    
    clean = preprocess_text(text)
    X = vectorizer.transform([clean])
    
    pred = model.predict(X)[0]
    proba = model.predict_proba(X)[0]
    
    result = f"Предсказание: {pred}\n"
    result += f"Вероятности: neg={proba[0]:.3f}, neu={proba[1]:.3f}, pos={proba[2]:.3f}"
    
    return result


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Использование: python src/predict.py 'текст отзыва'")
        sys.exit(1)
    
    text = sys.argv[1]
    print(predict_sentiment(text))