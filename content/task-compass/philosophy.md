---
title: "Philosophy of Task Compass"
description: "Why Task Compass exists, and the principles that guide its design."
date: "2025-09-03T09:00:00+01:00"
lastmod: "2025-11-26T18:30:00+01:00"
---

# Main principles

1. Respect how human mind works
2. Don't do the same work twice
3. Learn from what we do, now what we say

<!--more-->

I built Task Compass because I was frustrated. I've been using to-do lists for
years, on paper and in apps. Writing tasks down solved the problem of forgetting
what to do, but it didn't solve the problem of tracking what's important. The
second issue was that looking at the to-do list would overwhelm me, because my
brain thought that I have to do those tasks all at once.

## 1. Respect How Our Minds Work

### Pairwise comparisons are the first class citizen

We are not good at assigning an absolute score to individual list items. We're
slightly better at stack-ranking. We excel at *comparing* things.

{{< reminder_comparison
    title1="Buy milk" desc1="1L, full"
    title2="Bring the coat to the tailor" desc2="Remember the buttons"
    >}}

This is a natural, intuitive question. It doesn't demand a complex internal
rating system; it's a simple, honest choice.

This process offloads the rest of the cognitive burden of prioritization to the
app.

### Looking at the entire list not required

When you open Task Compass, you're not presented with a long to-do list.

1. If there's still prioritization work to be done, you're shown two tasks and
   asked to choose the more important one.

2. If prioritization is complete, the app shows you your #1 priority and a
   button to start the Pomodoro timer.

3. If you want to see more, you can see your #2 and #3 tasks.

## 2. Do the work only once

The app remembers your decisions, so it won't ask you about the same two tasks
twice. It builds an internal importance ranking based on your choices, but it
won't overwhelm you with the entire list; the whole point is that you only need
to see your most important task at any given moment.

If you said that A is more important than B, the app will always put A above B
in the ranking.

As you keep using the app, it will ask you for comparisons that are necessary to
update the importance ranking.

## 3. Detect Resistance Automatically

There's often a gap between our intentions and our actions. We *say* a task is
our #1 priority, but then we spend three days avoiding it. Your actions speak
louder than your words.

Task Compass listens to your actions. It doesn't ask you to guess how
"difficult" a task will be. It simply watches what you complete. If an important
task keeps sitting on your list, the app recognizes this as **resistance**. It
learns what you're avoiding, and helps you address it.

## How It's Implemented


