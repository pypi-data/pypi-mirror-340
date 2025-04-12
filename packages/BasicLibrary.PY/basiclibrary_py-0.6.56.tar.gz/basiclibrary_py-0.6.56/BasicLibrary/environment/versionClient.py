"""
 * @file   : versionMate.py
 * @time   : 14:59
 * @date   : 2025/4/12
 * @mail   : 9727005@qq.com
 * @creator: ShanDong Xiedali
 * @company: Less is more.Simple is best!
"""
import os

from BasicLibrary.data.tomlMate import TomlMate
from BasicLibrary.environment.versionHelper import VersionHelper
from BasicLibrary.projectHelper import ProjectHelper


class VersionClient(object):
    @staticmethod
    def increase_patch(pyproject_toml_file_full_path: str = "", version_node_path: str = ""):
        """
        将pyproject.toml中的version节点的patch版本号+1，并保存
        :param pyproject_toml_file_full_path: pyproject.toml文件的全路径
        :param version_node_path: version节点的路径
        :return:
        """
        if not pyproject_toml_file_full_path:
            pyproject_toml_file_full_path = os.path.join(ProjectHelper.get_root_physical_path(), "pyproject.toml")
        pass

        if not version_node_path:
            version_node_path = "project/version"
        pass

        mate = TomlMate(pyproject_toml_file_full_path)
        old_version = mate.get(version_node_path)

        new_version = VersionHelper.increase_patch(old_version)
        mate.set(version_node_path, new_version)

    pass


pass
