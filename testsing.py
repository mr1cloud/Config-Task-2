import unittest
from main import get_commits_with_branches, generate_mermaid_graph


class MyTestCase(unittest.TestCase):
    def test_get_commit_dependencies(self):
        commits_data = get_commits_with_branches('./.git', '2024-12-04')
        self.assertLess(5, len(commits_data))

    def test_generate_mermaid_graph(self):
        commits_data = get_commits_with_branches('./.git', '2024-12-04')
        graph = generate_mermaid_graph(commits_data=commits_data)
        self.assertIn('graph TD', graph)
        self.assertIn('195271e', graph)
        self.assertIn('16acffc', graph)
        self.assertIn('2a79789', graph)

    def test_generate_mermaid_graph_empty(self):
        commits_data = get_commits_with_branches('./.git', '2024-12-07')
        graph = generate_mermaid_graph(commits_data=commits_data)
        self.assertEqual(graph, 'graph TD\n')


if __name__ == '__main__':
    unittest.main()
