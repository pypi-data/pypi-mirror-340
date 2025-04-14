import argparse
from sys import prefix, exit
import pyplus

print(prefix + "\\python.exe: No module named pyplus.__main__; 'pyplus' is a package and cannot be directly executed")

exit(-1)

parser = argparse.ArgumentParser(description="imgfit commands")
subparsers = parser.add_subparsers(dest="command", required=True)

subparsers.add_parser("auto", help="Auto mode.")
subparsers.add_parser("manual", help="Manual mode.")
subparsers.add_parser("version",help="get the version.")
custom = subparsers.add_parser("customize",help="customize mode,same as 'pip install --upgrade [customize]'")
custom.add_argument("options",help="Same as 'pip install --upgrade [customize]'",nargs="+")
subparsers.add_parser("del_cache",help="Delete cache.")

args = parser.parse_args()

if args.command == "auto":
    auto_upgrade_pip.auto()
elif args.command == "manual":
    auto_upgrade_pip.manual()
elif args.command == "customize":
    auto_upgrade_pip.customize(args.options)
elif args.command == "del_cache":
    auto_upgrade_pip.delete_cache()
elif args.command == "version":
    print("Version : auto-upgrade-pip",auto_upgrade_pip.__version__)
