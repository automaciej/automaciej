---
title: "Absolute Priorities"
description: "What are absolute task priorities and what's the problem with them."
date: 2025-11-28T09:11:24Z
draft: false
---

Some systems let you set the priority like P0 or P1 for most important tasks,
then P2, P3, and so on.

<!--more-->

- P0
   - Task 1, Task 2, Task 3, Task 4, Task 5
- P1
   - Task 6, Task 7, Task 8
- P2
   - Task 9
   - ...

The result is that we might have buckets with P1, P2, and P3 priorities, but
inside the P1 category we're back to the same problem: which P1 task is the most
important?

| P0 | P1 | P2 |
| --- | --- | --- |
| 5 tasks | 3 tasks | 18 tasks |
| _too many in P0!_ | _about right_ | _"the rest"_ |

To work effectively with absolute priorities (P0, P1, etc), you need to
regularly review them: what's the size of the top priority pool? If it's more
than what you work on, you need to prune it by reassigning some tasks to second
priority. Then you might realize that your second priority pool is now also too
large and you created an entire domino effect. But the worst part is that you
keep re-assessing the same tasks.

| P0 | move ➞ | P1 | move ➞ | P2 |
| --- | --- | --- | --- | --- |
| 5➞1 task | 4 tasks | 3➞5 tasks | 2 tasks | 18➞20 tasks |
| _about right_ | | _about right_ | | _keeps growing_ |

New task comes in which happens to be P1. Now we have:

| P0 | P1 | P2 |
| --- | --- | --- |
| 1 task | 5➞6 tasks | 20 tasks |
| | _new task<br>P1 pool<br>too large now_ | |

Now you need to re-assess the P1 task pool and decide which task is going to be
moved to P2.

| P0 | P1 | need to move | P2 |
| --- | --- | --- | --- |
| 1 task | 6➞5 tasks | 1 task| 20➞21 tasks |
| | _need to reasses<br>all P1 tasks_ | |

Task Compass [philosophy][phil] is different: instead comparing tasks against
each other. This effectively automates the above work.

[phil]: {{% relref philosophy.md %}}
