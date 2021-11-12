import logging
import pandas as pd
from typing import Union, List

from modep_client.client import Client
from modep_client.tasks import BaseTask

logger = logging.getLogger(__name__)


class Frameworks:
    def __init__(self, client: Client):
        """
        Initialize the Framworks class

        :param client: A :class:`modep_client.client.Client` object
        """
        self.client = client

    def info(self):
        """
        Get info about the AutoML frameworks available through the API

        :return: A :class:`pandas.DataFrame` with one row for each framework
        """
        url = self.client.url + "frameworks/tabular/info"
        resp = self.client.sess.get(url, headers=self.client.auth_header())
        if resp.ok:
            js = resp.json()
            df = pd.DataFrame(js)
            if len(df) > 0:
                # keep column order same as json
                df = df[list(js[0].keys())].set_index("framework_name")
            return df
        else:
            self.client.response_exception(resp)        

    def list(self):
        """
        List all AutoML framework training runs

        :return: A :class:`pandas.DataFrame` with one row for each training run
        """
        url = self.client.url + "frameworks/tabular"
        resp = self.client.sess.get(url, headers=self.client.auth_header())
        if resp.ok:
            js = resp.json()
            df = pd.DataFrame(js)
            if len(df) > 0:
                # keep column order same as json
                df = df[list(js[0].keys())].set_index("id")
                df = df.sort_values(by="created", ascending=False)
            return df
        else:
            self.client.response_exception(resp)

    def train(
        self,
        framework_name: str,
        train_ids: Union[str, List[str]],
        test_ids: Union[str, List[str]],
        target: str,
        max_runtime_seconds: int,
    ):
        """
        Train an AutoML framework

        :param str framework_name: The name of the framework (ie. AutoGluon, AutoGluon_bestquality,
            autosklearn, autosklearn2, AutoWEKA, constantpredictor, DecisionTree, flaml, GAMA, H2OAutoML,
            hyperoptsklearn, mljarsupervised, mljarsupervised_compete, MLNet, RandomForest, TPOT, TunedRandomForest)
        :param train_ids: The id(s) of dataset(s) to train on (ie. `e1bc3d16b-6d67-43cd-af59-8d39d8cb2a02`)
        :param test_ids: The id(s) of dataset(s) to test on (ie. `1bc3d16b-6d67-43cd-af59-8d39d8cb2a02`)
        :param str target: The name of the target column in the training dataset(s)
        :param int max_runtime_seconds: The maximum amount of time in seconds to train per dataset(s)
        """

        url = self.client.url + "frameworks/tabular"

        train_ids = [train_ids] if isinstance(train_ids, str) else train_ids
        test_ids = [test_ids] if isinstance(test_ids, str) else test_ids

        data = dict(
            framework_name=framework_name,
            train_ids=train_ids,
            test_ids=test_ids,
            target=target,
            max_runtime_seconds=max_runtime_seconds,
            experiment_id="",
        )
        logger.info(data)

        resp = self.client.sess.post(url, json=data, headers=self.client.auth_header())
        if resp.ok:
            return BaseTask(resp.json(), self.get)
        else:
            self.client.response_exception(resp)

    def get(self, id: str):
        """
        Get an AutoML training run by id
        
        :param str id: The id of the training run
        :return: A dictionary containing the training run
        """
        url = self.client.url + "frameworks/tabular/" + str(id)
        resp = self.client.sess.get(url, headers=self.client.auth_header())
        if resp.ok:
            return resp.json()
        else:
            self.client.response_exception(resp)

    def stop(self, id):
        """
        Stop an AutoML training run

        :param str id: The id of the training run to stop
        :return: A dictionary containing the training run
        """
        url = self.client.url + f"frameworks/tabular/{id}/stop"
        resp = self.client.sess.get(url, headers=self.client.auth_header())
        if resp.ok:
            return resp.json()
        else:
            self.client.response_exception(resp)

    def delete(self, id):
        """
        Delete an AutoML training run

        :param str id: The id of the training run to delete
        :return: A dictionary containing info about the deletion
        """
        url = self.client.url + "frameworks/tabular/" + str(id)
        resp = self.client.sess.delete(url, headers=self.client.auth_header())
        if resp.ok:
            return resp.json()
        else:
            self.client.response_exception(resp)

    def predict(self, framework_id, dataset_id):
        """
        Start a job to get predictions from an AutoML framework on a new dataset

        :param str framework_id: The id of the framework to use
        :param str dataset_id: The id of the dataset to predict on
        """
        url = self.client.url + "frameworks/tabular/predict"

        data = dict(
            framework_id=framework_id,
            dataset_id=dataset_id,
        )

        resp = self.client.sess.post(url, json=data, headers=self.client.auth_header())
        if resp.ok:
            return BaseTask(resp.json(), self.get_predictions)
        else:
            self.client.response_exception(resp)

    def get_predictions(self, predictions_id):
        """
        Get the predictions created by an AutoML training or prediction job

        :param str predictions_id: The id of the predictions to get
        :return: A dictionary containing the predictions
        """
        url = self.client.url + f"frameworks/tabular/predictions/{predictions_id}"
        resp = self.client.sess.get(url, headers=self.client.auth_header())
        if resp.ok:
            return resp.json()
        else:
            self.client.response_exception(resp)

    def output(self, id, target_dir):
        url = self.client.url + f"frameworks/tabular/{id}/output"
        resp = self.client.sess.get(url, headers=self.client.auth_header())
        if resp.ok:
            # download contents to directory
            z = zipfile.ZipFile(io.BytesIO(resp.content))
            z.extractall(path=target_dir)
            return resp
        else:
            self.client.response_exception(resp)

