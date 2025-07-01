import argparse
import pandas as pd
from evaluate import load
from pdfminer.high_level import extract_text as extract_text_pdf
import docx2txt
import os
import sys


def convert_to_txt(input_path, output_path):
    """Конвертирует docx/pdf в текстовый файл"""
    if input_path.endswith('.docx'):
        text = docx2txt.process(input_path)
    elif input_path.endswith('.pdf'):
        text = extract_text_pdf(input_path)
    else:
        # Если файл уже текстовый
        with open(input_path, 'r', encoding='utf-8') as f:
            text = f.read()

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)
    return output_path


def main():
    parser = argparse.ArgumentParser(description='Оценка качества генерации конспектов')
    parser.add_argument('--reference', type=str, help='Путь к эталонному файлу (docx/pdf/txt)')
    parser.add_argument('--generated', type=str, help='Путь к сгенерированному файлу (docx/pdf/txt)')
    parser.add_argument('--output_csv', type=str, default='benchmark_results.csv',
                        help='Путь для сохранения результатов CSV')

    args = parser.parse_args()

    # Проверяем наличие файлов по умолчанию, если аргументы не переданы
    default_files = {
        'reference': 'reference.pdf',
        'generated': 'generated.docx'
    }

    if not args.reference:
        if os.path.exists(default_files['reference']):
            args.reference = default_files['reference']
            print(f"Используется файл по умолчанию: {args.reference}")
        else:
            print("Ошибка: Не указан --reference и не найден файл reference.docx")
            sys.exit(1)

    if not args.generated:
        if os.path.exists(default_files['generated']):
            args.generated = default_files['generated']
            print(f"Используется файл по умолчанию: {args.generated}")
        else:
            print("Ошибка: Не указан --generated и не найден файл generated.docx")
            sys.exit(1)

    # Конвертация файлов в текст
    ref_txt = convert_to_txt(args.reference, "reference.txt")
    gen_txt = convert_to_txt(args.generated, "generated.txt")
    print(f"Файлы конвертированы в текст: {ref_txt}, {gen_txt}")

    # Чтение текстовых файлов
    with open(ref_txt, encoding="utf-8") as f:
        reference = f.read()

    with open(gen_txt, encoding="utf-8") as f:
        prediction = f.read()

    # ROUGE (лексическое совпадение)
    print("\nВычисление ROUGE метрик...")
    rouge = load("rouge")
    r = rouge.compute(predictions=[prediction],
                      references=[reference],
                      use_stemmer=True)

    # BERTScore (семантическое совпадение)
    print("Вычисление BERTScore...")
    bertscore = load("bertscore")
    b = bertscore.compute(predictions=[prediction],
                          references=[reference],
                          lang="ru")

    # Сбор результатов
    results = {
        "ROUGE-1": r["rouge1"],
        "ROUGE-2": r["rouge2"],
        "ROUGE-L": r["rougeL"],
        "BERTScore F1": b["f1"][0]
    }

    # Вывод в консоль
    print("\n=== Результаты ===")
    for metric, value in results.items():
        print(f"{metric}: {value:.4f}")

    # Сохранение в CSV
    df = pd.DataFrame([results])
    df.to_csv(args.output_csv, index=False)
    print(f"\nРезультаты сохранены в {args.output_csv}")


if __name__ == "__main__":
    main()