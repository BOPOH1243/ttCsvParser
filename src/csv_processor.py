import argparse
import csv
from tabulate import tabulate
from typing import List, Dict, Callable, Any, Optional


class CSVProcessor:
    """Класс для обработки CSV-файлов с поддержкой фильтрации и агрегации."""

    OPERATORS: Dict[str, Callable[[Any, Any], bool]] = {
        ">": lambda a, b: a > b,
        "<": lambda a, b: a < b,
        "=": lambda a, b: a == b,
    }

    AGGREGATIONS: Dict[str, Callable[[List[float]], float]] = {
        "avg": lambda x: sum(x) / len(x),
        "min": lambda x: min(x),
        "max": lambda x: max(x),
    }

    def __init__(self, file_path: str):
        """Инициализация процессора CSV-файла.

        Args:
            file_path (str): Путь к CSV-файлу.
        """
        self.file_path = file_path
        self.data: List[Dict[str, Any]] = []
        self.headers: List[str] = []
        self._load_csv()

    def _load_csv(self) -> None:
        """Загружает данные из CSV-файла."""
        with open(self.file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            self.headers = reader.fieldnames or []
            self.data = [row for row in reader]

    def filter_data(self, condition: str) -> List[Dict[str, Any]]:
        """Фильтрует данные по условию.

        Args:
            condition (str): Условие фильтрации в формате "column=value".

        Returns:
            List[Dict[str, Any]]: Отфильтрованные данные.
        """
        if not condition:
            return self.data

        column, operator, value = self._parse_condition(condition)
        filtered_data = []
        for row in self.data:
            try:
                row_value = row[column]
                try:
                    row_value = float(row_value) if "." in row_value else int(row_value)
                    value_parsed = float(value) if "." in value else int(value)
                except ValueError:
                    value_parsed = value
                if self.OPERATORS[operator](row_value, value_parsed):
                    filtered_data.append(row)
            except KeyError:
                continue
            except TypeError:
                raise TypeError("условие фильтрации некорректно")
        return filtered_data

    def _parse_condition(self, condition: str) -> tuple[str, str, str]:
        """Парсит условие фильтрации.

        Args:
            condition (str): Условие в формате "column=value"/"column<value".

        Returns:
            tuple[str, str, str]: Колонка, оператор, значение.
        """
        operators = sorted(self.OPERATORS.keys(), key=lambda x: -len(x))
        for op in operators:
            if op in condition:
                column, value = condition.split(op, 1)
                return column.strip(), op, value.strip()
        raise ValueError(f"неправильный оператор: {condition}")

    def aggregate_data(
        self, data: List[Dict[str, Any]], aggregation: str, column: str
    ) -> Optional[float]:
        """Агрегирует данные по указанной колонке.

        Args:
            data (List[Dict[str, Any]]): Данные для агрегации.
            aggregation (str): Тип агрегации (avg, min, max).
            column (str): Колонка для агрегации.

        Returns:
            Optional[float]: Результат агрегации или None, если данные пусты.
        """
        if not data:
            return None

        values = []
        for row in data:
            try:
                value = float(row[column])
                values.append(value)
            except (KeyError, ValueError):
                continue

        if not values:
            return None

        return self.AGGREGATIONS[aggregation](values)


def parse_args() -> argparse.Namespace:
    """парсит аргументы командной строки.

    Returns:
        argparse.Namespace: спаршеные аргументы.
    """
    parser = argparse.ArgumentParser(description="Process CSV file with filtering and aggregation.")
    parser.add_argument("file_path", help="Path to the CSV file")
    parser.add_argument("--where", help="Filter condition (e.g., 'price>1000')", default="")
    parser.add_argument("--aggregate", help="Aggregation (e.g., 'avg=price')", default="")
    return parser.parse_args()


def main() -> None:
    """Основная функция скрипта."""
    args = parse_args()
    processor = CSVProcessor(args.file_path)

    #добавление нового оператора для фильтрации 
    processor.OPERATORS['<=']=lambda a, b: a <= b
    #FIXME надо добавить проверку валидности чисел
    filtered_data = processor.filter_data(args.where)

    if args.aggregate:
        aggregation, column = args.aggregate.split("=", 1)
        result = processor.aggregate_data(filtered_data, aggregation, column)
        if result is not None:
            print(f"{aggregation}({column}) = {result}")
        else:
            print("No data to aggregate")
    else:
        print(tabulate(filtered_data, headers="keys", tablefmt="grid"))


if __name__ == "__main__":
    main()