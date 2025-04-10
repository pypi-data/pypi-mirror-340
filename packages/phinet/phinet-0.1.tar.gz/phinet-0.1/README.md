# PHINet - Phishing Email Detection

PHINet is a lightweight custom boosting model for detecting phishing emails, built from scratch using decision trees and hand-crafted features.

## Features
- Custom boosting algorithm
- Suspicious keyword detection
- URL and attachment analysis
- Sender domain encoding

## Installation
```bash
pip install .
```

## Usage
```python
from phinet.model import PHINetBoost, PHINetFeatureEngine

engine = PHINetFeatureEngine()
features = engine.transform(df)
model = PHINetBoost()
model.fit(features, labels)
```
