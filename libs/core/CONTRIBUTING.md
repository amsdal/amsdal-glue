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

## Release

Before performing the release, it is necessary to merge the latest changes into the `main` branch. On your local computer, switch to the `main` branch, pull the latest changes, and run the `release.sh` script located in the `scripts` folder.

When running the script, you need to provide arguments: the `release date` and the names of the libraries with the required release versions `library_name/release_version`. The script accepts up to 5 commands at a time.

Example:

``` bash
   bash ./scripts/release.sh 01-01-24 api-server/0.1.0 amsdal-glue/0.2.0
```
The script will perform the following actions:
1. Creates a new brunch in release/01-01-24 format.
2. Enter each specified library.
3. Update the changelog.
4. Commit the changes and create a tag.
5. After processing all the specified libraries, push the changes and tags, triggering the necessary CI/CD processes for the releases.

Note! Before executing this command make sure your all changes are committed.
