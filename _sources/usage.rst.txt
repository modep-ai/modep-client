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


Train all tabular models on the dataset for a max of 30 minutes each::
    
  from modep_client.automl import FrameworkFlights

  flights = FrameworkFlights(client)

  frameworks = [
     'AutoGluon',
     'AutoGluon_bestquality',
     'autosklearn',
     'autosklearn2',
     'AutoWEKA',
     'constantpredictor',
     'DecisionTree',
     'flaml',
     'GAMA',
     'H2OAutoML',
     'hyperoptsklearn',
     'mljarsupervised',
     'mljarsupervised_compete',
     'MLNet',
     'RandomForest',
     'TPOT',
     'TunedRandomForest',
  ]

  # starts the training
  flight_job = flights.train(frameworks, train_dset['id'], test_dset['id'], 'survived', 60*30)

  # waits for training to complete
  flight = flight_job.result()

  
