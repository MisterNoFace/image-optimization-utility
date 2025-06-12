# Image Optimization Utility  
A script to optimize images located in a folder. The script includes the following features:
- Recursive directory scan  
- Resize images larger than a certain size  
- Detect images larger than 300kB (or a custom threshold) and reduce their size  
- Save optimized images in a separate folder  
- Final report: how many images were analyzed, how many optimized, total time spent  

## Modules  
The script uses Python 3.13 but is also compatible with Python 3.8.<br>  
It uses the following modules:  
- `os, time, shutil, multiprocessing, subprocess, argparse`: standard Python modules.  
- `pathlib, PIL, tqdm`: additional modules to be installed via pip.  

These modules are updated automatically by the program when it runs.

## Usage and Parameters  
To start scanning for images, run the script with Python and specify the folder path using the `--path` argument:

> **`python.exe image_optimizer.py --path path/to/folder`**

**The `--path` argument is the only required parameter**, since it indicates the folder path to scan.  
However, the following optional parameters are available:

- `-q` or `--quality`: sets the final image quality, **from 0 to 100**.<br>
  0 results in low quality (pixelated), and 100 preserves the best quality. **Default is 50.**


- `-dpi` or `--dpi`: sets the number of Dots Per Inch, a parameter that only affects printing. **Default is 72.**


- `-c` or `--compression`: sets how much the image should be compressed, **from 0 to 9**.  
  0 applies no compression (faster), and 9 applies maximum compression. **Default is 6.**


- `-m` or `--max-size`: the minimum size (in kB) an image must have to be compressed. **Default is 300kB.**


- `-n` or `--name`: sets the suffix for the output folder name. Default is `COPY`.<br>

For example, if you run the command: `image_optimizer.py --path C:\Users\...\image_folder` the program will create a folder at: `C:\Users\...\image_folder_COPY`, because the `--name` parameter defaults to `COPY`.

If you specify a custom suffix, the resulting folder will have a different name: `image_optimizer.py --path C:\Users\...\image_folder --name TEST` creates a folder at: `C:\Users\...\image_folder_TEST`

> So, **it is recommended to set a folder suffix** each time you run the scan, **to avoid overwriting files from a previous run.**

## How It Works  
Once you specify the folder path, the program will analyze the filesystem starting from that folder: it will scan folders and subfolders for image files.

> **Only images with the following extensions will be recognized and copied: `.png .jpg .jpeg .svg .webp`**

Once all images are found, the program will replicate the folder structure (including subfolders) and create a new folder with the same name as the original, with the suffix defined by the `--name` parameter, and copy all images into that folder.

Finally, the program checks which images exceed 300kB (or the threshold set with `--max-size`): the process involves resizing those images while preserving proportions and partially maintaining quality (which can be adjusted using `--quality`).
