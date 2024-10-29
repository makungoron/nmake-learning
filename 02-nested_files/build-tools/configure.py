import os
from pathlib import Path, WindowsPath

SRC_DIRNAME = 'src'
OBJ_DIRNAME = 'obj'
BIN_DIRNAME = 'bin'
TARGET_FILENAME = '02-nested_files.exe'
OUTPUT_FILENAME = 'makefile.nmake'
OUTPUT_PATH = Path(__file__).parent.parent


SEP = os.sep

def get_cpp_dirlist(src_dir: Path) -> list[Path]:
    # CPPが入っているサブディレクトリの一覧を
    ret = sorted(list(set([p.parent for p in src_dir.glob('**/*.cpp')])))
    return ret

def get_cpp_filelist(src_dir: Path) -> list[Path]:
    ret = sorted(list(src_dir.glob('**/*.cpp')))
    return ret


def convert_src_to_obj_dir(p: Path) -> Path:
    if isinstance(p, WindowsPath):
        subdir_list = str(p).split('\\', 1)
        subdir = '' if len(subdir_list) == 1 else subdir_list[-1]
        ret = WindowsPath(OBJ_DIRNAME, subdir)
    else:
        subdir_list = str(p).split('/', 1)
        subdir = '' if len(subdir_list) == 1 else subdir_list[-1]
        ret = Path(OBJ_DIRNAME, subdir)
    return ret

def make_compile_block(src_dir: Path, obj_dir: Path) -> str:
    src_dir = str(src_dir)
    obj_dir = str(obj_dir)

    if src_dir[-1] != SEP:
        src_dir += SEP
    if obj_dir[-1] != SEP:
        obj_dir += SEP

    return '\n'.join([
        '{' + src_dir + '}.cpp{' + obj_dir + '}.obj:',
        '\t@echo Compiling $< $@',
        '\t@echo $(@D)', # これは不要
        '\t@if NOT EXIST $(@D) mkdir $(@D)',
        '\t$(CPP) /nologo /c $(CFLAGS) $< /Fo"$@"'
    ])


def main():
    project_root_dir = Path(__file__).parent.parent
    src_dir = project_root_dir / SRC_DIRNAME
    cpp_files = get_cpp_filelist(src_dir)
    cpp_files = [file.relative_to(project_root_dir) for file in cpp_files]
    src_dirs = [file.relative_to(project_root_dir) for file in get_cpp_dirlist(src_dir)]
    print('cpp subdirectories:', *src_dirs)
    print(*cpp_files)

    CPP = 'CPP = cl.exe'
    CFLAGS = 'CFLAGS = /EHsc /W4 /Iinclude  # Include any additional flags or directories'

    SRC_DIR = f'SRC_DIR = {SRC_DIRNAME}'
    OBJ_DIR = f'OBJ_DIR = {OBJ_DIRNAME}'
    BIN_DIR = f'BIN_DIR = {BIN_DIRNAME}'
    TARGET = f'TARGET = {TARGET_FILENAME}'

    SRC_DIRS = 'SRC_DIRS = ' + ' '.join([str(p) for p in src_dirs])
    print(SRC_DIRS)

    obj_dirs = [convert_src_to_obj_dir(p) for p in src_dirs]
    OBJ_DIRS = 'OBJ_DIRS = ' + ' '.join([str(p) for p in obj_dirs])
    print(OBJ_DIRS)

    SRCS = 'SRCS = ' + ' '.join([str(p) for p in cpp_files])
    # NOTE: 区切り文字はWindowsPathの場合バックスラッシュになる

    OBJS = 'OBJS = '
    for cpp_file in cpp_files:
        # src/ を obj/ に置き換える
        # ソースコードや深い階層にsrcという名前があると困るので、
        # 大元のsrcフォルダ名のみ書き換えるようにしている
        if isinstance(cpp_file, WindowsPath):
            subdir_list = str(cpp_file.parent).split('\\', 1)
            subdir = '' if len(subdir_list) == 1 else subdir_list[-1]
            obj_file = WindowsPath(OBJ_DIRNAME, subdir, cpp_file.stem + '.obj')
            print(str(cpp_file.parent).split('\\', 1))
        else:
            subdir_list = str(cpp_file.parent).split('\\', 1)
            subdir = '' if len(subdir_list) == 1 else subdir_list[-1]
            obj_file = Path(OBJ_DIRNAME, subdir, cpp_file.stem + '.obj')
        OBJS += str(obj_file) + ' '
    OBJS = OBJS.strip()


    COMPILE_BLOCKS = '\n\n'.join([
        make_compile_block(src_dir, obj_dir)
        for src_dir, obj_dir in zip(src_dirs, obj_dirs)
    ])


    CLEAN_PHONY = '\n'.join([
        'clean:',
        f'\tdel /Q /S $(OBJ_DIR){SEP}*.obj',
        f'\tdel /Q $(BIN_DIR){SEP}$(TARGET)'
    ])

    makefile_components: list[str] = [
        '# Makefile.nmake',
        '',
        '# Compiler and flags',
        CPP,
        CFLAGS,
        '',

        '# Directories',
        SRC_DIR,
        OBJ_DIR,
        BIN_DIR,
        '',
        '# Output executable',
        TARGET,
        '',
        SRC_DIRS,
        OBJ_DIRS,
        SRCS,
        OBJS,
        '',
        '!MESSAGE SRCS = $(SRCS)',
        '!MESSAGE OBJS = $(OBJS)',
        '',
        'all: $(TARGET)',
        '$(TARGET) : $(OBJS)',
        '\t@echo Linking...',
        '\t@if NOT EXIST $(@D) mkdir $(@D)',
        f'\t$(CPP) /nologo $(OBJS) /Fe"$(BIN_DIR){SEP}$(TARGET)"',
        '',
        COMPILE_BLOCKS,
        '',
        '# Clean up build files',
        CLEAN_PHONY
    ]
    out_txt = '\n'.join(makefile_components)

    print(out_txt)

    out_path = OUTPUT_PATH / OUTPUT_FILENAME
    out_path.write_text(out_txt)
    print('makefile generated.')

if __name__ == '__main__':
    main()
