import logging
import pathlib
import re
import shutil
import string
import time
import typing
from abc import ABC
from abc import abstractmethod

import typer
from packaging.requirements import Requirement

from fspacker import config
from fspacker.exceptions import ProjectParseError
from fspacker.models import PackMode
from fspacker.parsers import parse_pyproject
from fspacker.utils import analyze_package_file_dependencies
from fspacker.utils import calc_checksum
from fspacker.utils import download_to_libs_dir
from fspacker.utils import get_cached_package
from fspacker.utils import get_fastest_embed_url
from fspacker.utils import install_package
from fspacker.utils import parse_requirement
from fspacker.utils import safe_read_url_data


class Packer:
    """打包工具"""

    def __init__(
        self,
        root_dir: pathlib.Path,
        dest_dir: pathlib.Path,
        mode: PackMode,
    ):
        self.mode = mode

        self.root_dir = root_dir
        self.dest_dir = dest_dir
        self.project_info = parse_pyproject(root_dir)

        # 打包器集合, 注意打包顺序
        self.spec_packers: typing.Dict[str, BaseSpecPacker] = dict(
            project_folder=ProjectFolderPacker(self),
            source_res=SourceResPacker(self),
            library=LibraryPacker(self),
            builtin=BuiltInLibPacker(self),
            exe_entry=ExeEntryPacker(self),
            runtime=RuntimePacker(self),
        )

    def pack(self):
        if not self.project_info:
            raise ProjectParseError("项目信息无效")

        logging.info(f"启动构建, 源码根目录: [[green underline]{self.root_dir}[/]]")
        if not self.root_dir.exists():
            raise ProjectParseError(f"目录路径不存在: [bold red]{self.root_dir}")

        t0 = time.perf_counter()

        for _, spec_packer in self.spec_packers.items():
            logging.info(spec_packer)
            spec_packer.pack()

        logging.info(f"打包完成! 总用时: [{time.perf_counter() - t0:.4f}]s.")


class BaseSpecPacker(ABC):
    """针对特定场景打包工具"""

    NAME = "基础打包"

    def __init__(self, parent: Packer):
        self.parent = parent

    def __repr__(self):
        return f"调用 [[green]{self.NAME} - {self.__class__.__name__}[/]] 打包工具"

    @property
    def root_dir(self):
        return self.parent.root_dir

    @property
    def dest_dir(self):
        return self.parent.dest_dir

    @property
    def mode(self):
        return self.parent.mode

    @property
    def project_info(self):
        return self.parent.project_info

    @property
    def dependencies(self):
        return self.project_info.dependencies

    @abstractmethod
    def pack(self):
        pass


class ProjectFolderPacker(BaseSpecPacker):
    NAME = "项目结构打包"

    def pack(self):
        if self.mode.rebuild:
            logging.info(f"清理旧文件: [[green]{self.dest_dir}[/]]")
            try:
                shutil.rmtree(self.dest_dir, ignore_errors=True)
            except OSError as e:
                logging.info(f"清理失败: [red bold]{e}")

        for directory in (self.dest_dir,):
            logging.info(f"创建文件夹: [[purple]{directory.name}[/]]")
            directory.mkdir(parents=True, exist_ok=True)


# int file template
INT_TEMPLATE = string.Template(
    """\
import sys, os
sys.path.append(os.path.join(os.getcwd(), "src"))
from $SRC import main
main()
"""
)

INT_TEMPLATE_QT = string.Template(
    """\
import sys, os
import $LIB_NAME

qt_dir = os.path.dirname($LIB_NAME.__file__)
plugin_path = os.path.join(qt_dir, "plugins" , "platforms")
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = plugin_path
sys.path.append(os.path.join(os.getcwd(), "src"))
from $SRC import main
main()
"""
)


class ExeEntryPacker(BaseSpecPacker):
    NAME = "入口程序打包"

    def pack(self):
        name = self.project_info.normalized_name

        exe_filename = "gui.exe" if self.project_info.is_gui_project() else "console.exe"
        src_exe_path = config.DIR_ASSETS / exe_filename
        assert src_exe_path.exists()
        dst_exe_path = self.dest_dir / f"{name}.exe"

        logging.info(
            f"打包目标类型: {'[green bold]窗口' if self.project_info.is_gui_project() else '[black bold]控制台'}[/]"
        )
        logging.info(
            f"复制可执行文件: [green underline]{src_exe_path.name} -> "
            f"{dst_exe_path.relative_to(self.root_dir)}[/] [bold green]:heavy_check_mark:"
        )
        shutil.copy(src_exe_path, dst_exe_path)

        dst_int_path = self.dest_dir / f"{name}.int"

        logging.info(
            f"创建 int 文件: [green underline]{name}.int -> {dst_int_path.relative_to(self.root_dir)}"
            f"[/] [bold green]:heavy_check_mark:"
        )

        for lib_name in ["PySide2", "PyQt5", "PySide6", "PyQt6"]:
            if self.project_info.contains_libname(lib_name):
                content = INT_TEMPLATE_QT.substitute(SRC=f"src.{name}", LIB_NAME=lib_name)
                break
        else:
            content = INT_TEMPLATE.substitute(SRC=f"src.{name}")

        with open(dst_int_path, "w") as f:
            f.write(content)


class RuntimePacker(BaseSpecPacker):
    NAME = "运行时打包"

    def pack(self):
        runtime_dir = self.dest_dir / "runtime"
        embed_file_path = config.PATH_EMBED_FILE

        if (runtime_dir / "python.exe").exists():
            logging.warning("目标文件夹 [purple]runtime[/] 已存在, 跳过 [bold green]:heavy_check_mark:")
            return

        if embed_file_path.exists():
            logging.info("找到本地 [green bold]embed 压缩包")
            logging.info(f"检查校验和: [green underline]{embed_file_path.name} [bold green]:heavy_check_mark:")
            src_checksum = config.get_json_config().get("file.embed.checksum", "")
            dst_checksum = calc_checksum(embed_file_path)

            if src_checksum == dst_checksum:
                logging.info("校验和一致, 使用[bold green] 本地运行时 :heavy_check_mark:")
            else:
                logging.info("校验和不一致, 重新下载")
                self._fetch_runtime()
        else:
            if not self.mode.offline:
                logging.info("非离线模式, 获取运行时")
                self._fetch_runtime()
            else:
                logging.error(f"离线模式且本地运行时不存在: [bold red]{embed_file_path}[/], 退出")
                return

        logging.info(
            f"解压 runtime 文件: [green underline]{config.PATH_EMBED_FILE.name} "
            f"-> {runtime_dir.relative_to(self.root_dir)}[/] [bold green]:heavy_check_mark:"
        )
        shutil.unpack_archive(config.PATH_EMBED_FILE, runtime_dir, "zip")

    def _fetch_runtime(self):
        fastest_url = get_fastest_embed_url()
        archive_url = f"{fastest_url}{config.PYTHON_VER}/{config.EMBED_FILE_NAME}"
        json_config = config.get_json_config()

        if not archive_url.startswith("https://"):
            logging.error(f"无效 url 路径: {archive_url}")
            typer.Exit(code=2)

        content = safe_read_url_data(archive_url)
        if content is None:
            logging.error("下载运行时失败")
            typer.Exit(code=2)

        logging.info(f"从地址下载运行时: [[green bold]{fastest_url}[/]]")
        t0 = time.perf_counter()

        with open(config.PATH_EMBED_FILE, "wb") as f:
            f.write(content)

        download_time = time.perf_counter() - t0
        logging.info(f"下载完成, 用时: [green bold]{download_time:.2f}s")

        checksum = calc_checksum(config.PATH_EMBED_FILE)
        logging.info(f"更新校验和 [{checksum}]")
        json_config["file.embed.checksum"] = checksum


class SourceResPacker(BaseSpecPacker):
    NAME = "源码 & 资源打包"

    # 忽视清单
    IGNORE_ENTRIES = ["dist-info", "__pycache__", "site-packages", "runtime", "dist", ".venv"]

    def _valid_file(self, filepath: pathlib.Path) -> bool:
        return all(x not in str(filepath) for x in self.IGNORE_ENTRIES)

    def pack(self):
        dest_dir = self.dest_dir / "src"
        source_files = list(file for file in self.root_dir.rglob("*.py") if self._valid_file(file))

        for source_file in source_files:
            with open(source_file, encoding="utf8") as f:
                content = "\n".join(f.readlines())
            if "def main():" in content:
                source_folder = source_file.absolute().parent
                break
        else:
            logging.error("未找到入口 Python 文件, 退出")
            typer.Exit(code=2)

        dest_dir.mkdir(parents=True, exist_ok=True)
        for entry in source_folder.iterdir():
            dest_path = dest_dir / entry.name

            if entry.is_file():
                logging.info(f"复制目标文件: [green underline]{entry.name}[/] [bold green]:heavy_check_mark:")
                shutil.copy2(entry, dest_path)
            elif entry.is_dir():
                if entry.stem not in self.IGNORE_ENTRIES:
                    logging.info(f"复制目标文件夹: [purple underline]{entry.name}[/] [bold purple]:heavy_check_mark:")
                    shutil.copytree(entry, dest_path, dirs_exist_ok=True)
                else:
                    logging.info(f"目标文件夹 [black]{entry.name}[/] 已存在, 跳过")


class LibraryPacker(BaseSpecPacker):
    NAME = "依赖库打包"

    def _install_lib(self, req: Requirement):
        dest_dir = self.dest_dir / "site-packages"
        dest_dir.mkdir(parents=True, exist_ok=True)

        lib_folder = dest_dir / req.name
        if lib_folder.exists():
            logging.info(f"依赖库 [black]{req.name}[/] 已存在, 跳过")
            return None

        logging.info(f"打包依赖: [green bold]{req}")
        cached_file = get_cached_package(req)
        if cached_file:
            logging.info(f"找到本地满足要求的依赖: [green]{cached_file.name}")
        else:
            logging.info(f"下载依赖: [green]{req}")
            cached_file = download_to_libs_dir(req)

        if cached_file.is_file():
            logging.info(f"安装依赖: [green]{cached_file.name}")
            install_package(req, cached_file, dest_dir, simplify=self.parent.mode.simplify)
            return cached_file
        else:
            logging.error(f"处理依赖失败: {req}")
            return None

    def pack(self):
        req_libs = self.dependencies
        logging.info(f"分析一级依赖库: [green bold]{req_libs}")
        for req_lib in req_libs:
            req = parse_requirement(req_lib)
            logging.info(f"打包依赖: [green bold]{req}")

            cached_file = self._install_lib(req)
            if cached_file:
                secondary_reqs = analyze_package_file_dependencies(cached_file)
                logging.info(f"分析二级依赖: [green]{secondary_reqs}")
                for secondary_req in secondary_reqs:
                    self._install_lib(secondary_req)

    @staticmethod
    def normalize_package_name(dep_requirement: str) -> typing.Tuple[str, str]:
        """标准化包名，去除版本约束，返回名称和版本"""

        name, version = re.split(r"[><=!~]", dep_requirement)
        return name.strip(), version.strip()

    @staticmethod
    def is_cached(package_req: str) -> bool:
        """检查包是否已存在于缓存"""
        package_name, package_ver = LibraryPacker.normalize_package_name(package_req)

        return any(
            pkg.name.startswith(f"{package_name}-") and pkg.suffix in (".whl", ".tar.gz", ".zip")
            for pkg in config.get_cache_dir().glob(f"{package_name}-{package_ver}")
        )


class BuiltInLibPacker(BaseSpecPacker):
    NAME = "内置依赖库打包"

    def pack(self):
        if self.mode.use_tk:
            tk_lib = config.DIR_ASSETS / "tkinter-lib.zip"
            tk_package = config.DIR_ASSETS / "tkinter.zip"
            logging.info(f"解压tk文件: [green]{tk_lib}[/], [green]{tk_package}")
            shutil.unpack_archive(tk_lib, self.dest_dir, "zip")
            shutil.unpack_archive(tk_package, self.dest_dir / "site-packages", "zip")
