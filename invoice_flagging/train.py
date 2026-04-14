
from data_preprocessing import load_invoice_data, split_data, scale_features, apply_labels
from model_evaluation import train_random_forest, evaluate_classifier
import joblib
from pathlib import Path

FEATURES = [
    "invoice_quantity",
    "invoice_dollars",
    "Freight",
    "total_item_quantity",
    "total_item_dollars"
]

TARGET = "flag_invoice"
    
    
def main():
    BASE_DIR = Path(__file__).resolve().parent.parent
    model_dir = BASE_DIR / "models"
    model_dir.mkdir(parents=True, exist_ok=True) 
    
    scaler_path = model_dir / "scaler.pkl"
    model_path = model_dir / "predict_flag_invoice.pkl"
    
    # Load data
    df = load_invoice_data()
    df = apply_labels(df)

    # Prepare data
    X_train, X_test, y_train, y_test = split_data(df, FEATURES, TARGET)
    X_train_scaled, X_test_scaled = scale_features(
        X_train, X_test, str(scaler_path)
    )
    
    # Train and evaluate models
    print("Training Random Forest with GridSearchCV...This might take few minutes⏳")
    grid_search = train_random_forest(X_train_scaled, y_train)

    evaluate_classifier(
        grid_search.best_estimator_,
        X_test_scaled,
        y_test,
        "Random Forest Classifier"
    )
    
    # Save best model
    joblib.dump(grid_search.best_estimator_, str(model_path) )

if __name__ == "__main__":
    main()
