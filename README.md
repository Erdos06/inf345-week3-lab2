# INF 345 — Week 1 Practice

**Fundamentals of DevOps · Fall 2026 · SDU University**

---

## What you will have at the end of this session

1. A GitHub account.
2. Git working on your own laptop.
3. A change of yours, reviewed automatically by a machine, merged into a shared repository.

That third one is the whole course in miniature. Everything we do for the next
fourteen weeks is a bigger version of what you are about to do in fifty minutes.

You are also, along the way, registering yourself for the course. There is no
separate form. **If you do not complete this lab, I do not have your GitHub
username, and I cannot give you any assignment for the rest of the semester.**

Deadline: **Sunday 21 September, 23:59 Almaty time.** Finishing during the
session is expected; the deadline is for the ones who hit a wall.

---

## Before we start

Have open:

- This page.
- A browser, signed in to GitHub. If you do not have an account yet, make one
  now at [github.com/signup](https://github.com/signup) — it takes two minutes
  and it is free. **Choose your username carefully: you will use it for the
  rest of your career, and I will use it to grade you all semester.** Your real
  name or something close to it. Not `xXx_killer_2007_xXx`.

That is all. Do not install anything yet.

---

## There are two tracks

| | Track A — terminal | Track B — browser |
|---|---|---|
| You use | Git on your own laptop | github.com only |
| Takes | ~35 minutes | ~10 minutes |
| Choose it if | Your laptop is yours and you can install software | You cannot install anything today, or Track A is fighting you |

**Start with Track A.** If you are stuck for more than five minutes at any
step, switch to Track B, finish the lab, and come back to Track A as homework.
Getting the submission in matters more than how you got it in.

Track B students: you must still complete Track A before the Week 2 practice.
Everything from Week 2 onwards assumes a working terminal.

---

# Track A — the terminal

## A1. Install Git

**Windows** — download and run [git-scm.com/download/win](https://git-scm.com/download/win).
Accept every default. When it finishes you will have a program called **Git Bash**
in your Start menu. Open it. That is your terminal for this course — not
PowerShell, not cmd.

**macOS** — open Terminal and type `git --version`. If a dialog offers to
install developer tools, accept it. Otherwise you already have Git.

**Linux** — you know what to do. `sudo apt install git` or your distro's equivalent.

Check it worked:

```bash
git --version
```

You should see something like `git version 2.51.0`. A version number — any
version number — means you are fine.

## A2. Tell Git who you are

Git stamps your name onto every commit you make. Set it once:

```bash
git config --global user.name "Your Full Name"
git config --global user.email "your.address@sdu.edu.kz"
```

Use the same email as your GitHub account, or GitHub will not connect your
commits to your profile.

Check:

```bash
git config --global --list
```

## A3. Fork this repository

On this repository's page on GitHub, click **Fork** (top right), then
**Create fork**.

You now have your own complete copy at
`github.com/<your-username>/inf345-week1-lab`. Nothing you do to it can damage
the original. This is the first useful property of Git: copies are cheap and
safe.

## A4. Clone your fork

On *your* fork's page, click the green **Code** button, make sure **HTTPS** is
selected, and copy the URL.

In your terminal:

```bash
cd ~
git clone https://github.com/<your-username>/inf345-week1-lab.git
cd inf345-week1-lab
```

> We are using HTTPS today, not SSH. SSH keys are Week 3. If a browser window
> opens asking you to authorise Git, say yes.

## A5. Make your branch

```bash
git checkout -b add-<your-username>
```

For example: `git checkout -b add-aisha-nurlanqyzy`

A branch is a private workspace. You will never commit directly to `main`
again, in this course or in a job.

## A6. Write your file

Copy the example and open it in a text editor:

```bash
cp students/EXAMPLE.yml students/<your-username>.yml
```

The filename must be **exactly** your GitHub username, lowercase, ending in
`.yml`. The check will reject anything else.

Now edit that new file. Use VS Code, Notepad, `nano`, whatever you like:

```yaml
name: Your Full Name
github: your-username
group: A
os: windows
email: you@sdu.edu.kz
```

- `group:` is **A** if your practice session is at 12:30, **B** if it is at 13:30.
- `os:` is `windows`, `macos` or `linux`.
- `email:` is optional, but if you include it, it must be your SDU address.
- Every colon is followed by a space. This is the single most common mistake.

## A7. Commit

```bash
git add students/<your-username>.yml
git commit -m "Add <your-username> to roster"
```

`git add` chooses what goes in. `git commit` records it, permanently, with your
name and the time on it. The time on it is what I grade.

## A8. Push

```bash
git push origin add-<your-username>
```

## A9. Open a pull request

Go back to your fork on GitHub. There will be a yellow banner —
**Compare & pull request**. Click it.

Check the top of the page carefully. It should read:

> base repository: **`inf345/inf345-week1-lab`** base: `main` ← head repository: **`<your-username>/inf345-week1-lab`** compare: `add-<your-username>`

Title it `Add <your-username>`. Click **Create pull request**.

## A10. Watch the machine grade you

Within about thirty seconds a check appears at the bottom of your pull request.

- 🟡 Yellow — it is running. Wait.
- ✅ Green — you are done. Go to "What just happened" below.
- ❌ Red — **this is normal and costs you nothing.** Click **Details**, read the
  error message, fix your file, then:

```bash
git add students/<your-username>.yml
git commit -m "Fix roster entry"
git push
```

The check runs again by itself. Repeat until green. There is no penalty for a
red check — only for no check at all.

---

# Track B — the browser

No installation. Everything on github.com.

1. On this repository's page, click **Fork**, then **Create fork**.
2. On your fork, open the `students` folder and click on `EXAMPLE.yml`.
3. Click the **pencil** icon to edit it.
4. Change the filename at the top of the editor from `EXAMPLE.yml` to
   `<your-github-username>.yml` — your username, lowercase.
5. Replace the contents with your own details (see step A6 above for the fields).
6. Click **Commit changes…**. Choose **Create a new branch for this commit**,
   then **Propose changes**.
7. On the next page, check that the base repository is the course repository
   and not your fork, then click **Create pull request**.
8. Wait for the check, exactly as in step A10.

Then install Git at home and do Track A before Week 2.

---

## What just happened

You did, on a small scale, the thing this entire course is about:

- You worked on a **copy**, not on the live thing. Nothing you did could break anything.
- You made your change on a **branch**, isolated from everyone else's work.
- You **proposed** the change rather than applying it. Someone else decides whether it lands.
- A **machine checked it automatically**, in seconds, in the same way for all fifty of you, at three in the morning if that is when you pushed.
- The check told you **what** was wrong rather than just that something was.

Now replace "a YAML file with your name in it" with "a change to a banking
system used by two million people", and you have the job.

The file that ran that check is
[`.github/workflows/validate.yml`](.github/workflows/validate.yml). It is about
sixty lines and it is commented. Open it. You are not expected to understand it
yet — you will write your own in Week 4 — but look at it now, so that when we
get there it is already familiar.

---

## Stuck?

In the session: say so immediately in the chat. Do not lose fifty minutes to a
missing space.

After the session: email me — `INF 345` and your group in the subject line,
from your `@sdu.edu.kz` address. Include the **link to your pull request** and
a screenshot of the error. I reply within two working days.

**Helping each other is encouraged.** Explaining a fix to a classmate is how
you learn it. Sending them your file to copy is not — and every commit here is
timestamped and attributed, so it is visible.
