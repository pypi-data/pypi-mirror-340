"""本模块包含库所需常用函数"""

import email
import fnmatch
import hashlib
import logging
import pathlib
import re
import ssl
import subprocess
import tarfile
import time
import typing
import urllib
import zipfile
from pathlib import Path
from typing import List
from typing import Optional
from urllib.parse import urlparse

import requests
from packaging import requirements
from packaging.requirements import InvalidRequirement
from packaging.requirements import Requirement

from fspacker import config
from fspacker.simplifiers import get_simplify_options
from fspacker.trackers import perf_tracker


def calc_checksum(filepath: pathlib.Path, block_size: int = 4096) -> str:
    """计算文件校验和"""

    hash_method = hashlib.sha256()
    logging.info(f"计算文件校验和: [green underline]{filepath.name}[/] [bold green]:heavy_check_mark:")

    try:
        with open(filepath, "rb") as file:
            for chunk in iter(lambda: file.read(block_size), b""):
                hash_method.update(chunk)

    except FileNotFoundError:
        logging.error(f"文件不存在: [red underline]{filepath}[/] [bold red]:white_exclamation_mark:")
        return ""
    except OSError as e:
        logging.error(f"读取文件 IO 错误: [red underline]{filepath}: {e}[/] [bold red]:white_exclamation_mark:")
        return ""

    checksum = hash_method.hexdigest()
    logging.debug(f"校验和计算值: [green underline]{checksum}[/] [bold green]:heavy_check_mark:")
    return checksum


def check_url_access_time(url: str) -> float:
    """测试 url 访问时间"""

    start = time.perf_counter()
    try:
        response = requests.get(url, timeout=2)
        response.raise_for_status()
        time_used = time.perf_counter() - start
        logging.info(f"地址 [[green]{url}[/]] 访问时间: [green] {time_used:.2f}s")
        return time_used
    except requests.exceptions.RequestException:
        logging.info(f"地址 [[red bold]{url}[/]] 访问超时")
        return -1


def get_fastest_url(urls: typing.Dict[str, str]) -> str:
    """获取 Embed python 最快访问链接地址"""

    min_time, fastest_url = 10.0, ""
    for embed_url in urls.values():
        time_used = check_url_access_time(embed_url)
        if time_used > 0:
            if time_used < min_time:
                fastest_url = embed_url
                min_time = time_used

    logging.info(f"找到最快地址: [[green bold]{fastest_url}[/]]")
    return fastest_url


def get_fastest_embed_url() -> str:
    json_config = config.get_json_config()

    if fastest_url := json_config.get("url.embed", ""):
        return fastest_url
    else:
        fastest_url = get_fastest_url(config.EMBED_URL_PREFIX)
        json_config["url.embed"] = fastest_url
        return fastest_url


def safe_read_url_data(url: str, timeout: int = 10) -> typing.Optional[bytes]:
    """Safely read data from a URL with HTTPS schema.

    Args:
        url: The URL to read from.
        timeout: Connection timeout in seconds.

    Returns:
        The content as bytes if successful, None otherwise.
    """
    parsed_url = urlparse(url)
    allowed_schemes = {"https"}

    try:
        if parsed_url.scheme not in allowed_schemes:
            raise ValueError(f"不支持的 URL scheme: {parsed_url.scheme}")

        context = ssl._create_unverified_context()
        with urllib.request.urlopen(url, timeout=timeout, context=context) as response:
            return response.read(1024 * 1024 * 100)  # limited to 100MB
    except (ValueError, urllib.error.URLError) as e:
        logging.error(f"读取 URL 数据失败: {e}")
        return None


def parse_requirement(req_str: str) -> typing.Optional[requirements.Requirement]:
    """解析需求字符串为Requirement对象"""

    try:
        return requirements.Requirement(req_str)
    except requirements.InvalidRequirement:
        logging.error(f"非法 requirement: {req_str}")
        return None


def _extract_package_version(filename: str) -> str:
    """从文件名提取版本号, 支持任意长度版本号如 20.0 或 1.20.3.4

    适配格式：
       package-1.2.3.tar.gz
       package-20.0-py3-none-any.whl
       Package_Name-1.20.3.4.whl
    """
    # 匹配两种命名格式：
    # 1. 常规格式：package-1.2.3
    # 2. 复杂wheel格式：Package-1.2.3.4-xxx.whl
    version_pattern = r"""
        (?:^|-)                   # 开头或连接符
        (\d+\.\d+(?:\.\d+)*)      # 版本号核心（至少两段数字）
        (?=-|\.|_|$)              # 后接分隔符或结束
    """
    match = re.search(version_pattern, filename, re.VERBOSE)
    return match.group(1) if match else "0.0.0"  # 默认返回最低版本


def _is_version_satisfied(cached_file: pathlib.Path, req: requirements.Requirement) -> bool:
    """检查缓存文件版本是否满足需求"""

    if not req.specifier:
        return True  # 无版本约束

    version = _extract_package_version(cached_file.name)
    return version in req.specifier


def get_cached_package(req: requirements.Requirement) -> typing.Optional[pathlib.Path]:
    """获取满足版本约束的缓存文件"""

    package_name = req.name.lower().replace("-", "_")  # 包名大小写不敏感
    pattern = f"{package_name}-*" if not req.specifier else f"{package_name}-[0-9]*"

    for cached_file in config.get_libs_dir().glob(pattern):
        if cached_file.suffix in (".whl", ".gz", ".zip"):
            if _is_version_satisfied(cached_file, req):
                return cached_file
    return None


def get_fastest_pip_url() -> str:
    json_config = config.get_json_config()

    if fastest_url := json_config.get("url.pip"):
        return fastest_url
    else:
        fastest_url = get_fastest_url(config.PIP_URL_PREFIX)
        json_config["url.pip"] = fastest_url
        return fastest_url


def download_to_libs_dir(req: requirements.Requirement) -> pathlib.Path:
    """下载满足版本的包到缓存"""

    pip_url = get_fastest_pip_url()
    net_loc = urlparse(pip_url).netloc
    libs_dir = config.get_libs_dir()
    libs_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        config.PYTHON_EXE,
        "-m",
        "pip",
        "download",
        "--no-deps",
        "--dest",
        str(libs_dir),
        str(req),  # 使用解析后的Requirement对象保持原始约束
        "--trusted-host",
        net_loc,
        "-i",
        pip_url,
        "--no-deps",
    ]

    subprocess.run(cmd, check=True)
    lib_filepath = get_cached_package(req) or pathlib.Path()
    logging.info(f"下载后库文件: [[green bold]{lib_filepath.name}[/]]")
    return lib_filepath


@perf_tracker
def unpack_whleel(
    wheel_file: pathlib.Path,
    dest_dir: pathlib.Path,
    excludes: typing.Set[str] = None,
    patterns: typing.Set[str] = None,
) -> None:
    excludes = set() if excludes is None else excludes
    patterns = set() if patterns is None else patterns

    excludes = set(excludes) | {"*dist-info/*"}
    with zipfile.ZipFile(wheel_file, "r") as zf:
        for file in zf.namelist():
            if any(fnmatch.fnmatch(file, exclude) for exclude in excludes):
                continue

            if len(patterns):
                if any(fnmatch.fnmatch(file, pattern) for pattern in patterns):
                    zf.extract(file, dest_dir)
                    continue
                else:
                    continue

            zf.extract(file, dest_dir)


@perf_tracker
def install_package(
    req: requirements.Requirement,
    lib_file: pathlib.Path,
    dest_dir: pathlib.Path,
    simplify: bool = False,
) -> None:
    """从缓存安装到site-packages"""
    options = get_simplify_options(req.name)

    if simplify and options:
        excludes, patterns = options.excludes, options.patterns
        logging.info(f"找到简化目标库: {req.name}, {options.excludes=}, {options.patterns=}")
    else:
        excludes, patterns = None, None

    if lib_file.suffix == ".whl":
        unpack_whleel(lib_file, dest_dir, excludes, patterns)
    else:
        cmds = [config.PYTHON_EXE, "-m", "pip", "install", str(lib_file.absolute()), "-t", str(dest_dir)]
        logging.info(f"调用命令: [green bold]{cmds}")
        subprocess.run(cmds, check=True)


class RequirementParser:
    @staticmethod
    def normalize_requirement_string(req_str: str) -> Optional[str]:
        """
        规范化需求字符串，处理以下特殊情况：
        1. 括号包裹的版本：shiboken2 (==5.15.2.1) -> shiboken2==5.15.2.1
        2. 不规范的版本分隔符：package@1.0 -> package==1.0
        3. 移除多余空格和注释
        """
        # 移除注释和首尾空格
        req_str = re.sub(r"#.*$", "", req_str).strip()
        if not req_str:
            return None

        # 处理括号包裹的版本 (常见于PySide生态)
        if "(" in req_str and ")" in req_str:
            req_str = re.sub(r"$([^)]+)$", r"\1", req_str)

        # 替换不规范的版本分隔符
        req_str = re.sub(r"([a-zA-Z0-9_-]+)@([0-9.]+)", r"\1==\2", req_str)

        # 标准化版本运算符（处理 ~= 和意外的空格）
        req_str = re.sub(r"~=\s*", "~=", req_str)
        req_str = re.sub(r"([=<>!~]+)\s*", r"\1", req_str)

        # 标准化版本运算符（处理 ; 以后的内容）
        req_str = re.sub(r" ; .*", "", req_str)

        return req_str.strip()

    @classmethod
    def parse_requirement(cls, req_str: str) -> Optional[Requirement]:
        """安全解析需求字符串为Requirement对象"""
        normalized = cls.normalize_requirement_string(req_str)
        if not normalized:
            return None

        try:
            # 分离环境标记
            if ";" in normalized:
                req_part, marker = normalized.split(";", 1)
                req = Requirement(req_part.strip())
                req.marker = marker.strip()
            else:
                req = Requirement(normalized)
            return req
        except InvalidRequirement as e:
            print(f"⚠  Failed to parse '{req_str}': {str(e)}")
            return None


class PackageFileDependencyAnalyzer:
    @staticmethod
    def extract_metadata(package_path: Path) -> Optional[email.message.Message]:
        """从包文件中提取元数据"""
        if package_path.suffix == ".whl":
            with zipfile.ZipFile(package_path) as z:
                for name in z.namelist():
                    if name.endswith(".dist-info/METADATA"):
                        metadata = z.read(name).decode("utf-8")
                        return email.message_from_string(metadata)

        elif package_path.suffix in (".tar.gz", ".zip"):
            opener = tarfile.open if package_path.suffix == ".gz" else zipfile.ZipFile
            with opener(package_path) as archive:
                for member in archive.getmembers():
                    if member.name.endswith(("PKG-INFO", "METADATA")):
                        fileobj = archive.extractfile(member)
                        metadata = fileobj.read().decode("utf-8")
                        return email.message_from_string(metadata)
        return None

    @classmethod
    def analyze_dependencies(cls, package_path: Path) -> List[Requirement]:
        metadata = cls.extract_metadata(package_path)
        if not metadata:
            return []

        requirements = []
        for field in ["Requires-Dist", "Requires"]:
            for req_str in metadata.get_all(field, []):
                req = RequirementParser.parse_requirement(req_str)
                if req:
                    requirements.append(req)
        return requirements

    @classmethod
    def analyze_to_list(cls, package_path: Path) -> List[Requirement]:
        """返回Requirement对象列表（去重）"""
        return list(cls.analyze_dependencies(package_path).values())


__analyzer = PackageFileDependencyAnalyzer()


def analyze_package_file_dependencies(package_file_path: pathlib.Path):
    global __analyzer

    return __analyzer.analyze_dependencies(package_file_path)
