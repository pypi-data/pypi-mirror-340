from typing import Optional
import tempfile
import os
import sys
import pathlib
from dataclasses import dataclass

from ._files import read_file
from ._tokenizer import Tokenizer
from ._global_evaluation_context import GlobalEvaluationContext
from ._template_script import TemplateScript


@dataclass
class Macro:
    outer_macro: Optional["Macro"]
    indentation: str
    is_embedded: bool
    content_line: str
    output: list[str]


def _separate_indentation_and_content_optionally_nl(s: str) -> tuple[str, str]:
    """Get the whitespace characters, that the *text* starts with, and the rest of it

    :param s: A string without newline characters except, maybe, the last character
    """

    # Separate the line and a possible trailing single newline
    if s and s[-1] == "\n":
        s, newline = s[:-1], s[-1]
    else:
        s, newline = s, ""

    # Strip any whitespace (s has no NL anymore) starting from the left
    s_stripped = s.lstrip()
    # Extract exactly the stripped whitespaces
    whitespace_len = len(s) - len(s_stripped)

    # Return the leading whitespace if s, and the following content (optionally with
    # the newline, we put aside at the beginning
    return s[0:whitespace_len], s_stripped + newline


def evaluate_template_script(
    template_script: TemplateScript,
    tokenizer: Tokenizer,
    global_evaluation_context: GlobalEvaluationContext,
    already_imported_files: set[str],
    globals_dict: Optional[dict] = None,
) -> str:
    """
    Run the *template_script* and return the results. For recursive
    template expansion, use *tokenizer* in the *global_evaluation_context*
    with the *globals_dict*.

    :param template_script: The script to evaluate.
    :param tokenizer: The tokenizer for recursive template expansions.
    :param global_evaluation_context: Global context information for all template
        expansions happening under a single PreProcessor.
    :param already_imported_files: Template files that have already been "imported"
        along the current (possibly recursive) expansion based on the globals_dict.
        Used by method *import_from* to avoid repeated imports of content
        from the same file.
    :param globals_dict: Like parameter *globals* of the Python function
        *exec*. Note, that in order to use it, a value for key *pp* will be
        set.
    """

    # The following two variables are also used within the functions, that are provided
    # to the expansion script as part of the content of its global namespace:
    # List of all generated fragments of output
    output: list[str] = []
    # Subsequent output does not stem from a macro
    macro: Optional[Macro] = None

    # The following functions are the respective functions that the template expansion
    # code can use.
    # They are defined as closures, in order to be able to access the current
    # evaluation context, the variables defined above, without needing an access path
    # seen in the template script.

    def _macro_starts(indentation: str, embedded: bool, content_line: str) -> None:
        """The *macro_starts_ function for macro code.

        Store the information, that subsequent *insert* calls stem from
        the current macro, the standard indentation for expansion results
        inserted by these calls, and whether the current macro is an embedded
        macro.

        The first line inserted by an embedded macro remains without indentation.
        """
        nonlocal macro
        macro = Macro(macro, indentation, embedded, content_line, list[str]())

    def _macro_ends(content_line: str) -> None:
        """The *macro_ends* function for macro code.

        Store the information, that subsequent *insert* calls do not stem
        from the current macro anymore.
        """
        nonlocal macro

        if macro is None:  # pragma: no cover
            raise RuntimeError(
                f"{content_line}:\n"
                f"Internal error: macro_end without macro_start in the "
                f"template expansion script for the above given template line"
            )

        current_macro = macro
        macro = current_macro.outer_macro
        current_output = macro.output if macro else output

        # Handle macro output (expansion result) line by line
        lines = "".join(current_macro.output).splitlines(keepends=True)

        if not lines:
            # Not a single line to process: finished
            return

        # First line
        line = lines.pop(0)
        (
            base_indentation,
            line_content,
        ) = _separate_indentation_and_content_optionally_nl(line)
        if current_macro.is_embedded:
            # Use unindented result content
            current_output.append(line_content)
        else:
            # Indent as defined for the macro
            current_output.append(current_macro.indentation + line_content)

        # Each subsequent line:
        for line in lines:
            (
                line_indentation,
                line_content,
            ) = _separate_indentation_and_content_optionally_nl(line)
            if len(line_indentation) == 0 and len(base_indentation) > 0:
                # Zero indentation in a context with none-zero base indentation:
                # Just take the line as it is
                current_output.append(line)
            elif line_indentation[0 : len(base_indentation)] == base_indentation:
                # Line indentation string is extension of base indentation
                # string: Compute relative indentation (including the content), and
                # prepend macro indentation to it
                current_output.append(
                    current_macro.indentation + line[len(base_indentation) :]
                )
            else:
                # If the line is indented, indentation (as a string)
                # need to start with exactly the base indentation
                raise RuntimeError(
                    f"{current_macro.content_line}:\n"
                    f"Output syntax error: indentation of the following line of the "
                    f"results of the template script from the above given template "
                    f"line is not an extension of the base indentation of these "
                    f"results:\n"
                    f">{line.rstrip()}<\n"
                    f"(Start of line shown enclosed by characters '>' and '<')"
                )

    def insert(*vargs: object) -> None:
        """The *insert function* for macro code.

        Concatenate string representations (result from *str()*)
        of the arguments. Indent the lines with the current indentation,
        except for the first line produced by an embedded macro.
        Insert result to the result of the template expansion.
        """
        lines_str = "".join((str(a) for a in vargs))

        if lines_str == "":
            # Nothing to insert into expansion output
            return

        current_output = macro.output if macro else output
        # If we have been called from within macro code (this includes the case that
        # the macro code calls a function that contains a text block that calls
        # us): store content for bulk processing at the end of the macro
        # If we have been called from a text block (and it is not part
        # of a function definition within a macro): Output it as-is
        # Both is implemented the same way.
        current_output.append(lines_str)

    def insert_content(file: str) -> None:
        """
        Insert the content of the file to the expansion results of the current
        template expansion. Do not perform a template expansion.

        :param file: File to process.
        """
        insert(read_file(file))

    def insert_from(
        template_file: str,
        globals_dict: Optional[dict] = None,
        trace_parsing: bool = False,
        trace_evaluation: bool = False,
    ) -> None:
        """
        Perform a macro expansion on the content of a file in the scope
        of a new Python interpreter.
        Use *globals* to initialize the interpreter like in a call of *eval()*.

        Insert the output to the expansion results of the current template
        expansion.

        When called a second time with an identical argument for *template_file*,
        and *globals* is *None* in both calls, re-use the output of the previous run.

        (If *globals* is not *None*, and you like to re-use results in cases of
        equivalent content of *globals*, this has to be implemented manually.)

        :param template_file: Template to expand. If the first part of the path
          (see *pathlib.PurePath.parts*) is '$$', this part is removed and the
          subsequent parts are interpreted relative to the directory of the
          currently expanded template.
        :param globals_dict: Like parameter *globals* of the Python function *exec*.
          Note, that in order to use it, a value for key *macro* will be set.
        :param trace_parsing: Print parsing log to stderr.
        :param trace_evaluation: Print evaluation log to stderr.
        """
        parts = pathlib.PurePath(template_file).parts
        if parts and parts[0] == "$$":
            template_dir = pathlib.PurePath(template_script.file_name).parent
            template_file = str(pathlib.PurePath(template_dir, *parts[1:]))
        template = read_file(template_file)
        template_script_to_insert_from = TemplateScript(
            template_file, template, tokenizer, trace_parsing, trace_evaluation
        )

        if globals_dict:
            # Here, we cannot cache, because we cannot recognize identical
            # content of the globals_dict
            result = evaluate_template_script(
                template_script_to_insert_from,
                tokenizer,
                global_evaluation_context,
                already_imported_files,
                globals_dict,
            )
        else:
            already_inserted = global_evaluation_context.already_inserted_content
            template_file_resolved = str(
                pathlib.Path(template_file).resolve(strict=True)
            )
            if template_file_resolved in already_inserted:
                result = already_inserted[template_file_resolved]
            else:
                result = evaluate_template_script(
                    template_script_to_insert_from,
                    tokenizer,
                    global_evaluation_context,
                    set[str](),  # no imports so far, due to new evaluation context
                    None,  # empty globals dict -> new evaluation context
                )
                already_inserted[template_file_resolved] = result
        insert(result)

    def import_from(
        template_file: str,
        trace_parsing: bool = False,
        trace_evaluation: bool = False,
    ) -> None:
        """
        Perform a macro expansion of *file* in the scope of the current interpreter.
        Attributes that have already been set can be used by macro code in
        *template_file*,
        and attributes set by such code can be used in macro code following
        the call.

        Discard the output of the expansion run.

        When called a second time with an identical argument for *template_file*,
        ignore the call.

        :param template_file: Template to expand. If the first part of the path
          (see *pathlib.PurePath.parts*) is '$$', this part is removed and the
          subsequent parts are interpreted relative to the directory of the
          currently expanded template.
        :param trace_parsing: Print parsing log to stderr.
        :param trace_evaluation: Print evaluation log to stderr.
        """

        parts = pathlib.PurePath(template_file).parts
        if parts and parts[0] == "$$":
            template_dir = pathlib.PurePath(template_script.file_name).parent
            template_file = str(pathlib.PurePath(template_dir, *parts[1:]))
        template_file_resolved = str(pathlib.Path(template_file).resolve(strict=True))
        if template_file_resolved in already_imported_files:
            return
        try:
            template = read_file(template_file)
            template_script_to_import_from = TemplateScript(
                template_file, template, tokenizer, trace_parsing, trace_evaluation
            )
            _ = evaluate_template_script(
                template_script=template_script_to_import_from,
                tokenizer=tokenizer,
                global_evaluation_context=global_evaluation_context,
                already_imported_files=already_imported_files,
                globals_dict=globals_dict,
            )
            already_imported_files.add(template_file_resolved)
        except Exception as e:
            raise RuntimeError(
                f'Exception when importing from file "{template_file}"'
            ) from e

    # Globals dict for the execution of the template script:
    # Make the current object accessible from within the template script code, and
    # also the functions that are meant to be called from within this code.
    # globals_dict["pp"] = global_evaluation_context
    globals_to_set = {
        "insert": insert,
        "insert_content": insert_content,
        "insert_from": insert_from,
        "import_from": import_from,
        "_macro_starts": _macro_starts,
        "_macro_ends": _macro_ends,
        "stderr": sys.stderr,
    }

    # Make these assignments, and prepare for undoing them later, is necessary
    if globals_dict is None:
        globals_dict = globals_to_set
        globals_backup = dict()
    else:
        globals_backup = {
            key: globals_dict[key]
            for key in globals_to_set.keys()
            if key in globals_dict
        }
        globals_dict.update(globals_to_set)

    # We create an empty file, that will not (!) be removed when
    # an exception happens. We use its path as virtual name
    # when executing a script that is stored in a string.
    # When the exec raises an exception, we store the template
    # that we have already executed to the file, so that the user
    # can "debug" the file that the exception mentions.
    # We need individual files since macro expansion can be nested,
    # so that we get different temporary files for each nesting level.
    tmp_file, tmp_file_path = tempfile.mkstemp(
        suffix=".py",
        prefix=f"template_script_{next(global_evaluation_context.tmp_file_numbers)}",
        dir=None,
        text=True,
    )

    # Execute the template script and return what it reports using *insert*
    template_script_code = str(template_script)
    try:
        ast_object = compile(
            template_script_code,
            tmp_file_path,
            mode="exec",
            # flags=0, dont_inherit=False, optimize=- 1
        )
        exec(ast_object, globals_dict)

        # Exec raised no exception, so we do not need the temporary file.
        os.close(tmp_file)
        os.remove(tmp_file_path)

        return "".join(output)

    except Exception as exc:
        # save the template to the file and close it
        try:
            template_as_bytes = template_script_code.encode(
                encoding="utf-8", errors="strict"
            )
            os.write(tmp_file, template_as_bytes)
        finally:
            os.close(tmp_file)
        note = (
            "Error occurred when executing template script.\n"
            f' File "{tmp_file_path}"'
        )
        # Depending on the used Python version, one of the following will happen.
        if hasattr(exc, "add_note"):  # pragma: no cover
            exc.add_note(note)
            raise
        raise RuntimeError(note) from exc  # pragma: no cover
    finally:
        # If a globals_dict has been given to us, undo changes we have done there
        globals_dict.update(globals_backup)
