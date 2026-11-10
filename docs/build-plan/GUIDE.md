# Build plan: guide

This folder says in what order the product is built. It follows from the requirements
and the architecture. The common method is in `docs/build-method.md`.

It can be one document or several. What usually belongs here (a reminder, not a form;
add, drop or merge as the project needs):

- **Milestones:** checkpoints where a group of features is finished and the product
  works. The first one is the foundation: shared modules, quality gates and CI.
- **Implementation plan:** the order of the work, what depends on what, what can run
  in parallel.
- **Test strategy:** which kinds of tests the project needs at the start. Tests are
  expected to change during the build.
- **Definition of done:** when the whole project counts as finished.
- **Configuration per milestone:** where a milestone differs from the default
  (helpers, review, effort, caps, settings), with the reason. The values go in
  `factory-setup/parameters.json`.
- **Which documentation changes need Daniel's approval** during the build.
