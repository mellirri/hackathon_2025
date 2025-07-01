import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_metrics(csv_file="benchmark_results.csv", output_file="metrics_plot.png"):
    """Строит график метрик из CSV-файла"""
    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"Файл {csv_file} не найден")
    
    df = pd.read_csv(csv_file)
    metrics = df.iloc[0].to_dict()
    
    # Подготовка данных
    names = list(metrics.keys())
    values = list(metrics.values())
    
    # Создание графика
    plt.figure(figsize=(10, 6))
    bars = plt.bar(names, values, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
    
    # Добавление значений на столбцы
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.01, 
                 f"{yval:.3f}", ha='center', va='bottom')
    
    # Настройки графика
    plt.title('Качество генерации конспектов', fontsize=14)
    plt.ylabel('Значение метрики', fontsize=12)
    plt.ylim(0, 1)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Сохранение и вывод
    plt.tight_layout()
    plt.savefig(output_file)
    print(f"График сохранен как {output_file}")
    plt.show()

if __name__ == "__main__":
    plot_metrics()