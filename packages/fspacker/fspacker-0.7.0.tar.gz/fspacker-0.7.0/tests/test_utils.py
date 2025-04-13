import hashlib
import pathlib

from fspacker.utils import calc_checksum


def test_calc_checksum_valid_file(tmpdir):
    """Calculate checksum for a valid file."""

    test_file = tmpdir / "test_file.txt"
    test_file.write("test content")
    checksum = calc_checksum(pathlib.Path(test_file))

    expected_checksum = hashlib.sha256(b"test content").hexdigest()
    assert checksum == expected_checksum


def test_calc_checksum_file_not_found():
    """Calculate checksum for a non-existent file."""

    non_existent_file = pathlib.Path("non_existent_file.txt")
    checksum = calc_checksum(non_existent_file)
    assert checksum == ""


def test_calc_checksum_empty_file(tmpdir):
    """Calculate checksum for an empty file."""
    test_file = tmpdir / "empty_file.txt"
    test_file.write("")
    checksum = calc_checksum(pathlib.Path(test_file))

    expected_checksum = hashlib.sha256(b"").hexdigest()
    assert checksum == expected_checksum


def test_calc_checksum_different_block_size(tmpdir):
    """Calculate checksum with a different block size."""
    test_file = tmpdir / "test_file.txt"
    test_file.write("test content")
    checksum = calc_checksum(pathlib.Path(test_file), block_size=2)

    expected_checksum = hashlib.sha256(b"test content").hexdigest()
    assert checksum == expected_checksum
