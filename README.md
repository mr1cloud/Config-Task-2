# Визуализатор Git зависимостей графа

Цель: Разработать инструмент командной строки для анализа и визуализации графа зависимостей коммитов в git-репозитории. Граф строится для всех коммитов до указанной даты, отображая файлы и папки, измененные в каждом коммите. Для описания графа используется формат Mermaid с возможностью графического отображения результата.

## Требования:
- Для визуализация трафа использовать Mermaid
- Анализируемый git-репозиторий должен быть доступен локально.

# Реализация функций:
1. **`get_commit_dependencies`**: Извлекает информацию о коммитах в указанном git-репозитории, которые были созданы начиная с указанной даты. Для каждого коммита собираются метаданные и измененные файлы.
2. **`generate_mermaid_graph`**: Генерирует Mermaid-скрипт для визуализации графа зависимостей на основе переданных данных о коммитах.
3. **`save_mermaid_graph`**: Сохраняет Mermaid-скрипт в файл.
4. **`convert_mermaid_to_png`**: Конвертирует Mermaid-скрипт в изображение формата PNG.
5. **`main`**: Основная функция, выполняющая следующий алгоритм:

## Функции реализованные для тестирование:
### 1) Проверяет, что функция корректно возвращает зависимости коммитов для указанного репозитория и даты.
```python
def test_get_commit_dependencies(self):
    dependencies = get_commit_dependencies('./data', '2024-11-06')
    self.assertIn('092270dd4feec0641fff990c991018e49662ce44', dependencies)
    self.assertIn('406d18d010dd618a3e32f4cf7ad2e8d8a4324a44', dependencies)
    self.assertIn('01f14b4159f512481c53a1ef8af143f3c293f45b', dependencies)
```

### 2) Проверяет, что функция корректно формирует граф в формате Mermaid на основе данных о зависимостях.
```python
def test_generate_mermaid_graph(self):
    dependencies = get_commit_dependencies('./data', '2024-11-06')
    graph = generate_mermaid_graph(dependencies=dependencies)
    self.assertIn('graph TD', graph)
    self.assertIn('092270d', graph)
    self.assertIn('406d18d', graph)
    self.assertIn('01f14b4', graph)
```

### 3) Проверяет корректность обработки случая, когда для заданной даты нет подходящих коммитов.
```python
def test_generate_mermaid_graph_empty(self):
    dependencies = get_commit_dependencies('./data', '2024-11-08')
    graph = generate_mermaid_graph(dependencies=dependencies)
    self.assertEqual(graph, 'graph TD\n')
```


## Результаты тестирование: