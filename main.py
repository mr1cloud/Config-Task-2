import os
import zlib
import argparse
from pathlib import Path
from datetime import datetime

import mermaid as md
from mermaid.graph import Graph


def parse_commit_data(commit_data: str) -> dict:
    """Парсинг данных коммита."""
    commit_info = {}

    commit_message = commit_data[commit_data.find('\n\n') + 2:-1]

    commit_data = commit_data.split('\n\n')[0]

    lines = commit_data.split('\n')
    for line in lines:
        if line.startswith('tree'):
            commit_info['tree'] = line.split(' ')[1]
        elif line.startswith('parent'):
            if 'parents' not in commit_info:
                commit_info['parents'] = []
            commit_info['parents'].append(line.split(' ')[1])
        elif line.startswith('author'):
            commit_info['author'] = line.split('>')[0].split(' ', 1)[1] + ">"
            commit_info['timestamp'] = int(line.split('>')[1].split(' ')[1])
        elif line.startswith('committer'):
            commit_info['committer'] = line.split(' ')[1]

    commit_info['message'] = commit_message

    if 'author' not in commit_info:
        return {}
    return commit_info


def get_branches(repo_path: str) -> dict:
    """Возвращает словарь с названиями веток и соответствующими хешами коммитов."""
    branches = {}
    branches_path = Path(repo_path) / 'refs' / 'heads'

    if branches_path.exists():
        for branch_file in os.listdir(branches_path):
            branch_path = branches_path / branch_file
            with open(branch_path, 'r') as f:
                commit_hash = f.read().strip()
                branches[branch_file] = commit_hash

    return branches


def get_commits_files(repo_path: str) -> dict:
    """Возвращает пути до файлов коммитов, которые лежат в папке objects."""
    git_objects_path = (Path(repo_path) / 'objects').resolve()
    commit_files = {}

    for root, _, files in os.walk(git_objects_path):
        for file in files:
            file_path = Path(root) / file
            file_data = file_path.read_bytes()
            data = zlib.decompress(file_data).decode('utf-8', errors='ignore')
            if 'commit' in data:
                commit_hash = root[-2:] + file_path.name
                parsed_data = parse_commit_data(data)
                if parsed_data:
                    commit_files[commit_hash] = {
                        "path": file_path,
                        "data": parse_commit_data(data)
                    }

    return commit_files


def assign_commit_to_branch(commit_hash: str, branches: dict) -> str | None:
    """Возвращает название ветки, к которой относится коммит, или None, если коммит не найден в ветках."""
    for branch, branch_commit_hash in branches.items():
        if branch_commit_hash == commit_hash:
            return branch
    return None


def get_commits_with_branches(repo_path: str, date: str) -> dict:
    """Возвращает все коммиты с их информацией и ветками."""
    branches = get_branches(repo_path)
    commit_files = get_commits_files(repo_path)
    buffer = {}

    for commit_hash, commit_data in commit_files.items():
        if datetime.fromtimestamp(commit_data['data']['timestamp']).strftime('%Y-%m-%d') < datetime.fromisoformat(date).strftime('%Y-%m-%d'):
            continue
        branch = assign_commit_to_branch(commit_hash, branches)
        commit_data["branch"] = branch
        buffer[commit_hash] = commit_data


    return buffer


def generate_mermaid_graph(commits_data: dict) -> str:
    """Генерация Mermaid графа зависимостей коммитов с развветвлениями и без дублирования."""
    graph = "graph TD\n"
    sorted_commits = list(commits_data.keys())

    commit_parents = {}
    for commit in sorted_commits:
        parents = commits_data[commit]['data'].get('parents', [])
        commit_parents[commit] = parents

    added_commits = set()

    for commit in sorted_commits:
        data = commits_data[commit]['data']
        commit_short = commit[:7]

        if commit_short in added_commits:
            continue

        commit_info = f"{data['message']}\n    {data['author']} {data['timestamp']}"

        graph += f'    {commit_short}(["`\n    Commit {commit_short}:\n    {commit_info.replace("`", "")}\n    `"])\n'

        added_commits.add(commit_short)

        for parent_commit in commit_parents[commit]:
            if parent_commit != commit:
                graph += f"    {parent_commit[:7]} --> {commit_short}\n"

    return graph


def save_mermaid_graph(graph, output_path):
    """Сохранение Mermaid графа в файл."""
    with open(output_path, 'w') as f:
        f.write(graph)
    print(f"Mermaid graph saved to {output_path}")


def convert_mermaid_to_png(graph_data: str, output_image_path: str):
    """Конвертация Mermaid графа в изображение PNG."""
    sequence = Graph(title="Git Graph", script=graph_data)
    render = md.Mermaid(sequence)
    render.to_png(output_image_path)


def main():
    parser = argparse.ArgumentParser(description="Visualize git commit dependencies in Mermaid format.")
    parser.add_argument("repo_path", help="Path to the git repository")
    parser.add_argument("date", help="Date of commits to visualize (format: YYYY-MM-DD)")
    parser.add_argument("output_path", help="Path to save the Mermaid graph file")
    parser.add_argument("output_image", help="Path to save the PNG image")

    args = parser.parse_args()

    commits_data = get_commits_with_branches(repo_path=args.repo_path, date=args.date)

    print(commits_data)

    graph = generate_mermaid_graph(commits_data=commits_data)
    save_mermaid_graph(graph=graph, output_path=args.output_path)
    convert_mermaid_to_png(graph_data=graph, output_image_path=args.output_image)


if __name__ == "__main__":
    main()
