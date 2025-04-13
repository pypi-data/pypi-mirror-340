import pytest

from fspacker.parsers import parse_pyproject


@pytest.mark.parametrize(
    "dirname, dependencies",
    [
        ("ex01_helloworld", ["defusedxml>=0.7.1", "orderedset>=2.0.3"]),
        ("ex02_office", ["pypdf>=5.4.0"]),
        ("ex03_tkinter", ["pyyaml>=6.0.2"]),
        ("ex04_pyside2", ["pyside2>=5.15.2.1"]),
        ("ex11_pygame", ["pygame>=2.6.1"]),
    ],
)
def test_parse_dependencies(dir_examples, dirname, dependencies):
    project_dir = dir_examples / dirname
    assert project_dir.exists()

    project_info = parse_pyproject(project_dir)
    assert project_info.name == dirname.replace("_", "-")
    assert project_info.dependencies == dependencies


def test_parse_project_info(dir_examples):
    dir_ex01 = dir_examples / "ex04_pyside2"
    assert dir_ex01.exists()

    project_info = parse_pyproject(dir_ex01)
    assert project_info.name == "ex04-pyside2"
    assert project_info.dependencies == [
        "pyside2>=5.15.2.1",
    ]
    assert project_info.contains_libname("pyside2")
    assert project_info.contains_libname("PySide2")
    assert not project_info.contains_libname("PyQt5")
