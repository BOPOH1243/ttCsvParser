# ttCsvParser
## сделал процессор для csv
вот пример команды запуска:
```python main.py data.csv --aggregate "avg=rating" --where "price>500"```

- реализовал сам процессор в отдельный класс, ибо так мне показалось круче
- сделал простенькую заглушку main.py
- сделал тесты для всего базового функционала, в том числе добавление нового оператора для фильтрации