import os
import subprocess
import argparse
from datetime import datetime

import mermaid as md
from mermaid.graph import Graph


def get_commit_dependencies(repo_path: str, date_str: str) -> dict:
    date_limit = datetime.strptime(date_str, "%Y-%m-%d")

    git_log_command = [
        'git', '-C', repo_path, 'log', '--pretty=format:%H %ct %an %s', '--since', date_str
    ]

    result = subprocess.run(git_log_command, capture_output=True, text=True, check=True)
    commits = result.stdout.splitlines()

    dependencies = {}

    for commit in commits:
        commit_hash, commit_time, commit_author, commit_message = commit.split(' ', 3)
        commit_time = datetime.fromtimestamp(int(commit_time)).strftime("%Y-%m-%d %H:%M:%S")

        git_diff_command = [
            'git', '-C', repo_path, 'diff', '--name-only', commit_hash + '^!'
        ]
        result = subprocess.run(git_diff_command, capture_output=True, text=True)
        changed_files = result.stdout.splitlines()

        dependencies[commit_hash] = {
            "files": changed_files,
            "author": commit_author,
            "time": commit_time,
            "message": commit_message
        }

    return dependencies


def generate_mermaid_graph(dependencies):
    graph = "graph TD\n"
    sorted_commits = list(dependencies.keys())

    for idx, commit in enumerate(sorted_commits):
        data = dependencies[commit]
        commit_short = commit[:7]
        files_str = " & ".join(data["files"]) if data["files"] else "No changes"
        commit_info = f"{commit_short}:\n    {data['message']}\n    {data['author']} {data['time']}"

        graph += f'    {commit_short}(["`\n    Commit {commit_info}:\n    {files_str}\n    `"])\n'

        if idx > 0:
            prev_commit = sorted_commits[idx - 1]
            graph += f"    {prev_commit[:7]} --> {commit_short}\n"

    return graph


def save_mermaid_graph(graph, output_path):
    with open(output_path, 'w') as f:
        f.write(graph)
    print(f"Mermaid graph saved to {output_path}")


def convert_mermaid_to_png(graph_data: str, output_image_path: str):
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

    dependencies = get_commit_dependencies(repo_path=args.repo_path, date_str=args.date)

    print(dependencies)

    graph = generate_mermaid_graph(dependencies=dependencies)

    save_mermaid_graph(graph=graph, output_path=args.output_path)
    convert_mermaid_to_png(graph_data=graph, output_image_path=args.output_image)


if __name__ == "__main__":
    main()
