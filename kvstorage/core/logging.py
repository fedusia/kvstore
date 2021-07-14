import logging
import sys


class RequestIDAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        return (
            "req_id: {}, message: {}".format(self.extra.get("x-request-id"), msg),
            kwargs,
        )


def create_logger():

    # Logger initialization
    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "%(asctime)-15s [%(filename)s:%(lineno)s %(funcName)s] %(levelname)s %(message)s"
    )
    handler.setFormatter(formatter)
    logger.handlers.clear()
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.info("Logger initialized")

    adapter = RequestIDAdapter(logger, {})
    adapter.info("Added RequestIDAdapter for logger")
    return adapter
