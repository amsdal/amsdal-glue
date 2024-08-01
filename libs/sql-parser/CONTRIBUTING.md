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

In order to release new version, you need to run the following command:

```bash
hatch run release RELEASE_VERSION
```

Replace `RELEASE_VERSION` to your current version that you are going to release, e.g. `0.0.10` (without leading `v`)
This command will generate change logs, commit, create a tag and push.

Note! Before executing this command make sure your all changes are committed.
