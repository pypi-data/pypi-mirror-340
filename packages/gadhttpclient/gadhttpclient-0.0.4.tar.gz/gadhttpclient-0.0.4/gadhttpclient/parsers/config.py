import pathlib

from gadify import temp
from gadify import urls

from gadhttpclient import const
from gadhttpclient.os import HTTP


def getconfig(file: str) -> tuple[pathlib.Path, bool]:
    if urls.checkurl(file):
        return temp.getfile(HTTP.download(file), extension=const.EXTENSION_TOML), True
    else:
        return pathlib.Path(file), False
