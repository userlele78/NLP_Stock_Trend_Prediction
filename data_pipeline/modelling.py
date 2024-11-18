import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split, cross_val_score
import optuna


class Modelling:
    def __init__(self, dataset_path, target_column, train_size=0.8, random_state=42):
        """
        Initialize the Modelling class with training and testing splits.

        Parameters:
            dataset_path (str): Path to the dataset file (CSV).
            target_column (str): The name of the target column.
            train_size (float): Proportion of the dataset to use for training.
            random_state (int): Seed for reproducibility.
        """
        self.dataset_path = dataset_path
        self.target_column = target_column
        self.train_size = train_size
        self.random_state = random_state

        # Load and split the dataset
        self.X_train, self.X_test, self.y_train, self.y_test = self.get_train_test_splits()

    def get_train_test_splits(self):
        """
        Load the dataset, split it into training and testing sets.

        Returns:
            X_train, X_test, y_train, y_test: Training and testing splits.
        """
        data = pd.read_csv(self.dataset_path)
        X = data.drop(columns=[self.target_column])
        y = data[self.target_column]

        return train_test_split(
            X, y, train_size=self.train_size, random_state=self.random_state
        )

    def model_selection(self, model="Random Forest", param=None, use_optuna=False, n_trials=50):
        """
        Train and evaluate a specified machine learning model.

        Parameters:
            model (str): Name of the model to use.
            param (dict): Hyperparameters for the model.
            use_optuna (bool): Whether to use Optuna for hyperparameter tuning.
            n_trials (int): Number of Optuna trials.

        Returns:
            acc (float): Accuracy of the model.
            report (str): Detailed classification report.
        """
        model_name, model_func = self.model_mapping(model)
        if use_optuna:
            print(f"Running Optuna optimization for {model_name}...")
            param = self.optimize_model(model_func, n_trials)

        acc, report = self.train_and_report(model_func, param)
        print(f"Accuracy of {model_name}: {acc:.4f}")
        return acc, report

    def model_mapping(self, model):
        """
        Map model names to sklearn model classes.

        Parameters:
            model (str): Model name.

        Returns:
            Tuple[str, class]: Model name and corresponding class.
        """
        mapping = {
            "Logistic Regression": LogisticRegression,
            "Random Forest": RandomForestClassifier,
        }
        if model not in mapping:
            raise ValueError(f"Model '{model}' is not supported.")
        return model, mapping[model]

    def train_and_report(self, model, param=None):
        """
        Train the model and generate a classification report.

        Parameters:
            model (class): Model class.
            param (dict): Hyperparameters for the model.

        Returns:
            accuracy (float): Accuracy of the model.
            report (str): Detailed classification report.
        """
        if param is None:
            param = {}

        clf = model(**param)
        clf.fit(self.X_train, self.y_train)
        y_pred = clf.predict(self.X_test)

        accuracy = accuracy_score(self.y_test, y_pred)
        report = classification_report(self.y_test, y_pred, zero_division=0)
        return accuracy, report

    def optimize_model(self, model, n_trials=50):
        """
        Use Optuna to find the best hyperparameters for a model.

        Parameters:
            model (class): Model class.
            n_trials (int): Number of Optuna trials.

        Returns:
            best_params (dict): Best hyperparameters found by Optuna.
        """
        def objective(trial):
            param = self.get_param_search_space(model, trial)
            clf = model(**param)
            return cross_val_score(clf, self.X_train, self.y_train, cv=3, n_jobs=-1).mean()

        study = optuna.create_study(direction="maximize")
        study.optimize(objective, n_trials=n_trials)
        print(f"Best parameters found by Optuna: {study.best_params}")
        return study.best_params

    def get_param_search_space(self, model, trial):
        """
        Define the hyperparameter search space for Optuna.

        Parameters:
            model (class): Model class.
            trial (optuna.Trial): Optuna trial object.

        Returns:
            param (dict): Dictionary of hyperparameters.
        """
        if model == LogisticRegression:
            return {
                "C": trial.suggest_loguniform("C", 1e-4, 1e2),
                "penalty": trial.suggest_categorical("penalty", ["l2"]),
                "solver": trial.suggest_categorical("solver", ["lbfgs", "liblinear"]),
                "max_iter": trial.suggest_int("max_iter", 100, 300),
            }
        elif model == RandomForestClassifier:
            return {
                "n_estimators": trial.suggest_int("n_estimators", 50, 500),
                "max_depth": trial.suggest_int("max_depth", 5, 50),
                "min_samples_split": trial.suggest_int("min_samples_split", 2, 10),
                "min_samples_leaf": trial.suggest_int("min_samples_leaf", 1, 10),
                "bootstrap": trial.suggest_categorical("bootstrap", [True, False]),
            }
        else:
            raise ValueError("No parameter search space defined for this model.")

    def plot_scores(self, scores, metric_names):
        """
        Plot the performance metrics.

        Parameters:
            scores (list): List of metric scores.
            metric_names (list): List of metric names.
        """
        plt.figure(figsize=(8, 5))
        plt.bar(metric_names, scores, color=["blue", "orange", "green", "red"])
        plt.ylabel("Score")
        plt.title("Model Performance")
        plt.show()


def main():
    """
    Run the main flow of training and evaluating models.
    """
    dataset_path = r"dataset/data.csv"  # Update with the actual path
    target_column = "target"  # Update with the actual target column name

    # Initialize Modelling instance
    model_instance = Modelling(
        dataset_path=dataset_path, target_column=target_column, train_size=0.8
    )

    # Train and evaluate Random Forest with Optuna
    print("Evaluating Random Forest with Optuna:")
    acc_rf, report_rf = model_instance.model_selection(
        model="Random Forest", use_optuna=True, n_trials=30
    )
    print(report_rf)

    # Train and evaluate Logistic Regression with Optuna
    print("Evaluating Logistic Regression with Optuna:")
    acc_lr, report_lr = model_instance.model_selection(
        model="Logistic Regression", use_optuna=True, n_trials=30
    )
    print(report_lr)

    # Plot scores
    scores = [acc_rf, acc_lr]
    metric_names = ["Random Forest", "Logistic Regression"]
    model_instance.plot_scores(scores, metric_names)


if __name__ == "__main__":
    main()
