import logging

file='logs/log.log'
level = logging.ERROR
fmt="%(levelname)s (%(asctime)s) %(message)s (Line: %(lineno)s) %(filename)s"
datefmt="%d/%m/%Y %I:%M:%S"