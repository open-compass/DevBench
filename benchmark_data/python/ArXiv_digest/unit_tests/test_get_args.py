import unittest
from query_arxiv import get_args

class TestGetArgs(unittest.TestCase):
    def test_missing_required_arguments(self) -> None:
        """
        Missing required arguments should result in SystemExit(2).
        """
        with self.assertRaises(SystemExit) as cm:
            get_args([])
        self.assertEqual(cm.exception.code, 2)

    
    def test_all_required_arguments_present(self) -> None:
        """
        Test whether all required arguments are present.
        """
        args = get_args(['--recent_days', '3'])
        self.assertEqual(args.recent_days, 3)
    
    
    def test_override_args(self) -> None:
        '''
        Test whether args are overriden correctly. 
        '''
        args = get_args([
            '--category', 'cs.CL',
            '--title', 'Neural+Networks',
            '--author', 'Smith',
            '--abstract', 'Deep+Learning',
            '--max_results', '20',
            '--recent_days', '30',
            '--to_file', 'results.csv',
            '--verbose'
        ])
        self.assertEqual(args.category, 'cs.CL')
        self.assertEqual(args.title, 'Neural+Networks')
        self.assertEqual(args.author, 'Smith')
        self.assertEqual(args.abstract, 'Deep+Learning')
        self.assertEqual(args.max_results, 20)
        self.assertEqual(args.recent_days, 30)
        self.assertEqual(args.to_file, 'results.csv')
        self.assertTrue(args.verbose)

    def test_defaults_only_recent_days(self) -> None:
        args = get_args([
            '--recent_days', '30'
        ])

        self.assertIsNone(args.category)
        self.assertIsNone(args.title)
        self.assertIsNone(args.author)
        self.assertIsNone(args.abstract)
        self.assertEqual(args.max_results, 10)
        self.assertEqual(args.recent_days, 30)
        self.assertEqual(args.to_file, "")
        self.assertFalse(args.verbose)