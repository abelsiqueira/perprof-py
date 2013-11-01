# This is the main file for perprof

class PerProfSetup():
    """This is a class to store the files to be used."""
    pass

def main():
    """This is the entry point when calling perprof."""
    import argparse

    parser = argparse.ArgumentParser(
            description='A python module for performance profiling (as described by Dolan and Moré)')

    args = parser.parse_args()
