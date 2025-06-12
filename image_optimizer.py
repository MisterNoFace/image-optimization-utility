import os, shutil, time, subprocess
from multiprocessing import Pool
from argparse import ArgumentParser

if __name__ == '__main__':
    print('\033[35m[INSTALL]\033[0m downloading/updating modules for the program')
    subprocess.run(['python', '-m', 'pip', 'install', '--upgrade', 'pip'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(['pip', 'install', 'pathlib', 'pillow', 'tqdm', '--upgrade'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

from pathlib import Path
from tqdm import tqdm
from PIL import Image, UnidentifiedImageError, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

parser = ArgumentParser(prog='web image utility')
parser.add_argument("-p", "--path", required=True, help="path of the folder to scan")
parser.add_argument("-n", "--name", required=False, default='COPIA', help="suffix to add to the name of the copy folder. Default is 'COPIA'")
parser.add_argument('-m', '--max-size', required=False, default=300, help="maximum image size in kB. Default=300")
parser.add_argument("-q", "--quality", required=False, default=50, help="image quality (1-100). Default=50")
parser.add_argument("-dpi", "--dpi", required=False, default=72, help="image dpi. Default=72")
parser.add_argument("-c", "--compression", required=False, default=6, help="image compression level (1-9). Default=6")
args = parser.parse_args()

if not os.path.exists(args.path):
    print(f'the path {args.path} does not exist in the filesystem, terminating the program')
    exit()

new_images_path = args.path + '_' + args.name
os.makedirs(new_images_path, exist_ok=True)

def get_folder_images(directory: str) -> list:
    img_folder: list = []
    for dir, subdirs, files in os.walk(directory):
        for file in files:
            f = Path(dir).joinpath(file)
            if f.is_file() and f.suffix.lower() in ['.jpg', '.jpeg', '.png', '.webp', '.svg']:
                # print(f)
                img_folder.append(f)
    return img_folder

def copy_image(img_path: Path):
    global new_images_path
    x = str(img_path.parent).replace(args.path, new_images_path)
    if not os.path.exists(x + img_path.name):
        os.makedirs(x, exist_ok=True)
        return Path(shutil.copy(img_path, x))
    return None

def resize_image(img_path: Path) -> float:
    try:
        with Image.open(img_path) as img:
            s = img_path.stat().st_size
            if img.width < 1920 or img.height < 1080:
                img = img.resize(size=(int(img.width / 2), int(img.height / 2)))
            else:
                img = img.resize(size=(int(img.width / 4), int(img.height / 4)))

            if img_path.suffix.lower() == '.png':
                img = img.convert('RGBA')
            else:
                img = img.convert('RGB')
            img.save(
                fp=img_path,
                optimize=True,
                compress_level=min(max(int(args.compression), 1), 9),
                quality=min(max(int(args.quality), 0), 100),
                dpi=(int(args.dpi), int(args.dpi))
            )
            return s - img_path.stat().st_size
    except (UnidentifiedImageError, OSError) as e:
        return 0

if __name__ == '__main__':
    t = time.time()
    print(f'\033[33m[CHECK]\033[0m searching for images in: \033[36m{args.path}\033[0m')
    found_images = get_folder_images(args.path)

    pool = Pool(min(32, os.cpu_count() * 2))
    print(f'\033[32m[INFO]\033[0m copying images to: \033[36m{new_images_path}\033[0m')
    copied_images = list(
        tqdm(
            iterable=pool.imap(copy_image, found_images),
            total=len(found_images),
            desc='\033[35m[COPY]\033[0m'
        )
    )

    print(f'\033[33m[CHECK]\033[0m searching for images to optimize \033[31m(size > {int(args.max_size)}KB)\033[0m')
    unoptimized_images = list(filter(lambda i: i.stat().st_size > int(args.max_size) * 1024, copied_images))

    if len(unoptimized_images) > 0:
        res = list(
            tqdm(
                iterable=pool.imap(resize_image, unoptimized_images),
                total=len(unoptimized_images),
                desc='\033[35m[OPTIMIZING]\033[0m'
            )
        )
        print(f'\n\033[32m[INFO]\033[0m the process saved \033[31m{round(sum(res) / (1024 * 1024 * 1024), 3)}GB\033[0m')
    print(f'\033[32m[INFO]\033[0m images found in \033[36m{args.path}\033[0m: \033[31m{len(found_images)} images\033[0m')
    print(f'\033[32m[INFO]\033[0m found \033[31m{len(unoptimized_images)} images\033[0m larger than \033[31m{int(args.max_size)}KB\033[0m')
    print(f'\033[32m[INFO]\033[0m total time taken: \033[31m{round((time.time()-t)/60, 2)} minutes\033[0m')
