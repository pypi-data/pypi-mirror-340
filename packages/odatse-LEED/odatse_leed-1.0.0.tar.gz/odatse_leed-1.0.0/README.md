# odatse-LEED: solver module for analyses of LEED data

[Open Data Analysis Tool for Science and Engineering (ODAT-SE)](https://github.com/issp-center-dev/ODAT-SE) is a framework for applying a search algorithm to a direct problem solver to find the optimal solution. It has been developed by the name 2DMAT, and since version 3.0, it is organized as an open platform for data analysis by modularizing direct problem solvers and search algorithms.

SATLEED is a software package developed by M.A. Van Hove for the analyses of LEED, which calculates the I-V curve from the atomic positions and other parameters, and evaluate the deviations from the Rocking curve obtained from the experiments. odatse-LEED is an adaptor library to use SATLEED as a direct problem solver of ODAT-SE.


## Prerequists

- Required
  - python >= 3.9
  - numpy >= 1.14
  - pydantic >= 2.0
  - fortranformat >= 2.0
  - ODAT-SE >= 3.0
  - SATLEED

## Install

- From PyPI (Recommended)
  - `python3 -m pip install -U odatse-LEED`
    - If you install them locally, use `--user` option like `python3 -m pip install -U --user`
- From Source (For developers)
  1. update `pip >= 19` by `python3 -m pip install -U pip`
  2. `python3 -m pip install ODATSE_LEED_ROOT_DIRECTORY` to install `odatse-LEED` package and `odatse-LEED` command
    - `ODATSE_LEED_ROOT_DIRECTORY` points to the directory including this `README.md` file.

## Simple Usage

- `odatse-LEED input.toml` (use the installed script)
- `python3 src/main.py input.toml` (use the raw script)
- For details of the input file, see the document.

## Files and directories of odatse-LEED

- `src/`
  - source codes
- `sample/`
  - sample usages
- `doc/`
  - source codes of documents (manuals)
- `tests/`
  - for automatic test
- `LICENSE`
  - license terms (GNU GPL v3)
- `README.md`
  - this file
- `pyproject.toml`
  - metadata for `odatse-LEED`

## License

This package is distributed under GNU General Public License version 3 (GPL v3) or later.

We hope that you cite the following references when you publish the results using 2DMAT / ODAT-SE:
"Data-analysis software framework 2DMAT and its application to experimental measurements for two-dimensional material structures",
Y. Motoyama, K. Yoshimi, I. Mochizuki, H. Iwamoto, H. Ichinose, and T. Hoshi, Computer Physics Communications 280, 108465 (2022).

Bibtex:
```
@article{MOTOYAMA2022108465,
  title = {Data-analysis software framework 2DMAT and its application to experimental measurements for two-dimensional material structures},
  journal = {Computer Physics Communications},
  volume = {280},
  pages = {108465},
  year = {2022},
  issn = {0010-4655},
  doi = {https://doi.org/10.1016/j.cpc.2022.108465},
  url = {https://www.sciencedirect.com/science/article/pii/S0010465522001849},
  author = {Yuichi Motoyama and Kazuyoshi Yoshimi and Izumi Mochizuki and Harumichi Iwamoto and Hayato Ichinose and Takeo Hoshi}
}
```

## Copyright

© *2020- The University of Tokyo. All rights reserved.*
This software was developed with the support of "*Project for advancement of software usability in materials science*" of The Institute for Solid State Physics, The University of Tokyo.

[source/master]: https://github.com/2DMAT/odatse-LEED/
[source/develop]: https://github.com/2DMAT/odatse-LEED/tree/develop
[ci/master/badge]: https://github.com/2DMAT/odatse-LEED/workflows/Test/badge.svg?branch=master
[ci/master/uri]: https://github.com/2DMAT/odatse-LEED/actions?query=branch%3Amaster
[doc/en/badge]: https://img.shields.io/badge/doc-English-blue.svg
[doc/ja/badge]: https://img.shields.io/badge/doc-Japanese-blue.svg
[doc/master/en/uri]: https://2DMAT.github.io/odatse-LEED/manual/master/en/index.html
[doc/master/ja/uri]: https://2DMAT.github.io/odatse-LEED/manual/master/ja/index.html
[doc/develop/en/uri]: https://2DMAT.github.io/odatse-LEED/manual/develop/en/index.html
[doc/develop/ja/uri]: https://2DMAT.github.io/odatse-LEED/manual/develop/ja/index.html
