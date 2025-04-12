> pour lire la documentation en français, cliquez [ici](https://github.com/Tostenn/Commitly/blob/main/docs/français/readme.md)

## 🧠 The Problem: The Empty Commit Syndrome

![Empty illustration](https://cdn.jsdelivr.net/gh/Tostenn/Commitly/images/vide.jpeg)

You've just wrapped up an intense coding session. You proudly type:

```bash
git add .
git commit ""
```

And then… nothing.

The cursor blinks, the quotes are empty, and **no idea** comes to mind. How do you summarize what you just did? How do you stick to your commit conventions? Should you mention the ticket? Where? How?

That’s where **Commitly** comes in.

---

# 🚀 What is Commitly?

Commitly is a Python library that leverages artificial intelligence to automatically generate a **well-structured commit message** based on your staged changes (`git diff --cached`).

No more empty commit syndrome. Commitly gives you a clear, contextual message — with or without a ticket — in French or English, and tailored to your team’s standards.

---

## ⚙️ Features

### `__init__(model=gpt_4o_mini, file_temp="commit.txt", lang="fr")`

Creates a Commitly instance.

- `model`: AI model to use (default is `gpt_4o_mini` via [g4f](https://github.com/xtekky/gpt4free)).
- `file_temp`: temporary file to store the generated message before committing.
- `lang`: language for commit generation (`fr` or `en`).

---

### `add(file: str) -> bool`

Adds a specific file to the Git staging area.

```python
commitly.add("app/models/user.py")
```

Equivalent to:

```bash
git add app/models/user.py
```

---

### `generate_commit_message(style_commit=None, format_commit=None, recommandation_commit=None, ticket=None) -> str`

Automatically generates a commit message based on the current staged diff (`git diff --cached`).

- `style_commit`: customize commit style (type, scope, etc.).
- `format_commit`: overall message format.
- `recommandation_commit`: writing guidelines or hints.
- `ticket`: optional ticket identifier to include in the footer.

> **⚠️ Note**: If there are no staged changes, this method raises a `DiffEmptyException`.

---

### `save_message_to_file(message: str) -> bool`

Saves a generated commit message to the specified temporary file (default: `commit.txt`).

```python
commitly.save_message_to_file(message)
```

Useful if you want to reuse this file in a `git commit` command.

---

### `commit() -> bool`

Commits changes using the message stored in the temporary file. Deletes the file after committing.

```python
commitly.commit()
```

---

### `push()`

Runs a `git push` to send your commit to the remote repository.

```python
commitly.push()
```

---

### `unstage(file: str)`

Removes a file from staging (same as `git reset <file>`).

```python
commitly.unstage("README.md")
```

---

### `_run_cmd(cmd: str, return_code: bool = False)`

Internal method to run shell commands. Returns either:

- the command output (`stdout`)
- or the exit code (`0` or `1`) if `return_code=True`

---

## 🧪 Full Example

```python
from commitly import Commitly

commitly = Commitly()
commitly.add("main.py")
message = commitly.generate_commit_message(ticket="#42")
commitly.save_message_to_file(message)
commitly.commit()
commitly.push()
```

---

## 📸 Visual Demo

![Full example](https://cdn.jsdelivr.net/gh/Tostenn/Commitly/images/exemple-1.png)

---

## 🧩 About the Commit Format

The generated message follows this structure:

```text
<type>[optional scope]: <description>

[optional body]

[optional footer]  ← ticket here (#1234)
```

Common types:
- `feat`: new feature
- `fix`: bug fix
- `docs`: documentation
- `refactor`: code improvement without behavior change
- `chore`: miscellaneous tasks (maintenance, updates, etc.)

---

## 📋 License

MIT © 2025 Kouya Chance Boman Tosten

---

> Say goodbye to the empty commit syndrome. Let **Commitly** tell your code’s story.

---

Dis-moi si tu veux un badge PyPI (une fois publié), ou une version anglaise des images (si nécessaire) !