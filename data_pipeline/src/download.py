import argparse

def download_data(source_url: str, output_path: str):
    # TODO: Implement downloading the dataset from source_url and saving to output_path
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source_url", type=str, required=True)
    parser.add_argument("--output_path", type=str, required=True)
    args = parser.parse_args()
    
    download_data(args.source_url, args.output_path)
