# Contributing

We welcome contributions to the AMSDAL Glue project! Whether you want to report a bug, request a feature, or submit a
pull request, we appreciate your help in making the project better.

## Project management

In all packages we have configured [Hatch](https://hatch.pypa.io/1.8/) to manage the project.
In order to contribute to the project, you will need to install Hatch.

```bash
pip install hatch
```

And then you can install the project in development mode:

```bash
hatch env create
```

And then run any scripts defined in the `pyproject.toml` file, for example to run the tests:

```bash
hatch run test
```

## Reporting Issues

If you encounter a bug or have a feature request, please open an issue on
the [GitHub repository](https://github.com/amsdal/amsdal-glue/issues)
and provide as much detail as possible. This will help us understand the problem and work towards a solution.

When reporting an issue, please include the following information:

- A clear and descriptive title.
- A detailed description of the issue or feature request.
- Steps to reproduce the issue, if applicable.
- Any relevant error messages or screenshots.
- The version of the AMSDAL Glue packages you are using.
- The version of Python you are using.
- Any other relevant information that may help us understand the problem.

## Contributing Code

If you would like to contribute code to the project, please follow these steps:

1. Fork the repository on GitHub.
2. Create a new branch for your changes.
3. Make your changes and commit them to your branch.
4. Run the tests to ensure that your changes do not break existing functionality.
5. Push your changes to your fork on GitHub.
6. Create a pull request to submit your changes for review.

When submitting a pull request, please include the following information:

- A clear and descriptive title.
- A detailed description of the changes you have made.
- Any relevant information that may help us understand the changes.
- If your changes are related to an existing issue, please reference the issue number in your pull request.
- If your changes add new functionality, please include tests to cover the new code.
- If your changes modify existing functionality, please ensure that the existing tests still pass.
- If your changes require updates to the documentation, please include those updates in your pull request.
- If your changes require updates to the README or other project files, please include those updates in your pull
  request.

## Code Style

We use [Ruff](https://docs.astral.sh/ruff/) to enforce code style and formatting in the project. Before submitting a
pull request,
please run the following command to ensure that your code adheres to the project's style guidelines:

```bash
hatch run all
```

This command will run the Ruff linter and formatter on the project's codebase. If there are any issues, Ruff will
provide suggestions for how to fix them. Some issues may be automatically fixed by running the following command:

```bash
hatch run fmt
```
