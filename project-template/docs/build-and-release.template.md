# Build & release — how we ship {{PROJECT_NAME}}

From source to something running in front of users. Covers the build, the
environments, and how a version gets out the door.

## Build

```bash
# FILL: the command(s) that produce the artifact — binary, image, bundle, package.
# Include what the output is and where it lands.
```

- **Artifact:** <!-- FILL: docker image / npm package / static bundle / wheel / … -->
- **Output location:** <!-- FILL: registry, dist/, etc. -->

## Environments

<!-- FILL: the environments this runs in and how they differ. Delete rows you
     don't have. Each should say how it's configured and who can deploy to it. -->

| Env | Purpose | How it's deployed | Config source |
| --- | --- | --- | --- |
| local | dev loop | `docs/development.md` | `.env` |
| staging | pre-prod verification | | |
| production | live | | |

## Release process

<!-- FILL: the actual steps to cut a release. Tag? Merge to main? Manual approval?
     Automated on merge? Be explicit — this is the doc people read at 2am. -->

1. 
2. 

## Versioning

<!-- FILL: the scheme (SemVer / CalVer / commit-sha) and what triggers a bump.
     Where the version number lives and how the changelog is maintained. -->

## Rollback

<!-- FILL: how to undo a bad release, fast. The command or the runbook link.
     If there's no rollback path, say so loudly — that's a risk, not a blank. -->

## CI/CD

<!-- FILL: link the pipeline. What runs on PR, what runs on merge to main, what
     runs on tag. What gates a deploy (green tests, approval, both?). -->
