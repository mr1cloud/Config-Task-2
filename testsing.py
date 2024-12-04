import unittest
from main import get_commit_dependencies, generate_mermaid_graph


class MyTestCase(unittest.TestCase):
    def test_get_commit_dependencies(self):
        dependencies = get_commit_dependencies('./data', '2024-11-06')
        self.assertIn('092270dd4feec0641fff990c991018e49662ce44', dependencies)
        self.assertIn('406d18d010dd618a3e32f4cf7ad2e8d8a4324a44', dependencies)
        self.assertIn('01f14b4159f512481c53a1ef8af143f3c293f45b', dependencies)

    def test_generate_mermaid_graph(self):
        dependencies = get_commit_dependencies('./data', '2024-11-06')
        graph = generate_mermaid_graph(dependencies=dependencies)
        self.assertIn('graph TD', graph)
        self.assertIn('092270d', graph)
        self.assertIn('406d18d', graph)
        self.assertIn('01f14b4', graph)

    def test_generate_mermaid_graph_empty(self):
        dependencies = get_commit_dependencies('./data', '2024-11-08')
        graph = generate_mermaid_graph(dependencies=dependencies)
        self.assertEqual(graph, 'graph TD\n')


if __name__ == '__main__':
    unittest.main()
