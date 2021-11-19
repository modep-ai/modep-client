import fire
import logging
import os
import openml as oml
from openml import datasets
import pandas as pd

from modep_client.automl import FrameworkFlights
from modep_client.client import Client
from modep_client.datasets import Datasets


logger = logging.getLogger(__name__)

# The OpenML AutoML Benchmark (39 tasks)
# https://www.openml.org/s/218/tasks/
TASK_IDS = [
    3945,
    7593,
    9952,
    9977,
    9981,
    14965,
    34539,
    167119,
    168908,
    168909,
    168910,
    168911,
    168912,
    146212,
    146195,
    168868,
    146818,
    146821,
    146822,
    146825,
    146606,
    168329,
    168330,
    168331,
    168332,
    168335,
    168337,
    168338,
    189354,
    189355,
    189356,
    167120,
    10101,
    7592,
    3,
    31,
    53,
    12,
    3917,
]


def upload(max_folds=1, task_ids=TASK_IDS):

    client = Client(os.environ["MODEP_API_KEY"])
    datasets = Datasets(client)

    print(datasets.list())
    for idx in datasets.list().index:
        print(datasets.delete(idx))

    tasks = []
    for task_id in task_ids:

        task = oml.tasks.get_task(task_id, download_qualities=False)
        dataset = oml.datasets.get_dataset(task.dataset_id, download_qualities=False)

        n_repeats, n_folds, n_samples = task.get_split_dimensions()
        if n_repeats != 1 or n_samples != 1:
            raise NotImplementedError(f"n_samples: {n_samples}, n_repeats: {n_repeats}")

        print(task)
        print(dataset)

        target = task.target_name
        categorical_target = hasattr(task, "class_labels")

        X, y = task.get_X_and_y(dataset_format="dataframe")

        df = pd.concat((X, y), 1)

        if max_folds is None:
            max_folds = n_folds

        for fold in range(max_folds):

            train_indices, test_indices = task.get_train_test_split_indices(
                repeat=0, fold=fold, sample=0
            )

            df_train = df.iloc[train_indices]
            df_test = df.iloc[test_indices]

            train_name = (
                f"OpenML-{task_id}-name={dataset.name}-fold={fold:02d}-split=train"
            )
            test_name = (
                f"OpenML-{task_id}-name={dataset.name}-fold={fold:02d}-split=test"
            )

            train_dset = datasets.upload(
                df_train,
                train_name,
                target=target,
                categorical_target=categorical_target,
            )
            test_dset = datasets.upload(
                df_test, test_name, target=target, categorical_target=categorical_target
            )

            print(train_dset)
            print(test_dset)


def train(task_ids=TASK_IDS, max_runtime_seconds=60 * 5):

    client = Client(os.environ["MODEP_API_KEY"])
    datasets = Datasets(client)
    flights = FrameworkFlights(client)

    dsets = datasets.list()
    print(dsets)
    print("task_ids", task_ids)

    for task_id in task_ids:
        dsets_ = dsets[dsets["name"].str.contains(f"OpenML-{task_id}")]
        print(dsets_)
        train_dset = dsets_[dsets_["name"].str.contains("split=train")]
        test_dset = dsets_[dsets_["name"].str.contains("split=test")]
        assert len(train_dset) == 1 and len(test_dset) == 1, task_id
        train_id = train_dset.index[0]
        test_id = test_dset.index[0]
        target = train_dset.iloc[0]["target"]

        flight_task = flights.train(
            ["constantpredictor"], train_id, test_id, target, max_runtime_seconds
        )
        flight_id = flight_task.response["id"]
        flights.wait_terminal(flight_id)


if __name__ == "__main__":
    fire.Fire()
