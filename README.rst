============
modep-client
============
.. image:: https://github.com/modep-ai/modep-client/actions/workflows/docs.yml/badge.svg
           :target: https://modep-ai.github.io/modep-client
.. image:: https://github.com/modep-ai/modep-client/actions/workflows/tests.yml/badge.svg
        :target: https://github.com/modep-ai/modep-client/actions		    
.. image:: https://img.shields.io/pypi/v/modep-client.svg
        :target: https://pypi.org/project/modep-client

Python client for the modep API. Run flights of AutoML frameworks and compare them all:

- `AutoGluon <https://auto.gluon.ai/>`_: Amazons's version of AutoML with lots of stacking
- `auto-sklearn <https://www.automl.org/automl/auto-sklearn/>`_: automatic sklearn pipelines from NIPS 2015
- `auto-sklearn 2 <https://www.automl.org/auto-sklearn-2-0-the-next-generation/>`_: new version for 2020 that added portfolios
- `Auto-WEKA <https://www.cs.ubc.ca/labs/beta/Projects/autoweka/>`_: a JAR if you're into that
- `FLAML <https://github.com/microsoft/FLAML/>`_: Microsoft's version of AutoML - Fast and Lightweight AutoML
- `GAMA <https://github.com/PGijsbers/gama/>`_: AutoML project from OpenML, from the authors of the AutoML benchmarking library used here
- `H2O AutoML <https://docs.h2o.ai/h2o/latest-stable/h2o-docs/automl.html>`_: free version of H2O.ai, $100M Series E 🚀
- `hyperopt-sklearn <http://hyperopt.github.io/hyperopt-sklearn/>`_: uses hyperopt to search sklearn pipelines
- `mljar-supervised <https://supervised.mljar.com/>`_: has several modes depending on how aggressively you want to search
- `MLNet <https://docs.microsoft.com/en-us/dotnet/machine-learning/reference/ml-net-cli-reference/>`_: command line AutoML by Microsoft
- `TPOT <https://github.com/EpistasisLab/tpot/>`_: optimizes sklearn pipelines using genetic programming, gives you back the code of the best pipeline
  
In addition, the following non-AutoML baseline frameworks are available for comparison:

- Constant Predictor: predicts empirical target class probabilities for classification or the target median for regression
- Decision Tree: sklearn Decision Tree with default parameters
- Random Forest: sklearn Random Forest with default parameters except `n_estimators = 2000`
- Tuned Random Forest: above with tuned `max_features` parameter

For all frameworks you can

- Get predictions on new data
- Download anything saved during training like leaderboards, figures, and logs

Helpful links

- For the latest documentation: https://modep-ai.github.io/modep-client  
- To add new frameworks, add PRs to: https://github.com/openml/automlbenchmark
- For the API's Swagger docs: https://modep.ai/v1/api-docs
