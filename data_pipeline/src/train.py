import argparse
import mlflow
import yaml

def train(data_path: str, params: dict):
    # TODO: Load training data
    # TODO: Use MLflow to log parameters, metrics, and models for Linear and Tree-based models
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_path", type=str, required=True)
    parser.add_argument("--params_path", type=str, default="params.yaml")
    args = parser.parse_args()
    
    with open(args.params_path, "r") as f:
        params = yaml.safe_load(f)
        
    train(args.data_path, params)
