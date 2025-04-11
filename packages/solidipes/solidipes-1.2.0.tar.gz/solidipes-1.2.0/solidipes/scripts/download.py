import argparse

from solidipes.plugins.discovery import downloader_list

command = "download"
command_help = "Download dataset to an online repository"


# Get all downloaders
downloader_subclasses_instances = [Subclass() for Subclass in downloader_list]
downloaders = {downloader.command: downloader for downloader in downloader_subclasses_instances}


def main(args):
    platform = args.platform
    downloader = downloaders[platform]
    downloader.download(args)


def populate_arg_parser(parser):
    # Create subparsers for each download platform
    downloader_parsers = parser.add_subparsers(dest="platform", help="Target hosting platform")
    downloader_parsers.required = True

    for downloader in downloaders.values():
        downloader_parser = downloader_parsers.add_parser(downloader.command, help=downloader.command_help)
        downloader.populate_arg_parser(downloader_parser)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    populate_arg_parser(parser)
    args = parser.parse_args()
    main(args)
