# Release Updates

Use when a product update reaches users and needs an announcement. Most updates need no announcement; the translation step decides which do.

## Inputs

- Merged change records: titles and descriptions explain the reason better than commit messages do.
- The commit log, for changes merged without a record.
- Release notes, if the team writes them.
- Feature-flag state: what users can reach today, not what is merged.

## Rules

1. Market only what users can use today. Flagged, internal-beta, or undeployed changes wait.
2. Translate each change into one line: "You can now ..." or "... no longer ...". A change with no such line gets no announcement. Refactors, dependency bumps, CI, and test changes get none.
3. Tier each change:

   | Tier | Typical change | Output |
   |---|---|---|
   | Major | New capability, new plan, large workflow change | Changelog entry, blog post, email, in-app message, social post |
   | Medium | New integration, UX change users notice, speed gain users feel | Changelog entry, targeted email or in-app message, one social post |
   | Minor | Fixes and small polish | Changelog entry only, batched |

   Bundle several medium changes that share a theme into one major story.
4. State what the change does for the reader, and only what the record supports. Use a number only if the change record supplies it. Credit a requesting user only when the team credits users and that user agreed.
5. If the record says the change is partial ("phase one", "first step"), the announcement says so.
6. Check the site, docs, comparison pages, and ads for claims the change makes false: a new limit, a renamed plan, a removed integration, a changed price. List each one for the owner.
7. Each change that adds search demand (a new integration, a new comparison) goes on the content backlog.
8. Spread a Major change's outputs over days or weeks, not one day. Reuse the announcement format that drew the most response in past records.
