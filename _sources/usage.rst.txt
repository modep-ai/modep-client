=====
Usage
=====

Connect to the API and upload a dataset::

  from modep_client.client import Client
  from modep_client.datasets import Datasets
  
  client = Client(os.environ['MODEP_API_KEY'])
  datasets = Datasets(client)
    
  df_train = pd.read_csv('https://jgoode.s3.amazonaws.com/titanic/train.csv')
  df_test = pd.read_csv('https://jgoode.s3.amazonaws.com/titanic/test.csv')

  train_dset = datasets.upload(df_train, 'titanic_train')
  test_dset = datasets.upload(df_test, 'titanic_test')

