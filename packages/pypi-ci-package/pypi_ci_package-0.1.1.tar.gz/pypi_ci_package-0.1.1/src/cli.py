import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("name", type=str)
    parser.add_argument("age", type=float)

    args = parser.parse_args()

    print(f"Name: {args.name}")
    print(f"Age: {args.age}")
