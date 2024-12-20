import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

class OutlierClipper(BaseEstimator, TransformerMixin):
    def __init__(self, numerical_columns=None, threshold=1.5):
        # Si numerical_columns est None, cela signifie qu'il faut définir les colonnes numériques automatiquement
        self.numerical_columns = numerical_columns
        self.threshold = threshold

    def fit(self, X, y=None):
        # Si X est un tableau numpy, le convertir en DataFrame
        if isinstance(X, np.ndarray):
            X = pd.DataFrame(X)

        # Si X est déjà un DataFrame
        if isinstance(X, pd.DataFrame):
            # Si numerical_columns n'a pas été fourni, l'extraire des colonnes numériques du DataFrame
            if self.numerical_columns is None:
                self.numerical_columns = X.select_dtypes(include=['float64', 'int64']).columns.tolist()

            self.columns = self.numerical_columns
        else:
            raise ValueError("X doit être un DataFrame ou un tableau numpy")

        self.lower_bounds = {}
        self.upper_bounds = {}

        # Calculer les bornes inférieures et supérieures pour chaque colonne numérique
        for col in self.columns:
            Q1 = X[col].quantile(0.25)
            Q3 = X[col].quantile(0.75)
            IQR = Q3 - Q1
            self.lower_bounds[col] = Q1 - self.threshold * IQR
            self.upper_bounds[col] = Q3 + self.threshold * IQR

        return self

    def transform(self, X):
        # Si X est un tableau numpy, le convertir en DataFrame
        if isinstance(X, np.ndarray):
            X = pd.DataFrame(X, columns=self.columns)

        # Appliquer le clipping
        X_clipped = X.copy()
        for col in self.columns:
            lower = self.lower_bounds[col]
            upper = self.upper_bounds[col]
            X_clipped[col] = X_clipped[col].clip(lower=lower, upper=upper)

        return X_clipped


# Les 2 solutions marchent

# import numpy as np
# import pandas as pd
# from sklearn.base import BaseEstimator, TransformerMixin

# class OutlierClipper(BaseEstimator, TransformerMixin):
#     def __init__(self, numerical_columns=None, threshold=1.5):
#         # Si numerical_columns est None, cela signifie qu'il faut définir les colonnes numériques automatiquement
#         self.numerical_columns = numerical_columns
#         self.threshold = threshold

#     def fit(self, X, y=None):
#         # Si X est un tableau numpy, le convertir en DataFrame
#         if isinstance(X, np.ndarray):
#             X = pd.DataFrame(X)

#         # Si X est déjà un DataFrame
#         if isinstance(X, pd.DataFrame):
#             # Si numerical_columns n'a pas été fourni, l'extraire des colonnes numériques du DataFrame
#             if self.numerical_columns is None:
#                 self.numerical_columns = X.select_dtypes(include=['float64', 'int64']).columns.tolist()

#             self.columns = self.numerical_columns
#         else:
#             raise ValueError("X doit être un DataFrame ou un tableau numpy")

#         self.lower_bounds = {}
#         self.upper_bounds = {}

#         # Calculer les bornes inférieures et supérieures pour chaque colonne numérique
#         for col in self.columns:
#             Q1 = X[col].quantile(0.25)
#             Q3 = X[col].quantile(0.75)
#             IQR = Q3 - Q1
#             self.lower_bounds[col] = Q1 - self.threshold * IQR
#             self.upper_bounds[col] = Q3 + self.threshold * IQR

#         return self

#     def transform(self, X):
#         # Si X est un tableau numpy, le convertir en DataFrame
#         if isinstance(X, np.ndarray):
#             X = pd.DataFrame(X, columns=self.columns)

#         # Appliquer le clipping
#         X_clipped = X.copy()
#         for col in self.columns:
#             lower = self.lower_bounds[col]
#             upper = self.upper_bounds[col]
#             X_clipped[col] = X_clipped[col].clip(lower=lower, upper=upper)

#         return X_clipped
