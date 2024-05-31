from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix


def build_model() -> RandomForestClassifier:
    return RandomForestClassifier(n_estimators=100, min_samples_split=50, random_state=1)


def train_model(x_train, y_train, build_model_fn):
    model = build_model_fn()
    model.fit(x_train, y_train)

    return model


def evaluate_model_performance(y_true, y_pred):
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)
    cm = confusion_matrix(y_true, y_pred)

    return {"accuracy": accuracy, "precision": precision, "recall": recall, "f1": f1, "confusion_matrix": cm}
