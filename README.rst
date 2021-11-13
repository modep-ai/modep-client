============
modep-client
============
.. image:: https://github.com/modep-ai/modep-client/actions/workflows/docs.yml/badge.svg
           :target: https://modep-ai.github.io/modep-client
.. image:: https://github.com/modep-ai/modep-client/actions/workflows/tests.yml/badge.svg
        :target: https://github.com/modep-ai/modep-client/actions		    
.. image:: https://img.shields.io/pypi/v/modep-client.svg
        :target: https://pypi.org/project/modep-client

Python client for the modep API. Run flights of AutoML frameworks:

- AutoGluon: https://auto.gluon.ai: Amazons's version of AutoML with new stacking
- auto-sklearn: https://www.automl.org/automl/auto-sklearn/:  automatic sklearn pipelines
- auto-sklearn 2.0: https://www.automl.org/auto-sklearn-2-0-the-next-generation/: added portfolios
- Auto-WEKA: https://www.cs.ubc.ca/labs/beta/Projects/autoweka/: a JAR if you're into that
- FLAML: https://github.com/microsoft/FLAML: Microsoft's version of AutoML - Fast and Lightweight AutoML
- GAMA: https://github.com/PGijsbers/gama: AutoML project from OpenML (same authors of AutoML benchmarks https://github.com/openml/automlbenchmark)
- H2O AutoML: https://docs.h2o.ai/h2o/latest-stable/h2o-docs/automl.html: by H2O.ai - $100M Series E 🚀
- hyperopt-sklearn: http://hyperopt.github.io/hyperopt-sklearn/: uses hyperopt to search sklearn pipelines
- mljar-supervised: https://supervised.mljar.com/: a JAR that does AutoML
- MLNet: https://docs.microsoft.com/en-us/dotnet/machine-learning/reference/ml-net-cli-reference: command line AutoML by Microsoft
- TPOT: https://github.com/EpistasisLab/tpot: optimizes sklearn pipelines using genetic programming

In addition, the following non-AutoML baseline frameworks are available for comparison:

- Constant Predictor: predicts empirical target class probabilities for classification or the target median for regression
- Decision Tree: scikit-learn Decision Tree with default parameters
- Random Forest: scikit-learn Random Forest with default parameters except `n_estimators = 2000`
- Tuned Random Forest: above with tuned `max_features` parameter

For these you can get predictions on new data and any saved figures generated during training.
  
To add new frameworks, add PRs to: https://github.com/openml/automlbenchmark
  
Latest release documentation: https://modep-ai.github.io/modep-client
