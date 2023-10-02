import logging
import logstash

# generate log
logger = logging.getLogger()

# log level
logger.setLevel(logging.INFO)

#  log formatter
# formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
logger.addHandler(logstash.LogstashHandler("logstash", 5044, version=1, tags="ugc_etl"))
# log to console
# stream_handler = logging.StreamHandler()
# stream_handler.setFormatter(formatter)

# logger.addHandler(stream_handler)
