import argparse
from core.services.metadata_service import MetadataService

def run_cli():
    parser = argparse.ArgumentParser(description="Metadata Inspector CLI")
    parser.add_argument("--file", "-f", help="File path", required=True)
    parser.add_argument("--type", "-t", help="File type (image, pdf...)", required=True)
    parser.add_argument("--extract", action="store_true", help="Extract metadata")
    parser.add_argument("--clean", action="store_true", help="Clean metadata")
    args = parser.parse_args()

    service = MetadataService()

    if args.extract:
        metadata = service.extract(args.file, args.type)
        print("Extracted Metadata:\n", metadata)
    elif args.clean:
        service.clean(args.file, args.type)
        print("Metadata cleaned.")
    else:
        print("Please specify --extract or --clean")
