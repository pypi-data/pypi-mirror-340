# -*- coding: utf-8 -*-

import argparse
import warnings
import sys
import traceback

from pkg_info import get_pkg_info
from semver import compare

from tailer_sdk import tailer_config
from tailer_sdk import tailer_configuration_manager
from tailer_sdk import tailer_gcp_cf_manager
from tailer_sdk import tailer_auth
from tailer_sdk import tailer_help
from tailer_sdk import tailer_crypto
from tailer_sdk import sql_dag_generator

import google.auth

warnings.filterwarnings(
    "ignore", "Your application has authenticated using end user credentials")

# Globals
#
__version__ = "1.3.19"
TAILER_SDK_NAME = "tailer-sdk"


def display_tailer_header():

    print("")
    print("Tailer SDK")
    print("Version : " + __version__)
    print("")


def notify_update_tailer_sdk():

    print("Checking Tailer SDK version ...\n")

    try:

        pkg = get_pkg_info(TAILER_SDK_NAME)

        if compare(__version__, pkg.version) < 0:

            print("\nIMPORTANT NOTICE")
            print("-----------------")
            print("Update available {} -> {}".format(__version__, pkg.version))
            print("Please run : pip3 install tailer-sdk --upgrade\n")

    except Exception as ex:

        print("\nError while retrieving package information : \n{}\n".format(ex))


def main():

    # Display Tailer header
    #
    display_tailer_header()

    parser = argparse.ArgumentParser(
                description=__doc__,
                formatter_class=argparse.RawDescriptionHelpFormatter,
                add_help=False)

    parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help='Please type \'tailer help\' for full detailed help.')
    parser.add_argument("command", help="Tailer SDK command.", type=str)
    parser.add_argument("--no-gcp-cf-deploy", help="Will not deploy GCP Cloud Function associated to a configuration.", action='store_true')
    parser.add_argument("arguments", nargs=argparse.REMAINDER)

    args = parser.parse_args()

    # Evaluating COMMAND
    #
    if args.command == "config":
        tailer_config.tailer_config()

    elif args.command == "migrate":
        tailer_config.migrate_config()

    elif args.command == "configuration":

        # TTT local run case
        #
        conf_usage = "Usage :\n\ntailer configuration run TTT-CONFIGURATION.json [task_1 task_2 ... task_N]\n\n"

        if len(args.arguments) >= 2:
            if args.arguments[0].strip() == "run":
                sql_dag_generator.process(
                        configuration_file=args.arguments[1],
                        run_locally=True,
                        arguments=args.arguments,
                        tailer_sdk_version=__version__)
            else:
                print(conf_usage)
        else:
            print(conf_usage)

    elif args.command == "encrypt":
        if len(args.arguments) > 0:
            tailer_crypto.encrypt_payload(args.arguments[0])
        else:
            print("Please provide something to encrypt.")

    elif args.command == "generate-keys":
        tailer_crypto.generate_key_pair()

    elif args.command == "auth":
        if len(args.arguments) > 0:
            if (args.arguments)[0] == "login":
                tailer_auth.login()

            elif (args.arguments)[0] == "get-token":

                # Get configuration
                #
                tailer_configuration = tailer_config.get_tailer_configuration_file()
                tailer_auth.get_token(tailer_configuration)

            elif (args.arguments)[0] == "reset-password":

                # Get configuration
                #
                tailer_configuration = tailer_config.get_tailer_configuration_file()
                tailer_auth.reset_password(tailer_configuration=tailer_configuration)

    elif args.command == "create":
        if len(args.arguments) > 0:
            if (args.arguments)[0] == "configuration":
                if tailer_configuration_manager.process(args, tailer_sdk_version=__version__) is False:
                    raise Exception("error while processing Tailer SDK create command.")

    elif args.command == "check":
        if len(args.arguments) > 0:
            if (args.arguments)[0] == "configuration":
                if tailer_configuration_manager.process(args, tailer_sdk_version=__version__) is False:
                    raise Exception("error while processing Tailer SDK check command.")

    elif args.command == "deploy":
        if len(args.arguments) > 0:
            if (args.arguments)[0] == "configuration":
                if tailer_configuration_manager.process(args, tailer_sdk_version=__version__) is False:
                    raise Exception("error while processing Tailer SDK deploy command.")

            if (args.arguments)[0] == "gcp-cloud-function":
                tailer_gcp_cf_manager.process(args)
    
    elif args.command == "help":
        tailer_help.display_help()
    else:
        tailer_help.display_help()

    # Check if there is a newer version
    #
    notify_update_tailer_sdk()


if __name__ == "__main__":

    try:
        main()
        exit(0)

    except Exception:

        print("Error:\n")
        exc = sys.exception()
        for excLine in traceback.format_exc(exc):
            print(excLine)

        exit(1)
