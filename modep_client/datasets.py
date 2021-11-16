import copy
import logging
import os
import pandas as pd
import tempfile
from typing import Union
from requests_toolbelt import MultipartEncoder

from modep_client.client import Client

logger = logging.getLogger(__name__)


class Datasets:
    def __init__(self, client: Client):
        """
        Initialize the Datasets class

        :param client: A :class:`modep_client.client.Client` object
        """
        self.client = client

    def upload(self,
               dset: Union[str, pd.DataFrame],
               name: str,
               target: str = None,
               categorical_target: bool = True,
               ):
        """
        Upload a tabular dataset.

        :param dset: either a path to a CSV file or DataFrame containing the data
        :type dset: str or :class:`pandas.DataFrame`
        :param str name: A name to give the dataset (ie. `titanic-train` or `titanic-test`)
        :param target: Optionally specify a target column for the dataset
        :type target: str or None
        :param bool categorical_target: `True` if the specified `target` column is categorical
            (for classification), otherwise set this to `False` for regression.
        """

        if isinstance(dset, str):
            path = dset
            if not os.path.exists(path):
                raise Exception(f"Path does not exist: '{path}'")
        elif isinstance(dset, pd.DataFrame):
            path = tempfile.NamedTemporaryFile(suffix="-df-upload").name + ".csv"
            logger.info("Writing DataFrame to %s", path)
            dset.to_csv(path, index=False)
        else:
            raise ValueError(
                "Unknown type for dataset, "
                "must be either string path or pd.DataFrame"
            )
        logger.info("Uploading from %s", path)

        url = self.client.url + "datasets/tabular"
        # deepcopy since we update headers below
        headers = copy.deepcopy(self.client.auth_header())

        with open(path, "rb") as f:
            data = MultipartEncoder(
                {
                    "path": os.path.abspath(path),
                    "name": name,
                    "file": (path, f, "text/csv/h5"),
                    "target": target,
                    "categorical_target": str(categorical_target),
                }
            )
            headers.update(
                {"Prefer": "respond-async", "Content-Type": data.content_type}
            )
            resp = self.client.sess.post(url, data=data, headers=headers)
        if resp.ok:
            return resp.json()
        else:
            self.client.response_exception(resp)

    def get(self, id: str):
        """
        Get a dataset by id.

        :param str id: The id of the dataset
        :return: A dictionary for the dataset
        """
        url = self.client.url + "datasets/tabular/" + str(id)
        resp = self.client.sess.get(url, headers=self.client.auth_header())
        if resp.ok:
            return resp.json()
        else:
            self.client.response_exception(resp)

    def list(self):
        """
        List all datasets.

        :return: A list of dictionaries for each uploaded or public dataset
        """
        url = self.client.url + "datasets/tabular"
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

    def delete(self, dataset_id):
        """
        Delete a dataset by id.

        :param str id: The id of the dataset
        :return: A dictionary containing information on the deletion
        """
        url = self.client.url + "datasets/tabular/" + str(dataset_id)
        resp = self.client.sess.delete(url, headers=self.client.auth_header())
        if resp.ok:
            return resp.json()
        else:
            self.client.response_exception(resp)            
