# Визуализатор Git зависимостей графа

Цель: Разработать инструмент командной строки для анализа и визуализации графа зависимостей коммитов в git-репозитории. Граф строится для всех коммитов до указанной даты, отображая файлы и папки, измененные в каждом коммите. Для описания графа используется формат Mermaid с возможностью графического отображения результата.

## Требования:
- Для визуализация трафа использовать Mermaid
- Анализируемый git-репозиторий должен быть доступен локально.

## Тестирование:
![graph.png](graph.png)

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
    commits_data = get_commits_with_branches('./.git', '2024-12-04')
    self.assertLess(5, len(commits_data))
```
### Результат:
![image](https://github.com/user-attachments/assets/f0012471-61e3-4b2e-9947-a8ed2341e982)


### 2) Проверяет, что функция корректно формирует граф в формате Mermaid на основе данных о зависимостях.
```python
def test_generate_mermaid_graph(self):
    commits_data = get_commits_with_branches('./.git', '2024-12-04')
    graph = generate_mermaid_graph(commits_data=commits_data)
    self.assertIn('graph TD', graph)
    self.assertIn('195271e', graph)
    self.assertIn('16acffc', graph)
    self.assertIn('2a79789', graph)
```
### Результат:
![image](https://github.com/user-attachments/assets/46601ebc-0800-4b69-b86d-9c6516cc1c39)


### 3) Проверяет корректность обработки случая, когда для заданной даты нет подходящих коммитов.
```python
def test_generate_mermaid_graph_empty(self):
    commits_data = get_commits_with_branches('./.git', '2024-12-07')
    graph = generate_mermaid_graph(commits_data=commits_data)
    self.assertEqual(graph, 'graph TD\n')
```
### Результат:
![image](https://github.com/user-attachments/assets/2e4ea4a5-e50e-4300-91a8-403a77e4094b)


## Результаты тестирование:
![image](https://github.com/user-attachments/assets/b1bcec07-5e43-42fd-a738-b98f2430dbaf)
