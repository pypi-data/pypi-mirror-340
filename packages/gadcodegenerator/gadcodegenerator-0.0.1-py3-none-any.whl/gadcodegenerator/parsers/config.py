import pathlib

from gadutils import temp
from gadutils import urls

from gadcodegenerator import const
from gadcodegenerator.os import HTTP
from gadcodegenerator.os import File


def getconfig(file: str) -> tuple[pathlib.Path, bool]:
    if urls.checkurl(file):
        return temp.getfile(HTTP.download(file), extension=const.EXTENSION_TOML), True
    else:
        return pathlib.Path(file), False


def getcontent(workdir: pathlib.Path, content: str) -> str:
    if content.startswith(const.SYNTAX_FILES_CONTENT_FILE):
        path = pathlib.Path(content[len(const.SYNTAX_FILES_CONTENT_FILE) :].strip())

        if not path.is_absolute():
            path = workdir / path

        if path.exists() and path.is_file():
            return File.read(path)

    elif urls.checkurl(content):
        return HTTP.download(content)

    return content
