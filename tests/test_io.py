import io
import unittest
from communityreach.io import read_activities


class CSVTests(unittest.TestCase):
    def test_valid_and_overlap(self):
        data = 'name,cost,beneficiaries\nFood,100,H1;H2;H2\nWater,80,H2;H3\n'
        items = read_activities(io.StringIO(data))
        self.assertEqual(len(items), 2)
        self.assertEqual(len(items[0].people), 2)
    def test_invalid_files(self):
        bad = [
            '', 'foo,bar\nX,3\n', 'name,cost,beneficiaries\n',
            'name,cost,beneficiaries\nA,abc,H1\n',
            'name,cost,beneficiaries\nA,0,H1\n',
            'name,cost,beneficiaries\nA,4,\n',
            'name,cost,beneficiaries\n,4,H1\n',
            'name,cost,beneficiaries\nA,4,H1\nA,5,H2\n',
            'name,cost,beneficiaries\nA,4,H1,extra\n',
            'name,cost,beneficiaries\nA,4\n',
        ]
        for sample in bad:
            with self.subTest(sample=sample):
                with self.assertRaises(ValueError):
                    read_activities(io.StringIO(sample))


if __name__ == '__main__':
    unittest.main()
