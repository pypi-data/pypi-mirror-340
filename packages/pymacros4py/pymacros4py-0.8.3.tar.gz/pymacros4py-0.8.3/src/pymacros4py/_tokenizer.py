import re
from collections.abc import Iterator, Iterable
from typing import NamedTuple


class Token(NamedTuple):
    """A macro or text section found in the template by the tokenizer"""

    type: str
    """ The token type (error, text, embedded_macro, line_block_macro) """
    content: str
    """ The macro code of the macro section, resp. the text of the text section"""
    section_start_pos: int
    """ Position of first character (might be whitespace) of the macro section """
    start_marker_pos: int
    """ Position of first character of the introducing macro marker """
    content_pos: int
    """ Position of the first character of the token content in the template """


TokenStream = Iterator[Token]


class Tokenizer:
    """Text tokenizer for macro expansion. It extracts macro sections and
    remaining text sections and recognizes if a macro section is started but not ended.
    It can be configured by replacing the default regular expression patterns by
    application specific ones.

    :param macro_marker: If a string literal of the allowed forms or a comment starts
        with a string matching the *macro_marker*, it is treated as macro call.
    :param string_literal_start: Pattern for the start of a macro string literal
    :param string_literal_start_group: Name of the regular expression pattern group
        that encapsulates the concrete string used in the input to start the
        macro string literal. See *string_literal_end*.
    :param string_literal_end: End of a macro string literal.
        If *string_literal_start* allows several options to start a string literal,
        *string_literal_end* can refer to *string_literal_start_group*
        to express, that the literal needs to end like it started.
    :param line_comment_start: Pattern for the start of a macro string in a comment.
    """

    def __init__(
        self,
        macro_marker: str = r"\$\$",
        string_literal_start: str = r"(''')|'" + r'|(""")|"',
        string_literal_start_group: str = "pm4p_quotes",
        string_literal_end: str = r"(?P=pm4p_quotes)",
        line_comment_start: str = r"#(( |\t)*)",
    ) -> None:
        # Prefixes used for distinguishing the named match groups of the tokenizer
        # from others that might be used in the patterns chosen by the application
        self._token_group_prefix = token_group_prefix = "pm4p_grp_"
        self._token_pos_group_prefix = token_pos_group_prefix = "pm4p_pos_grp_"
        token_other_group_prefix = "pm4p_other_grp_"

        # Helper functions and literals for regular expressions
        def re_in_brackets(pattern: str) -> str:
            return r"(" + pattern + r")"

        def re_named_group(name: str, content_pattern: str) -> str:
            return re_in_brackets(r"?P<" + name + r">" + content_pattern)

        def re_or_bracketed_elements(patterns: Iterable[str]) -> str:
            """Regular expression or'ing some patterns. The patterns are put into
            brackets to avoid associativity problems, the result is not."""
            return re_in_brackets(r")|(".join(patterns))

        def re_not_ahead(pattern: str) -> str:
            return re_in_brackets(r"?!" + pattern)

        def re_if(id_or_name: str, yes_pattern: str, no_pattern: str) -> str:
            return re_in_brackets(
                r"?" + re_in_brackets(id_or_name) + yes_pattern + r"|" + no_pattern
            )

        optional_whitespace = r"(\s*)"
        spaces_or_tabs = r"([ \t]*)"
        character_or_newline = re_in_brackets(r".|\n")
        anything = character_or_newline + r"+"
        anything_non_greedy = character_or_newline + r"+?"
        eol = r"$"
        sol = r"^"
        end_of_line_optionally_nl = re_in_brackets(r"$\n?")

        # Regular expression for a macro call
        # (Starts with quotes or like a comment, continues with a macro marker,
        # continues with macro text, and ends with matching closing quotes,
        # if it has started with brackets, or the end of the line.)
        def re_macro_instance(
            group_suffix: str,
        ) -> str:
            # Adapt the named group names in order to make them usable multiple times
            # within the same regular expression
            local_start_marker_group = token_pos_group_prefix + group_suffix
            local_string_literal_start_group = string_literal_start_group + group_suffix
            local_string_literal_end = string_literal_end.replace(
                string_literal_start_group, local_string_literal_start_group
            )

            # starting quotes or hash. Quotes have their own group to describe
            # matching closing quotes later on. All together has a group to know
            # the starting position of non-whitespace part of the macro section.
            local_start_marker = (
                re_named_group(
                    local_start_marker_group,
                    re_or_bracketed_elements(
                        [
                            re_named_group(
                                local_string_literal_start_group, string_literal_start
                            ),
                            line_comment_start,
                        ]
                    ),
                )
                + macro_marker
                + optional_whitespace
            )
            local_end_marker = re_if(
                local_string_literal_start_group,
                optional_whitespace + macro_marker + local_string_literal_end,
                eol,
            )
            return (
                local_start_marker
                + re_named_group(token_group_prefix + group_suffix, anything_non_greedy)
                + local_end_marker
            )

        def re_macro_line_block_instance(
            group_suffix: str,
        ) -> str:
            # 'line_block_macro'
            return re_in_brackets(
                sol
                + spaces_or_tabs
                + re_macro_instance(group_suffix)
                + spaces_or_tabs
                + end_of_line_optionally_nl
            )

        # Regular expression for a text block
        # ("as long as it does not look like a line block macro or the start
        # of a non-line-block macro section". The first is necessary, because
        # a match of a line block macro can also fail by the text after
        # the macro section. And the second case need to be limited to the start
        # of the section in order to find syntax errors of missing section endings.)
        re_text = re_named_group(
            token_group_prefix + "text",
            re_in_brackets(
                re_not_ahead(
                    re_or_bracketed_elements(
                        [
                            re_macro_line_block_instance(
                                token_other_group_prefix + "ahead_line_block"
                            ),
                            re_in_brackets(string_literal_start) + macro_marker,
                            re_in_brackets(line_comment_start) + macro_marker,
                        ]
                    )
                )
                + character_or_newline
            )
            + r"+",
        )

        # Regular expression that matches anything else and reports an error
        re_error = re_named_group(token_group_prefix + "error", anything)

        # A token is a macro call, or (otherwise) a block that does not look
        # like the start of a macro call, or (otherwise) a syntax error
        # (text, that starts like a macro call, but does not fully match the
        # syntax of a macro call)
        re_tokens = re_or_bracketed_elements(
            [
                re_macro_line_block_instance("line_block_macro"),
                re_macro_instance("embedded_macro"),
                re_text,
                re_error,
            ]
        )
        # import sys
        # print(re_tokenizer, file=stderr)
        # raise RuntimeError("tmp")
        self._tokenizer_pattern = re.compile(re_tokens, re.MULTILINE)

    def tokenize(self, text: str) -> TokenStream:
        """Iterate and unpack oll tokens in *text*."""

        # A token is a match of a named group with a name started by
        # *token_group_prefix*.
        tokenizer_pattern = self._tokenizer_pattern
        token_group_prefix = self._token_group_prefix
        for match in re.finditer(tokenizer_pattern, text):
            # Get match data
            group_dict, pos = match.groupdict(), match.start()
            if not group_dict:  # pragma: no cover
                raise RuntimeError(f"Internal error: No match result at pos {pos}")

            # Groups that match and are relevant, because they stem from the tokenizer
            found_tokens = {
                name: token_content
                for (name, token_content) in group_dict.items()
                if token_content is not None
                and name.removeprefix(token_group_prefix) != name
            }
            if not found_tokens:  # pragma: no cover
                raise RuntimeError(f"Internal error: No match at pos {pos}")
            # Get group with the syntax case we are in, and the code content
            if len(found_tokens) > 1:  # pragma: no cover
                raise RuntimeError(
                    f"Internal error: Several matches at pos {pos}" f": {found_tokens}"
                )
            token_group_name, token_content = found_tokens.popitem()
            token_type = token_group_name.removeprefix(token_group_prefix)
            token_content_pos = match.start(token_group_name)

            # start position of section
            section_start_pos = match.start()

            # In case of macro: position of start marker
            start_marker_pos = (
                match.start(self._token_pos_group_prefix + token_type)
                if token_type in ["macro", "line_block_macro"]
                else section_start_pos
            )

            yield Token(
                token_type,
                token_content,
                section_start_pos,
                start_marker_pos,
                token_content_pos,
            )
