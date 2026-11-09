---
title: "Task Sync Kotlin"
description: "Kotlin libraries giving an app one offline-first interface to Google Tasks, Microsoft To Do, Todoist and GitHub Issues."
date: "2026-11-09T12:00:00+00:00"
excludeFromRSS: true
app: "task_sync_kotlin"
---

Task lists live in many services, and every one of them has its own API, its own idea of what a task
is, and its own ways of failing when the network drops. Task Sync Kotlin is a set of open-source
Kotlin libraries that hide those differences: an app talks to one `TaskStore` interface, and gets
the same task and list types whichever service is behind it.

<!--more-->

They are the libraries behind [Task Compass](https://task-compass.app) on Android, and you can use
them in your own app.

## What you get

- **Offline-first.** The app reads from a local database (Room on Android) and writes to it first;
  changes sync with the service in the background. The app keeps working without a network.
- **One vocabulary.** `Task`, `TaskList`, `RecurrenceRule` and `SyncStatus` are the same for every
  source. A source declares what it can and can't do (due times, priorities, labels, moving a task
  between lists), and the app branches on that instead of on the service.
- **A shared sync engine.** A queue of pending changes that merges redundant edits, full and
  incremental pulls with detection of deleted tasks, and conflict awareness are written once, in the
  foundation library, not in each source.

The libraries never handle sign-in. The app owns the OAuth flow (or the token the user pastes in)
and hands the library an access token provider.

## The repositories

- [task-sync-kotlin](https://github.com/automaciej/task-sync-kotlin): the foundation. The sync
  engine, the shared task vocabulary, the `TaskStore` contract, and the factory that wires a source
  to them. Adding a new source takes about 40 lines of service-specific code.
- [google-tasks-kotlin](https://github.com/automaciej/google-tasks-kotlin): Google Tasks. Native
  task moves between lists. The API stores a due date but not a due time.
- [microsoft-todo-kotlin](https://github.com/automaciej/microsoft-todo-kotlin): Microsoft To Do, over
  the Microsoft Graph API. Due times, importance and structured recurrence. A task deleted
  elsewhere is noticed on the next full sync.
- [todoist-kotlin](https://github.com/automaciej/todoist-kotlin): Todoist. The richest of the four:
  projects, priorities, labels, subtasks, and recurrence written in plain language.
- [github-issues-kotlin](https://github.com/automaciej/github-issues-kotlin): GitHub Issues as a task
  list, with repositories as lists. Signs in with a personal access token.

The source libraries are MIT-licensed, versioned independently, and available through
[JitPack](https://jitpack.io). Each repository's README has the API and the details.
