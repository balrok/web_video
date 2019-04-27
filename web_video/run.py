#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# check dir for files older 60s so we are sure to have complete transfered files
# then create a tmp dir for them
# put a screenshot
# use bento4 to create different qualities
#     hls
#     dash
#     webm
# when finished remove file and move tmp directory

try:
    from os import scandir
except ImportError:
    from scandir import scandir
import sys
import urllib.request
from time import time
import os
from lib.singleton import SingleInstance
from lib.filetype import BasicFile
from zenlog import log
from zenlog import logging
import logging.handlers


def main(root_dir: str, callback: str=""):
    return_code = 0
    for e in scandir(root_dir):
        if e.is_dir():
            log.debug("checking %s", e.name)
            changed = False
            dirstart = time()
            is_watch_dir = False
            for entry in scandir(e.path):
                fh = BasicFile.get_instance(entry)
                if fh:
                    is_watch_dir = True
                    log.debug("Found a file %s with type %s", entry.name,
                              repr(fh))
                    start = time()
                    res = fh.process()
                    changed = False
                    for i in res:
                        if res[i] == fh.UPDATED:
                            changed = True
                            log.info("updated {} - {}".format(entry.name, i))
                        if res[i] == fh.ERROR:
                            log.error(
                                "ERROR: {} could not be processed - {}\n".
                                format(entry.name, i))
                            return_code = -1
                    if time() - start > 1:
                        log.info("For %s took: %d", entry.name,
                                 int(time() - start))
            if is_watch_dir:
                if BasicFile.foldername_string(e.name) != e.name:
                    log.warning(
                        "The Foldername is not nice for urls - fixing it")
                    BasicFile.move_directory(
                        e.path,
                        os.path.join(
                            os.path.dirname(e.path),
                            BasicFile.foldername_string(e.name)))

                if time() - dirstart > 1:
                    log.info("For dir %s took: %d", e.path,
                             int(time() - dirstart))

                if changed:
                    if len(callback) > 0:
                        if callback.startswith("http"):
                            log.info("Opening url %s" % callback)
                            try:
                                urllib.request.urlopen(callback).read()
                            except:
                                log.error("Error opening this url")
                        else:
                            log.error("callback must start with http: %s",
                                      callback)
    sys.exit(return_code)


def configure_logging(root_dir: str):
    logger = logging.getLogger()
    hdlr = logging.handlers.RotatingFileHandler(
        os.path.join(root_dir, ".web_video.log"),
        maxBytes=1024 * 1024 * 10,
        backupCount=5)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    try:
        from logging.handlers import SysLogHandler
        syslog = SysLogHandler()
        syslog.setFormatter(formatter)
        logger.addHandler(syslog)
    except Exception as e:
        log.warning("No syslog handler: %s", e)


lock = None


def run_it():
    global lock
    configure_logging(sys.argv[1])
    lock = SingleInstance("videotransformer")
    #if not BasicFile.test_requirements():
    #    log.error("Some program requirements not met")
    #    sys.exit(-1)
    # first argument is folder which we will check
    # second argument a callback-url
    main(*sys.argv[1:])


if __name__ == "__main__":
    run_it()
