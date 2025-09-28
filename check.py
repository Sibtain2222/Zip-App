import os 
import tkinter as tk 
from tkinter import filedialog
from pathlib import Path
import zipfile


root= tk.Tk()
root.withdraw()


# //////////////////////////////////////////////////////

# now zip the file and folder

def compress_to_zip(input_path, output_file=None):
    if not output_file:
        output_file = input_path + ".zip"

    with zipfile.ZipFile(output_file, "w", zipfile.ZIP_DEFLATED) as zipf:
        if os.path.isfile(input_path):
            # Just one file
            zipf.write(input_path, os.path.basename(input_path))
        else:
            # Walk through folder and add files
            for root, _, files in os.walk(input_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    if not os.path.isfile(file_path):
                        continue
                    # Store relative path inside the zip
                    arcname = os.path.relpath(file_path, start=input_path)
                    zipf.write(file_path, arcname)
    return output_file
# ////////////////////////////////
    # print(f"✅ Compressed: {input_path} → {output_file}")


# Example usage
# compress_to_zip("myfile.txt")        # single file
# compress_to_zip("myfolder")          # whole folder












# //////////////////////////////////////////////////////////
# for folder
# folder_path=filedialog.askdirectory(title="open folder ")
# archive_path = compress_to_zip(folder_path)
# def get_folder_size(folder):
#     total=0
#     for file in Path(folder).rglob('*'):
#        try:
#            if file.is_file():
#                total+=file.stat().st_size
#        except FileNotFoundError:
#            continue
#     return total / (1024 * 1024) # in MB

# class ByteSize(int):

#     _KB = 1024
#     _suffixes = 'B', 'KB', 'MB', 'GB', 'PB'

#     def __new__(cls, *args, **kwargs):
#         return super().__new__(cls, *args, **kwargs)

#     def __init__(self, *args, **kwargs):
#         self.bytes = self.B = int(self)
#         self.kilobytes = self.KB = self / self._KB**1
#         self.megabytes = self.MB = self / self._KB**2
#         self.gigabytes = self.GB = self / self._KB**3
#         self.petabytes = self.PB = self / self._KB**4
#         *suffixes, last = self._suffixes
#         suffix = next((
#             suffix
#             for suffix in suffixes
#             if 1 < getattr(self, suffix) < self._KB
#         ), last)
#         self.readable = suffix, getattr(self, suffix)

#         super().__init__()

#     def __str__(self):
#         return self.__format__('.2f')

#     def __repr__(self):
#         return '{}({})'.format(self.__class__.__name__, super().__repr__())

#     def __format__(self, format_spec):
#         suffix, val = self.readable
#         return '{val:{fmt}} {suf}'.format(val=val, fmt=format_spec, suf=suffix)

#     def __sub__(self, other):
#         return self.__class__(super().__sub__(other))

#     def __add__(self, other):
#         return self.__class__(super().__add__(other))
    
#     def __mul__(self, other):
#         return self.__class__(super().__mul__(other))

#     def __rsub__(self, other):
#         return self.__class__(super().__sub__(other))

#     def __radd__(self, other):
#         return self.__class__(super().__add__(other))
    
#     def __rmul__(self, other):
#         return self.__class__(super().__rmul__(other))   
# # //////////////////////////////////////////////////////


# if folder_path:
#     print(f"Original folder size: {get_folder_size(folder_path):.2f} MB")

# # Compressed archive size
#     compressed_size = os.path.getsize(archive_path) / (1024*1024)
#     print(f"Compressed archive size: {compressed_size:.2f} MB")

# else:
#     print('not found ')



# ////////////////////////////////
# for files 
def convert_bytes(num):
    """
    this function will convert bytes to MB.... GB... etc
    """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0


def file_size(file_path):
    """
    this function will return the file size
    """
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return convert_bytes(file_info.st_size)



file_path=filedialog.askopenfilename(filetypes=[("All Files","*")],initialdir="/home",title="open_file")
achieve_path=compress_to_zip(file_path)
if file_path :
   
    print(f"{file_path} {file_size(file_path)}")
    print(f"Compressed archive size: {file_size(achieve_path)}")
    
else:
    print('not found ')



