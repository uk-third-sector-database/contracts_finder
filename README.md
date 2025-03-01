## Contracts Finder Scraper

![coverage](https://img.shields.io/badge/Purpose-Research-yellow)
[![Generic badge](https://img.shields.io/badge/Python-3.x-red.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/License-GNU3.0-purple.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/Maintained-Yes-brightgreen.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/BuildPassing-Yes-orange.svg)](https://shields.io/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14951540.svg)](https://doi.org/10.5281/zenodo.14951540)

A scraper to scrape data on awarded contracts from [Contracts Finder](https://www.gov.uk/contracts-finder).
It uses Version 2 of the contracts finder API, iterating through dateranges in a gradually decremental way. The only dependency is `requests`, with output deposited in `./data/`.

### License
This work is free. You can redistribute it and/or modify it under the terms of the GNU GPL 3.0 license.

### Acknowledgements
We are grateful for funding from the ESRC (project reference: ES/X000524/1).
