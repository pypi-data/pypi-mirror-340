import itertools
import re

from ._tokenizer import Tokenizer


class TemplateScriptIndentation:
    """
    Current indention state of a stream of created code. Used during the creation of a
    template script."""

    def __init__(self, steps: int) -> None:
        self._indentation_level = 0
        self._indentation_steps = steps

    def indent(self) -> None:
        self._indentation_level += 1

    def dedent(self, content_line: str, content: str) -> None:
        self._indentation_level -= 1
        if self._indentation_level < 0:
            raise RuntimeError(
                f"--- {content_line}: "
                "Nesting error in compound statements "
                "with suites spanning several sections, "
                f"in macro section:\n{content}"
            )

    def __str__(self) -> str:
        return " " * self._indentation_level * self._indentation_steps

    def __bool__(self) -> bool:
        return self._indentation_level != 0


def _extract_prefix(template: str, pos: int) -> str:
    """Find the start of the line in *template* where *pos* is.
    Return the characters from the start of the line till the one
    before *pos*.

    :param template: A template. Needs to follow Unix-style end of line convention.
    :param pos: A position (number of characters) in the template
    """
    # Find position of previous newline character and skip it.
    # If we do not find one, we are at the first line of the text, get
    # position -1, and the '+1' brings us to the first character of the file.
    nl_pos = template.rfind("\n", 0, pos) + 1
    # characters from line start (inclusively) to pos (exclusively)
    return template[nl_pos:pos]


def _line_no(template: str, pos: int) -> int:
    """Return the line in *template* where *pos* is, counted from 1"""
    return template[:pos].count("\n") + 1


# def _col_no(template: str, pos: int) -> int:
#     """ Return the column in *template* where *pos* is, counted from 1 """
#     return pos - template[:pos].rfind("\n") + 1


def _separate_indentation_and_content(text: str) -> tuple[str, str]:
    """Get the whitespace characters, that the *text* starts with, and the rest of it

    :param text: A string without newline characters
    """
    # strip any whitespace starting from the left
    text_stripped = text.lstrip()
    # Extract exactly the stripped whitespaces
    whitespace_len = len(text) - len(text_stripped)
    return text[0:whitespace_len], text_stripped


class TemplateScript:
    """
    Template script for *template*, created using *tokenizer*.
    Its string representation (as returned by *str(template_script)*) is the
    generated script code.

    :param file_name: Name of the file of the template. Used for log messages.
    :param template: The template to expand. Needs to follow Unix-style
       end of line convention.
    :param tokenizer: Tokenizer to use.
    :param trace_parsing: Print parsing log.
    :param trace_evaluation: Print evaluation log.
    """

    # Given the current functionality and use cases, the class could be replaced by a
    # function that directly returns the generated script code. The form of a class has
    # been chosen to make it possible to add further attributes in the future.

    def __init__(
        self,
        file_name: str,
        template: str,
        tokenizer: Tokenizer,
        trace_parsing: bool = False,
        trace_evaluation: bool = False,
    ) -> None:
        self.file_name = file_name

        # Token texts that have already been regarded in the generation of the
        # token expansion code. Used to give the template script access to them.
        token_strings = list[str]()

        # Initialize handling of indentation in template script
        script_indentation = TemplateScriptIndentation(4)

        # List of the strings produced by the expansion of the found tokens
        template_script_strings = []

        # Parse tokens and generate template expansion code, string by string
        for token_no, token in zip(itertools.count(), tokenizer.tokenize(template)):
            (
                token_type,
                content,
                section_start_pos,
                start_marker_pos,
                content_pos,
            ) = token

            content_line = f'File "{file_name}", line {_line_no(template, content_pos)}'

            if trace_parsing:
                print(f"--- {content_line}: {token_type}:\n>{content}<\n\n", flush=True)

            token_strings.append(content)

            if trace_evaluation:
                template_script_strings.append(
                    f"{str(script_indentation)}"
                    f"print('''{repr(content_line)}: {token_type}\n"
                    f">{token_strings[token_no]}<\n\n''', flush=True)\n"
                )

            if token_type == "error":
                raise RuntimeError(
                    f"--- {content_line}: "
                    "Syntax error in macro section, macro started but not ended:\n"
                    f"{content}"
                )

            elif token_type == "text":
                s = f"{str(script_indentation)}insert({repr(content)})\n"
                template_script_strings.append(s)

            elif token_type in ["embedded_macro", "line_block_macro"]:
                # Section indentation
                start_marker_prefix = _extract_prefix(template, start_marker_pos)
                start_marker_indentation = re.sub(r"\S", " ", start_marker_prefix)

                # Base indentation
                code_start_prefix = _extract_prefix(template, content_pos)
                base_indentation = re.sub(r"\S", " ", code_start_prefix)

                # If the last character of macro code is a colon,
                # the macro code is a compound statement with a multi-section suite.
                # (We can check this like this, because whitespace has already been
                # stripped on the right by the tokenizer)
                multi_section_suite_starts = content and content[-1] == ":"

                # Case that content is":end":
                # (We can check this like this, because other
                # content is not allowed in macro code together with ":end")
                multi_section_suite_ends = content.strip()[0:4] == ":end"

                if not multi_section_suite_starts and not multi_section_suite_ends:
                    # Inform the global_evaluation_context of the template script that a
                    # new macro starts here, what indention its output need to have, and
                    # whether it is an embedded macro.
                    template_script_strings.append(
                        str(script_indentation)
                        + "_macro_starts("
                        + "indentation="
                        + repr(start_marker_indentation)
                        + ", "
                        + "embedded="
                        + str(token_type == "embedded_macro")
                        + ", "
                        + "content_line="
                        + repr(content_line)
                        + ")\n"
                    )

                if multi_section_suite_ends:
                    # Handle suite (of a compound statement) ending in this macro
                    script_indentation.dedent(content_line, content)
                    # Note: A macro that ends a suite (of a compound statement)
                    # has no _macro_end (and no _macro_start).
                    continue

                # # Detect and expand shorthand notation "? something" for
                # # "insert(something)"
                # # (This functionality is currently not offered)
                # if content[0] == "?":
                #     content = "insert(" + content[1:].lstrip() + ")"

                # Case of a statement ending a suite and re-starting a new one
                if re.match(r"(elif|else|except|finally|case).*:", content):
                    script_indentation.dedent(content_line, content)

                # iterator of numbered lines
                lines = content.splitlines()
                numbers_and_lines = enumerate(lines)

                # Special-case first line of macro code: It already comes without
                # indentation
                number, line = next(numbers_and_lines)
                template_script_strings.append(str(script_indentation) + line + "\n")

                # All lines subsequent lines of output: De-indent line relative to
                # the base indentation, indent it for the results and insert it to
                # the results
                for no, line in numbers_and_lines:
                    line_indentation, _ = _separate_indentation_and_content(line)
                    if len(line_indentation) == 0 and len(base_indentation) > 0:
                        # Zero indentation in a context with none-zero base indentation:
                        # Just take the line as it is
                        template_script_strings.append(line + "\n")
                    elif (
                        line_indentation[0 : len(base_indentation)] == base_indentation
                    ):
                        # Line indentation string is extension of base indentation
                        # string: Compute relative indentation, and prepend
                        # script indentation
                        template_script_strings.append(
                            str(script_indentation)
                            + line[len(base_indentation) :]
                            + "\n"
                        )
                    else:
                        # If the macro code is indented, indentation (as a string)
                        # need to start with exactly the base indentation
                        raise RuntimeError(
                            f"{content_line}: "
                            f"Syntax error: indentation of line {no} of the "
                            f"macro code is not an extension of the base indentation."
                        )

                if multi_section_suite_starts:
                    # Handle compound statement with a suite beginning in this macro
                    # section and spanning subsequent sections
                    script_indentation.indent()

                if not multi_section_suite_starts:
                    # Inform the global_evaluation_context of the template script that
                    # the macro ends here
                    template_script_strings.append(
                        str(script_indentation) + f"_macro_ends({repr(content_line)})\n"
                    )

            else:  # pragma: no cover
                raise RuntimeError(
                    f"{content_line}:"
                    f"Internal error: Tokenizer returned unknown token "
                    f"type {token_type} at position {content_pos}"
                )

        # Check sanity of reached state
        if script_indentation:
            raise RuntimeError(
                "Syntax error: block nesting (indentation) not correct, "
                "is :end somewhere missing?"
            )

        # Concatenate the template strings to the template script
        self._template_script = "".join(template_script_strings)

    def __str__(self) -> str:
        """Return the code of the template script."""
        return self._template_script
