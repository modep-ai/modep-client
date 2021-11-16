#!/usr/bin/env python

"""Tests for `modep_client` package."""

import logging
import os
import pandas as pd
import pytest
import time
import uuid

from modep_client.client import Client
from modep_client.datasets import Datasets
from modep_client.automl import Frameworks, FrameworkFlights

logger = logging.getLogger(__name__)


@pytest.fixture
def client():
    client = Client(os.environ['MODEP_API_KEY'])
    return client


def test_datasets(client):
    datasets = Datasets(client)
    
    df_train = pd.read_csv('https://jgoode.s3.amazonaws.com/titanic/train.csv')
    df_test = pd.read_csv('https://jgoode.s3.amazonaws.com/titanic/test.csv')

    id = str(uuid.uuid4())[:5]
    train_name = f'titanic_train_{id}'
    test_name = f'titanic_test_{id}'

    train_dset = datasets.upload(df_train, train_name)
    test_dset = datasets.upload(df_test, test_name)
    dsets = datasets.list()
    assert train_name in dsets.name.values
    assert test_name in dsets.name.values
    train_id = dsets[dsets.name == train_name].index[0]
    test_id = dsets[dsets.name == test_name].index[0]

    datasets.delete(train_id)
    datasets.delete(test_id)
    dsets = datasets.list()
    assert train_name not in dsets.name.values
    assert test_name not in dsets.name.values


def test_train(client):
    datasets = Datasets(client)    
    frameworks = Frameworks(client)
    flights = FrameworkFlights(client)
    
    df_train = pd.read_csv('https://jgoode.s3.amazonaws.com/titanic/train.csv')
    df_test = pd.read_csv('https://jgoode.s3.amazonaws.com/titanic/test.csv')

    id = str(uuid.uuid4())[:5]
    train_name = f'titanic_train_{id}'
    test_name = f'titanic_test_{id}'

    train_dset = datasets.upload(df_train, train_name)
    test_dset = datasets.upload(df_test, test_name)
    dsets = datasets.list()
    assert train_name in dsets.name.values
    assert test_name in dsets.name.values
    train_id = dsets[dsets.name == train_name].index[0]
    test_id = dsets[dsets.name == test_name].index[0]

    flight_job = flights.train(['constantpredictor'], train_id, test_id, 'survived', 60)
    flight = flight_job.result()
    logger.info(flight)

    assert flight['status'] == 'SUCCESS'
    
    datasets.delete(train_id)
    datasets.delete(test_id)
    dsets = datasets.list()
    assert train_name not in dsets.name.values
    assert test_name not in dsets.name.values