# Release notes

The general flow is the following:

1. create a topic branch and make your changes there
2. run `hatch run change-logs create -c "Added a cool feature!" cool-feature.added.md`
3. It will create a `./release_notes/cool-feature.added.md` file. Do not forget to commit this file.
4. That's it.

These newly created change logs will be available on docs.amsdal.com in the next release.

Note, the `cool-feature.added.md` file name contains several parts separated by `.`:

1. `cool-feature` - the code of this change. Keep it short, simple, and unique.
2. `added` - it's a type of change. See all available types below.

The supported types of changes:

- `added`
- `removed`
- `changed`
- `deprecated`
- `security`
- `fixed`
- `performance`

For example, if your changes related to `performance` optimizations use `performance` type, e.g. 
`hatch run change-logs create -c "Optimized SQL JOIN statement."  sql-join.performance.md`
---
## Release

Before performing the release, you need to update the release version in the `__about__.py` file, which is located at `libs/folder_where_release_will_be/src/library_name/__about__.py`.

Next, you need to merge the latest changes into the main branch. To do release:

1. Switch to the `main` branch on your local computer.
2. Pull the latest changes from the remote repository.
3. Run the `release.sh` script located in the `scripts` folder.
4. When running the script, you need to specify the following arguments: the `release_date` and the folder names in the `libs` directory with the required versions in the format `folder_name/release_version`. The script accepts up to 5 variables at a time.

Example:

``` bash
   bash ./scripts/release.sh 01-01-24 api-server/0.1.0 amsdal-glue/0.2.0
```
The script will perform the following actions:
1. Creates a new brunch in release/01-01-24 format.
2. Enter each specified library.
3. Update the changelog.
4. Commit the changes and push.


After running the script, you need to create a pull request, review all changes, and then merge the `release branch` into the `main` branch. This action will trigger the CI/CD pipeline, which will check the version changes, create the necessary tags, and push them to the `main` branch. After that, CI/CD processes will be triggered to perform the release

## NOTE!
The script `scripts/tag_check.sh` handles checking for changes and creating tags. If you are adding new services to `libs`, you also need to modify the `tag_check.sh` file to include the new directory for checking.

Additions should be made in the following format:

    folder_tags["./libs/folder_name_where_changes_are_to_be_checked/src/library_name"]="tag_name_that_should_trigger_CI/CD"
The tag name should be provided without any additional symbols at the end, like '`/`' or '`/v`'.
