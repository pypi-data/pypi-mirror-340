if __name__ == "__main__":
    import doctest
    import unittest
    import coverage  # type: ignore

    # -- Start recording coverage
    cov = coverage.Coverage(source_pkgs=["pymacros4py"])
    cov.start()

    # -- Create empty TestSuite
    test_suite = unittest.TestSuite()
    verbosity = 1  # 1 normal, 2 for more details
    failfast = True  # True

    # -- Test modules: doc tests (currently: none)
    # for file in pathlib.Path("tests").glob("*.py"):
    #     file_name = file.name.removesuffix(".py")
    #     __import__(file_name)
    #     test_suite.addTests(doctest.DocTestSuite(file_name))

    # -- Test modules: unit tests classes
    new_suite = unittest.defaultTestLoader.discover("tests", pattern="test_unit*.py")
    test_suite.addTests(new_suite)

    # -- Package module source: doc tests (currently: none)
    # for file in pathlib.Path("src", "pymacros4py").glob("*.py"):
    #     file_name = file.name.removesuffix(".py")
    #     if file_name == "__init__":
    #         continue
    #     module = "." + file_name
    #     temp_module = importlib.import_module(module, "pymacros4py")
    #     test_suite.addTests(doctest.DocTestSuite(temp_module))

    # -- Separate documentation: doc tests (currently: none)
    # for file_path in pathlib.Path(".", "docs", "source").glob("*.rst"):
    #   test_suite.addTests(doctest.DocFileSuite(str(file_path), module_relative=False))

    # -- DocTests for README.rst
    test_runner = unittest.TextTestRunner(verbosity=verbosity, failfast=failfast)
    if test_runner.run(test_suite).wasSuccessful():
        # Create new empty TestSuite for doctests
        # (we do them separately to be sure, the README.rst is already created by the
        # unittests)
        test_suite = unittest.TestSuite()
        test_suite.addTests(doctest.DocFileSuite("README.rst", module_relative=False))
        unittest.TextTestRunner(verbosity=verbosity, failfast=failfast).run(test_suite)

    # -- Stop recording coverage, create HTML from results
    cov.stop()
    cov.save()
    cov.xml_report()
    cov.html_report()
