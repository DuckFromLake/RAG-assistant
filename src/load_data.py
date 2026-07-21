import os
from pathlib import Path
import pandas as pd
import psycopg2
from dotenv import load_dotenv

load_dotenv()
CATEGORIES = ['neg', 'neu', 'pos']

def load_reviews(base_dir):
    records = []

    for cat in CATEGORIES:
        cat_dir = Path(base_dir) / cat
        

        if not cat_dir.exists():
            print(f"Папка {cat_dir} не найдена, пропускаем")
            continue
        
        for file_path in cat_dir.glob('*.txt'):
            text = file_path.read_text(encoding='utf-8').strip()

            records.append({
                'text': text,
                'category': cat,
                'filename': file_path.name
            })
    
    return pd.DataFrame(records)


def upload_to_db(df):

    conn = psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=os.getenv('DB_PORT', '5432'),
        dbname=os.getenv('DB_NAME', 'NLPassistant'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', '1234')
    )
    
    cur = conn.cursor()
    cur.execute("TRUNCATE TABLE documents RESTART IDENTITY")
    
    for _, row in df.iterrows():
        cur.execute(
            "INSERT INTO documents (text, category, filename) VALUES (%s, %s, %s)",
            (row['text'], row['category'], row['filename'])
        )
    
    conn.commit()
    
    cur.execute("SELECT COUNT(*) FROM documents")
    count = cur.fetchone()[0]
    print(f"Загружено в БД: {count} строк")
    

    cur.close()
    conn.close()

if __name__ == '__main__':
    print("Читаем файлы...")
    df = load_reviews('data/raw/kinopoisk_reviews')
    print(f"Найдено отзывов: {len(df)}")

    print("Загружаем в базу данных...")
    upload_to_db(df)

    print("\nРаспределение по категориям:")
    print(df['category'].value_counts())