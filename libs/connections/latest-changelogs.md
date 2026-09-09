## [v0.2.1](https://pypi.org/project/amsdal-glue-connections/0.2.1/) - 2026-09-09

### Added

- Added Python 3.13 and 3.14 to the supported/tested versions. Bumped the pyo3 dependency from 0.23 to 0.24 so the Rust extension builds a native `abi3` wheel for Python 3.14 without needing `PYO3_USE_ABI3_FORWARD_COMPATIBILITY`.
