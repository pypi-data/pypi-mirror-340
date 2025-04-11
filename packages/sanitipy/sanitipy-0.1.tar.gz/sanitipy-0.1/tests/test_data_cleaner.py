import unittest
import pandas as pd
from sanitipy.data_cleaner import DataCleaner

class TestDataCleaner(unittest.TestCase):
  def test_remove_duplicates(self):
    data = pd.DataFrame({
      'A': [1, 1, 2, 2],
      'B': [3, 3, 4, 4]
    })
    cleaner = DataCleaner(data)
    cleaned_data = cleaner.remove_duplicates()
    
    self.assertEqual(len(cleaned_data), 2)

if __name__ == '__main__':
  unittest.main()
