import pandas as pd
from sklearn.preprocessing import StandardScaler

class Preprocessor:
  def __init__(self, data: pd.DataFrame):
    self.data = data
  
  def infer_data_types(self, df):
    for col in df.columns:
      if df[col].dtype == 'object':
        # Check for datetime columns
        try:
          pd.to_datetime(df[col], format="%Y/%m/%d")
          df[col] = pd.to_datetime(df[col], errors='coerce')
        except (ValueError, TypeError):
          pass
      
      # Fill in NaN values with the mode (mode frequent value) if applicable
      if df[col].dtype == 'object':
        df[col] = df[col].astype('string')
      elif df[col].dtype in ['float64', 'int64']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df
  
  def normalize_data(self):
    scaler = StandardScaler()
    self.data = pd.DataFrame(scaler.fit_transform(self.data), columns=self.data.columns)

    return self.data
  
  def encode_categorical(self):
    self.data = pd.get_dummies(self.data)

    return self.data
