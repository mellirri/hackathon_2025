import os
import argparse
import docx2txt
from pdfminer.high_level import extract_text

def convert_file(input_path, output_path):
    """Конвертирует файл в текстовый формат"""
    if input_path.endswith('.docx'):
        text = docx2txt.process(input_path)
    elif input_path.endswith('.pdf'):
        text = extract_text(input_path)
    else:
        raise ValueError("Поддерживаются только DOCX и PDF форматы")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)
    return output_path

def main():
    parser = argparse.ArgumentParser(description='Конвертация DOCX/PDF в TXT')
    parser.add_argument('input', help='Входной файл (docx/pdf)')
    parser.add_argument('output', help='Выходной файл (txt)')
    
    args = parser.parse_args()
    
    try:
        result = convert_file(args.input, args.output)
        print(f"Файл успешно конвертирован: {result}")
    except Exception as e:
        print(f"Ошибка конвертации: {str(e)}")

if __name__ == "__main__":
    main()