# -*- coding: utf-8 -*-

"""Console script for plotdarn."""
import argparse
import sys
from .plotdarn import plot_superdarn, read_file
import geoviews as gv


def main():
    """Console script for plotdarn."""
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='SuperDarn file to plot')
    args = parser.parse_args()

    data = read_file(args.file)

    gv.extension('bokeh')

    plot_superdarn(data)

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
