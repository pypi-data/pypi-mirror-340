import unittest
import pymacros4py
import pathlib
import tempfile
import os
import re
import contextlib
import io
import subprocess


class ReadmeExamplesTest(unittest.TestCase):
    def test_expansion_result(self) -> None:
        """
        Test that all README examples have the specified expansion script and result
        """
        for template_path in pathlib.Path("tests/data/").glob("doc_*.tpl.py"):
            with self.subTest(template=str(template_path), mode="script"):
                result_file_path = template_path.with_suffix("").with_suffix(
                    ".script.py"
                )
                pp = pymacros4py.PreProcessor()
                result = pp.template_script(str(template_path))
                # Hide internals from the examples for the README.rst
                result = re.sub(r"^ *_macro_.*$\n", "", result, flags=re.MULTILINE)
                if result_file_path.exists():
                    prev_result = pymacros4py._files.read_file(str(result_file_path))
                    self.assertMultiLineEqual(result, prev_result)
                else:
                    with open(result_file_path, "w", encoding="utf-8") as f_out:
                        f_out.write(result)

            with self.subTest(template=str(template_path), mode="expand"):
                result_file_path = template_path.with_suffix("").with_suffix(".py")
                pp = pymacros4py.PreProcessor()
                if result_file_path.exists():
                    result = pp.expand_file(str(template_path))
                    prev_result = pymacros4py._files.read_file(str(result_file_path))
                    self.assertMultiLineEqual(
                        result, prev_result, "In " + str(template_path)
                    )
                else:
                    pp.expand_file_to_file(str(template_path), str(result_file_path))


class ReadmeTest(unittest.TestCase):
    overwrite = False

    def test(self) -> None:
        """
        Test that README.rst is up-to-date. Create, if missing.
        """

        pp = pymacros4py.PreProcessor()
        templates_root = pathlib.Path("tpl")
        for template in templates_root.glob("**/*"):
            if not template.is_file():
                continue
            goal = template.relative_to(templates_root)
            if goal.exists() and not self.overwrite:
                result = pp.expand_file_to_file(
                    str(template), str(goal), diffs_to_result_file=True
                )
                if result:
                    print(result, flush=True)
                    self.fail(str(goal) + " not up to date. See differences above.")
            else:
                pp.expand_file_to_file(str(template), str(goal))


class TestForMentionedButNotDocumentedBehaviour(unittest.TestCase):
    def test_insert_from_with_caching(self) -> None:
        """The README says, that repeated calls of *insert_from*
        with the same file and without parameter *global* leads to re-use
        of already expanded template data. The template generates a random
        number for each time a template is expanded. They equal, if only
        one expansion happened."""
        template_path = "tests/data/testcase_insert_from_with_caching.tpl.py"
        pp = pymacros4py.PreProcessor()
        result = pp.expand_file(template_path).splitlines()
        self.assertEqual(result[0], result[1])

    def test_insert_from_without_caching(self) -> None:
        """The README says, that repeated calls of *insert_from*
        with the same file and with non-None parameter *global* disables
        re-use of already expanded template data. For more see
        test_insert_from_with_caching."""
        template_path = "tests/data/testcase_insert_from_without_caching.tpl.py"
        pp = pymacros4py.PreProcessor()
        result = pp.expand_file(template_path).splitlines()
        self.assertNotEqual(result[0], result[1])

    def test_no_re_import(self) -> None:
        """The README says, that repeated calls of *import_from*
        with the same file is blocked. The template import another template
        that sets a variable to a new random value each time the import
        happens. Then, we can see, whether the second import is prevented."""
        template_path = "tests/data/testcase_import_from_a_second_time.tpl.py"
        pp = pymacros4py.PreProcessor()
        result = pp.expand_file(template_path).splitlines()
        self.assertEqual(result[0], result[1])

    def test_writing_result_files(self) -> None:
        """The README says, that expand_file_to_file can write its results
        to a file. All other tests just verify results, if the output already
        exists in the target file. Thus, this test here tests writing."""
        template_path = "tests/data/doc_templ_and_templ_exp.tpl.py"
        tmp_file, tmp_file_path = tempfile.mkstemp(text=True)
        try:
            pp = pymacros4py.PreProcessor()
            result = pp.expand_file(template_path)
            pp.expand_file_to_file(template_path, tmp_file_path)
            result_in_file = pymacros4py._files.read_file(tmp_file_path)
            self.assertEqual(result, result_in_file)
        finally:
            os.close(tmp_file)

    def test_trace_parsing_with_exception(self) -> None:
        """The README describes exception handling and tracing. The
        indirect expectation is, that an exception does not prevent the
        tracing from working. There is no explicit example in the README,
        so, we test this here, for tracing the parsing."""
        template_path = "tests/data/testcase_tracing_parsing_and_exception.tpl.py"
        pp = pymacros4py.PreProcessor()
        with contextlib.redirect_stdout(io.StringIO()) as f:
            self.assertRaisesRegex(
                RuntimeError,
                r".*Syntax error in macro section, macro started but not ended.*",
                pp.expand_file,
                template_path,
                trace_parsing=True,
            )
        s = f.getvalue()
        self.assertRegex(
            s, r"(?s)" r".*line 1.*text.*x = " r".*line 1.*error.*insert\(v\).*"
        )

    def test_trace_evaluation_with_exception(self) -> None:
        """The README describes exception handling and tracing. The
        indirect expectation is, that an exception does not prevent the
        tracing from working. There is no explicit example in the README,
        so, we test this here, for tracing the evaluation."""
        template_path = "tests/data/testcase_tracing_evaluation_and_exception.tpl.py"
        pp = pymacros4py.PreProcessor()
        with contextlib.redirect_stdout(io.StringIO()) as f:
            # The expected behaviour depends on the availability of method
            # *add_note* for exceptions.
            if hasattr(RuntimeError(), "add_note"):
                self.assertRaisesRegex(
                    NameError,
                    r"name 'unknown_variable' is not defined",
                    pp.expand_file,
                    template_path,
                    trace_evaluation=True,
                )
            else:
                self.assertRaisesRegex(
                    RuntimeError,
                    r"Error occurred when expanding the following template:*",
                    pp.expand_file,
                    template_path,
                    trace_evaluation=True,
                )
        s = f.getvalue()
        self.assertRegex(
            s,
            r"(?s)"
            r".*line 1.*line_block_macro.*insert"
            r".*line 2.*line_block_macro.*insert.*",
        )

    def test_run_process_with_file_with_exception(self) -> None:
        """The README describes the behaviour when a
        *subprocess.CalledProcessError* occurs, but gives no doctest."""
        with contextlib.redirect_stdout(io.StringIO()) as f:
            self.assertRaisesRegex(
                subprocess.CalledProcessError,
                r"returned non-zero exit status 1",
                pymacros4py.run_process_with_file,
                ["python", "-m", "non_existing_module"],
                "some_file_path",
            )
        s = f.getvalue()
        self.assertRegex(
            s,
            r"(?s)"
            r".*The called process raised an exception"
            r".*some_file_path"
            r".*No module named non_existing_module.*",
        )

    def test_import_from_with_error(self) -> None:
        """The README describes importing from files. The
        indirect expectation is, that an exception also informs about the
        template that is expanded while the exception is raised.
        here is no explicit example in the README,
        so, we test this here."""
        template_path = "tests/data/testcase_import_from_with_error.tpl.py"
        pp = pymacros4py.PreProcessor()
        with contextlib.redirect_stdout(io.StringIO()) as f:
            self.assertRaisesRegex(
                RuntimeError,
                r".*Exception when importing.*error_unexpected_end.tpl.py.*",
                pp.expand_file,
                template_path,
                trace_parsing=True,
            )
        s = f.getvalue()
        self.assertRegex(
            s, r"(?s).*testcase_import_from_with_error.tpl.py.*import_from.*"
        )


if __name__ == "__main__":
    # This code allows to start the input/output test cases manually, without
    # all other tests triggered by the test procedure for the whole package.
    # Note: If this module is run on itself, the current directory needs to
    # be the base directory of the package.
    ReadmeExamplesTest().test_expansion_result()
