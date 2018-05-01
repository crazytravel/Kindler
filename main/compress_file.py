import os
import os.path
import zipfile


def zip_file(file_path, zip_file_path):
    """
    压缩文件为zip
    :param file_path: 被压缩的文件路径，可以是目录
    :param zip_file_path: 压缩后的路径
    :return:
    """
    file_list = []
    if os.path.isfile(file_path):
        file_list.append(file_path)
    else:
        for root, dirs, files in os.walk(file_path):
            for name in files:
                file_list.append(os.path.join(root, name))

    zf = zipfile.ZipFile(zip_file_path, 'w', zipfile.zlib.DEFLATED)
    for tar in file_list:
        arc_name = tar[len(file_path):]
        print(arc_name, tar)
        zf.write(tar, arc_name)
    zf.close()

# def zip_files(file_list):
#     zf = zipfile.ZipFile(zip_file_path, 'w', zipfile.zlib.DEFLATED)
#     for tar in file_list:
#         arc_name = tar[len(file_path):]
#         print(arc_name, tar)
#         zf.write(tar, arc_name)
#     zf.close()


def unzip_file(zip_file_path, unzip_dir):
    """
    解压缩文件
    :param zip_file_path: 压缩文件路径
    :param unzip_dir: 解压路径
    :return:
    """
    try:
        with zipfile.ZipFile(zip_file_path) as zFile:
            zFile.extractall(path=unzip_dir)
    except zipfile.BadZipFile:
        print(zip_file_path + ' is a bad zip file, please check')
