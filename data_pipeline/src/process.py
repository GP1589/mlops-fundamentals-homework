import argparse

def process_data(input_path: str, train_output: str, prod_output: str):
    # TODO: Load dataset, split temporally (pre-2018 for train, 2018+ for prod simulation)
    # Save train_output and prod_output
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path", type=str, required=True)
    parser.add_argument("--train_output", type=str, required=True)
    parser.add_argument("--prod_output", type=str, required=True)
    args = parser.parse_args()
    
    process_data(args.input_path, args.train_output, args.prod_output)
