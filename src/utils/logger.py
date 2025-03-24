import logging

def get_logger(settings):
    log_config = settings.get('logging', {})
    log_level = getattr(logging, log_config.get('level', 'INFO').upper())
    log_file = log_config.get('file', 'app.log')
    enable_console = log_config.get('console', True)

    logger = logging.getLogger('cross_universe_sync')
    logger.setLevel(log_level)
    logger.propagate = False

    if not logger.handlers:
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        fh = logging.FileHandler(log_file)
        fh.setLevel(log_level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        if enable_console:
            ch = logging.StreamHandler()
            ch.setLevel(log_level)
            ch.setFormatter(formatter)
            logger.addHandler(ch)

    return logger
