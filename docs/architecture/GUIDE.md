# Architecture: guide

This folder says how the product is organized inside. The agent leads it. Daniel
approves a plain-language summary and any decision that changes the product.

It can be one document or several. What usually belongs here (a reminder, not a form;
add, drop or merge as the project needs):

- **Component breakdown:** the modules or parts, what each one does, how they connect,
  and how a new feature plugs in.
- **Core domain model:** the central concepts, rules and calculations of the product,
  whatever they are in this project.
- **Cross-cutting concerns:** what every part must do the same way, and the shared
  module that does it.
- **Data model:** what information is stored and how it relates.
- **Domain rules and glossary:** the facts of the field, with sources, and the
  vocabulary.
- **Architecture decision records:** each choice of stack or infrastructure, with the
  alternatives considered and the reason.
- **Quality gates:** the automatic checks and the tool for each: formatter, linter,
  type checker, tests, and others the project needs. Use the standard tools of the
  stack with their default rules. Write custom rules only for this project's own
  structure.

Ask what a professional in the field of this product would settle at the start, and
settle it here.
