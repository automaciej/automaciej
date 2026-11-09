---
title: "Task Sync Kotlin"
description: "A family of Kotlin libraries giving an app an offline-first interface to Google Tasks, Microsoft To Do, Todoist and GitHub Issues."
date: "2026-11-09T12:00:00+00:00"
excludeFromRSS: true
layout: app
weight: 9
aliases:
  - /task-sync-kotlin/
params:
  author: "Maciej Bliziński"
  category: "libraries"
  platforms: ["Android"]
---

These are the libraries behind [Task Compass][tc] on Android. iOS provides the
EventKit library which provides you with offline-first, easy to use interface to
Apple Reminders. I wanted something similar for Google Tasks, and realized that
Google only provides you with a REST interface and a simple client library, but
there was nothing I could find to provide offline access.

Libraries are open source and you can use them in your own app.

<!--more-->

[tc]: https://task-compass.app

## What you get

- **Offline-first.** Your app interacts with a local database (Room in the
  Android case). A separate synchronization workflow runs in the background.
  Your app works the same whether the device is online or offline.
- **One API.** `Task`, `TaskList`, `RecurrenceRule` and `SyncStatus` are the
  same for every task source. Each source type says what it can and can't do
  (due times, priorities, labels, moving a task between lists). Your app decides
  how to handle each case.
- **A shared sync engine.** There's a single queue which merges redundant
  changes.

The libraries don't handle logging in.

## The repositories

- [task-sync-kotlin](https://github.com/automaciej/task-sync-kotlin): the
  foundation. The sync engine, the shared task vocabulary, the `TaskStore`
  contract, and the factory that links a source to them. Adding a new source
  takes about 40 lines of service-specific code.
- [google-tasks-kotlin](https://github.com/automaciej/google-tasks-kotlin):
  Google Tasks. Native task moves between lists. The API stores a due date but
  not a due time (explicitly absent from the Google Tasks API unfortunately).
- [microsoft-todo-kotlin](https://github.com/automaciej/microsoft-todo-kotlin):
  Microsoft To Do, over the Microsoft Graph API. Due times, importance and
  structured recurrence. A task deleted elsewhere is only noticed on the next
  full sync: an API limitation.
- [todoist-kotlin](https://github.com/automaciej/todoist-kotlin): Todoist. The
  strangest of the four: projects, priorities, labels, subtasks, and recurrence
  written in plain language.
- [github-issues-kotlin](https://github.com/automaciej/github-issues-kotlin):
  GitHub Issues as a task list, with repositories as lists. Signs in with a
  personal access token.

The source libraries are MIT-licensed, versioned independently, and available
through [JitPack](https://jitpack.io). Each repository's README has the API and
the details.
