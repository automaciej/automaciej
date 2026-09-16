---
title: "Why don't you kill it?"
description: "What would I do if I killed it?"
date: "2026-09-16T14:18:42+01:00"
draft: true
tags: ["productivity"]

---

We sat down holding our takeaway coffee cups in gentle autumn sunshine.

-- How's your app doing? \
-- It's about a year in the making, I still haven't got many users, judging by
the update count it's around a hundred. \
-- Why don't you kill it?

An honest question, not mean, not criticizing, just down to earth business
thinking. I paused for a second.

-- Hm, if I killed it, I would first try to buy it. If I couldn't buy it, I'd
build it again.

He nodded.

<!--more-->

Later that day I thought, would there really be a reason to build it again? Maybe a
similar thing already exists? What are the specific things I'm looking for?

1. **"What's my next task?": Answer the question**

   I don't want the app to show me a list and say, "you pick something now." I
   want the default mode of operation to just show me the one thing that's the
   most important for me to do.

2. **"What's my next task?": Don't beg the question**

   The app can't just ask me which task to show on top. That's app's job, not
   mine. The app needs to figure out what questions to ask me, I'll answer those
   questions and the app must use my answers to out what's the #1 task right
   now.

3. **"What's my next task?": Stick to your answer**

   I don't want a process which risks giving me a different answer each time.

4. **No silos**

   I already did the hard work of typing all my tasks in. I am not going to
   retype them, or copy/paste one by one. Single directional import also doesn't
   cut it. It needs to have a live sync with an existing task source, like Apple
   Reminders, Google Task, Todoist, Microsoft To Do, CalDAV, or another place
   that has an API. No silos.

Things I don't care much about:

- Group/team work. App is for personal productivity.
- Deadline handling.
- Any specific platform like iOS or Android.
- Any specific type of user interface. Graphical, web, CLI, are all allowed.
- Free and paid apps are fine.
- Open source or priorietary software is fine.

Things technically covered by requirements above but worth calling out:

- No Eisenhower matrix apps that just ask me in which quadrant each task
  belongs. Quadrants are fine, but the placement is app's job.
- No general focus timers, Kanban boards, or generic siloed task managers.
- No things like "you can make it yourself with Apple Shortcuts". It has to be
  an implemented solution.

I tried looking for an app that meets those criteria. As of September 2026, only
one app I could find meets those... my app. I wondered, how so, are those
criteria so narrow?

Individually, I don't think they are. Each requirement alone is common.

The strongest filter is requirement 2. Productivity designers either punt it to
the user, "you know your priorities, just tell us." Or they use deadlines as
proxy for importance. But this is just a variant of "you know your priorities."
Or they resort to non-deterministic and/or privacy-wise questionable LLM/AI
callouts.

But that's the problem, requirement 2 is hard to solve. How do you have an app
figure out what to ask the user? Then, how to make sense of the answers?

Requirements 1, 3, and 4 are individually common but together, for a business
minded person, they tend to contradict each other. Requirement 1 feels risky,
because "a single task by default" UI challenges even the best UX designers.
What to do with all that empty space? Requirement 3 (on-device, deterministic)
runs against the current trend of everything being a cloud AI.

So what would happen if I killed it? I'd miss the convenience of not having to
manually order my tasks. I would miss having my task pool marshalled, choices
presented and remembered.

From my today's point of view an app that only stores my tasks and lets me drag
them up and down, what problem does it really solve? I would do better just
jotting things down on paper.

Can you imagine a web browser without tabs? It's such an absurd proposition
that... why would you even ask such a question? That's how I feel about tasks
today.
