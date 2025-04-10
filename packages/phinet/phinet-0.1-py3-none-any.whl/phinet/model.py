
import pandas as pd
import numpy as np
import re
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.utils.validation import check_X_y, check_array

# ----- Feature Engineering -----
class PHINetFeatureEngine:
    keyword_list = ['login', 'verify', 'bank', 'account', 'urgent', 'click']

    def __init__(self):
        self.domain_encoder = LabelEncoder()

    def transform(self, df):
        df = df.copy()
        df['body_length'] = df['email_body'].apply(len)
        df['suspicious_keywords'] = df['email_body'].apply(
            lambda body: sum(kw in body.lower() for kw in PHINetFeatureEngine.keyword_list)
        )
        df['url_count'] = df['urls'].apply(lambda u: len(re.findall(r'https?://', str(u))))
        df['https_count'] = df['urls'].apply(lambda u: str(u).count("https://"))
        df['attachment_risk'] = df['attachments'].apply(
            lambda att: int(any(ext in str(att).lower() for ext in ['.exe', '.zip', '.bat']))
        )
        df['sender_domain'] = df['email_id'].apply(lambda e: e.split('@')[-1] if '@' in e else 'unknown')
        df['sender_domain_encoded'] = self.domain_encoder.fit_transform(df['sender_domain'])

        return df[['body_length', 'suspicious_keywords', 'url_count', 'https_count',
                   'attachment_risk', 'sender_domain_encoded']]

# ----- Boosting Model -----
class PHINetBoost(BaseEstimator, ClassifierMixin):
    def __init__(self, n_estimators=5, max_depth=3):
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.models = []

    def fit(self, X, y):
        X, y = check_X_y(X, y)
        residual = y.copy()
        self.models = []
        for _ in range(self.n_estimators):
            tree = DecisionTreeClassifier(max_depth=self.max_depth)
            tree.fit(X, residual)
            pred = tree.predict(X)
            residual = y - pred
            self.models.append(tree)
        return self

    def predict(self, X):
        X = check_array(X)
        preds = np.sum([model.predict(X) for model in self.models], axis=0)
        return (preds >= (self.n_estimators / 2)).astype(int)

# ----- Training Wrapper -----
def train_phinet_model(df):
    feature_engine = PHINetFeatureEngine()
    X = feature_engine.transform(df)
    y = df['label']
    model = PHINetBoost(n_estimators=7)
    model.fit(X, y)
    return model, feature_engine
