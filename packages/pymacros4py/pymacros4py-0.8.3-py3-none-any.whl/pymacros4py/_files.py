import os
import tempfile
import subprocess
from typing import TypeAlias, Optional
from dataclasses import dataclass, asdict


FileName: TypeAlias = str | bytes | os.PathLike


@dataclass
class FileOptions:
    """Options as they can be used for opening a file. See Python function *open*."""

    encoding: Optional[str] = None
    errors: Optional[str] = None
    newline: Optional[str] = None


file_options = FileOptions(None, None, None)
""" Options used for reading and writing files. See Python function *open*. """


def read_file(in_file_name: FileName, finally_remove: bool = False) -> str:
    """Load text from *in_file_name* using the chosen *file_options*.
    If option *remove_on_error* is set to True and an exception occurs,
    remove the file."""
    try:
        with open(in_file_name, **asdict(file_options)) as f_in:
            s_in = f_in.read()
    finally:
        if finally_remove:
            os.remove(in_file_name)
    return s_in


def write_file(out_file_name: FileName, content: str) -> None:
    """Write text to *out_file_name* using the chosen *file_options*."""
    with open(out_file_name, "w", **asdict(file_options)) as f_out:
        f_out.write(content)


def write_to_tempfile(content: str) -> str:
    """Write text to a temporary file using the chosen *file_options*
    and return the path of the file as str."""
    tmp_file, tmp_file_name = tempfile.mkstemp(text=True)
    os.close(tmp_file)

    try:
        write_file(tmp_file_name, content)
    except Exception as e:  # pragma: no cover
        os.remove(tmp_file_name)
        raise e

    return str(tmp_file_name)


def run_process_with_file(args: list[str], path_str: str) -> None:
    """Run the command described by *args* (compare subprocess.run)
    using *subprocess.run* and capture both stdout and stderr. If a
    *subprocess.CalledProcessError is raised, print the captured output
    and print an error messages that hints to file *path_str*.

    Example:
    pymacros4py.run_on_tempfile(["black", "path_to_file"], "path_to_file")
    """
    try:
        subprocess.run(
            args,
            # capture_output=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding="utf8",
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(
            "\n"
            "The called process raised an exception.\n"
            "The file it operated on starts here:\n"
            f'  File "{path_str}", line 0'
        )
        print("The process returned as output:")
        print(str(e.output))
        raise
