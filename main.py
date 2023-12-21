import sys
import config

from Tests.test import TestFlow
from Utils.http_request import HttpRequest
from Utils.logging_utils import configure_logging, logging

def main():
    try:
        # Set defaults
        server_url = config.SERVER_URL
        log_level = logging.INFO

        # Check if user provided a server URL
        if len(sys.argv) > 1:
            server_url = sys.argv[1]

        # Check if user provided a log level
        if len(sys.argv) > 2:
            log_level = getattr(logging, sys.argv[2].upper(), logging.INFO)

        configure_logging(log_level)
        HttpRequest.base_url = server_url

        # Run the test flow
        TestFlow().test_flow()

    except Exception as e:
        logging.exception(f"An error occurred: {e}")


if __name__ == "__main__":
    main()