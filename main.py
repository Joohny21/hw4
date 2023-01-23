"""
Відсортувати файли в папці.
"""

import argparse
from pathlib import Path
from shutil import copyfile
import concurrent.futures
import logging
from typing import List

"""
--source [-s] picture
--output [-o]
"""

THREAD_POOL_SIZE = 4

parser = argparse.ArgumentParser(description='Sorting folder')
parser.add_argument("--source", "-s", help="Source folder", required=True)
parser.add_argument("--output", "-o", help="Output folder", default="dist")

args = vars(parser.parse_args())

source = args.get("source")
output = args.get("output")

folders = []
files = []


def grabs_folder(path: Path) -> None:
    for el in path.iterdir():
        if el.is_dir():
            folders.append(el)
            grabs_folder(el)


#
def copy_file(el: Path) -> None:
    if el.is_file():
        ext = el.suffix
        new_path = output_folder / ext
        try:
            new_path.mkdir(exist_ok=True, parents=True)
            copyfile(el, new_path / el.name)
        except OSError as err:
            logging.error(err)


def _iterdir(fldr: Path):
    for each in fldr.iterdir():
        if each.is_file():
            files.append(each)


def main(folders: List):
    with concurrent.futures.ThreadPoolExecutor(max_workers=THREAD_POOL_SIZE) as executor:
        futures = []
        for folder in folders:
            futures.append(executor.submit(_iterdir, folder))

    with concurrent.futures.ThreadPoolExecutor(max_workers=THREAD_POOL_SIZE) as executor:
        for el in files:
            futures.append(executor.submit(copy_file, el))


if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR, format="%(threadName)s %(message)s")
    base_folder = Path(source)
    output_folder = Path(output)
    folders.append(base_folder)
    grabs_folder(base_folder)
    main(folders)

    # threads = []
    #
    # for folder in folders:
    #     th = Thread(target=copy_file, args=(folder,))
    #     th.start()
    #     threads.append(th)
    #
    # [th.join() for th in threads]

    print('Можно удалять стару папку якщо треба')
