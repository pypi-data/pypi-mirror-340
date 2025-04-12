import itertools


class GlobalEvaluationContext:
    """
    Global context information for all template expansions happening under a single
    PreProcessor.
    """

    def __init__(self) -> None:
        self.already_inserted_content = dict[str, str]()
        # A cache of the expansion results of all template files that have already
        # been "inserted". Used by method *insert_from* of the evaluator to avoid
        # unnecessary repeated expansions.

        self.tmp_file_numbers = itertools.count()
        # Global counter for generated temporary files. During recursive evaluation,
        # all files 'on the stack' exist in parallel, so they are numbered.
        # Currently, an exception stops the evaluation and only the files on the
        # stack remains (for debugging), but for the future, it might be possible
        # to continue expansion with other files, and for this, be use a global
        # counter here, and not one just for files on the local evaluation stack.
