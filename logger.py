import logging

def setup_logger(debug=False):
    log_level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        filename='./_output/tool_log.log',
        filemode='w',
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=log_level
    )
    logger = logging.getLogger()
    return logger