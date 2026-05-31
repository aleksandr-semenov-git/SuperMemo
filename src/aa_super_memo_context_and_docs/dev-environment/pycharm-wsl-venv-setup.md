# PyCharm + WSL + virtualenv setup (reusable)

Guide for running a Python project on **Windows host + WSL (Ubuntu)** with PyCharm. Copy/adapt the placeholders for any project.

**Placeholders used below:**

| Placeholder | Example (SuperMemo) |
|-------------|---------------------|
| `{PROJECT_NAME}` | `SuperMemo` |
| `{PROJECT_WSL_PATH}` | `/mnt/c/Users/User/WORK/PycharmProjects/SuperMemo` |
| `{VENV_NAME}` | `SuperMemo` |
| `{PYTHON_VERSION}` | `3.14` |
| `{WSL_DISTRO}` | `Ubuntu` (optional; omit if using default WSL distro) |

---

## Why WSL for the whole workflow

- PyCharm on Windows can use a **WSL interpreter** so code runs in Linux like production/Docker.
- If the terminal stays **PowerShell**, Git may warn about **LF ↔ CRLF** and you mix Windows vs Linux tooling.
- **Rule:** interpreter, terminal, and `pip` should all be WSL — not Windows Python + WSL interpreter.

---

## 1. Install Python in WSL (not only on Windows)

WSL is a separate Linux environment. PyCharm cannot use Windows `python.exe` as the base for a WSL venv.

```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python{PYTHON_VERSION} python{PYTHON_VERSION}-venv
```

Verify:

```bash
python3.14 --version   # adjust version
```

---

## 2. Create virtualenv in WSL

Standard location (works well with PyCharm):

```bash
python3.14 -m venv ~/.virtualenvs/{VENV_NAME}
```

Activate once to confirm:

```bash
source ~/.virtualenvs/{VENV_NAME}/bin/activate
which python
# → /home/<user>/.virtualenvs/{VENV_NAME}/bin/python
deactivate
```

Install deps from project (Django projects usually `src/`):

```bash
cd {PROJECT_WSL_PATH}/src
source ~/.virtualenvs/{VENV_NAME}/bin/activate
pip install -r requirements.txt
```

---

## 3. PyCharm: project interpreter

1. **Settings** → **Project** → **Python Interpreter**
2. Add interpreter → **On WSL** → select `{WSL_DISTRO}` if prompted
3. **Existing** → base: `/usr/bin/python{PYTHON_VERSION}` or the venv binary:
   - `/home/<user>/.virtualenvs/{VENV_NAME}/bin/python`
4. Confirm bottom-right status bar shows the WSL venv (e.g. `Python 3.14 ({VENV_NAME})`)

**Content roots:** project root is usually the repo root; `manage.py` lives under `src/` for SuperMemo — set working directory accordingly when adding run configurations.

---

## 4. PyCharm: default terminal = WSL

1. **Settings** → **Tools** → **Terminal**
2. **Shell path:** `wsl.exe`  
   Or pin a distro: `wsl.exe -d {WSL_DISTRO}`
3. Enable **Activate virtualenv** (see § 5 — may not work alone on Windows PyCharm + WSL)

Close the old PowerShell tab; open a new terminal. Prompt should look like:

```text
user@hostname:/mnt/c/.../ProjectName$
```

Not:

```text
PS C:\Users\...>
```

---

## 5. Auto-activate venv in terminal (`.bashrc` workaround)

**Known issue:** PyCharm on Windows often **does not** auto-activate a WSL venv even when “Activate virtualenv” is checked. The activation script does not cross the Windows → WSL boundary reliably.

**Fix:** append to `~/.bashrc` in WSL:

```bash
# Auto-activate {VENV_NAME} when opening terminal in this project (PyCharm WSL workaround)
if [ "$PWD" = "{PROJECT_WSL_PATH}" ]; then
    source ~/.virtualenvs/{VENV_NAME}/bin/activate
fi
```

Edit:

```bash
nano ~/.bashrc
# paste block at bottom, save: Ctrl+O, Enter, Ctrl+X
```

Reload or open a new PyCharm terminal. Expected prompt:

```text
({VENV_NAME}) user@hostname:/mnt/c/.../ProjectName$
```

**Reuse on another project:** duplicate the `if` block with a different `{PROJECT_WSL_PATH}` and `{VENV_NAME}` (or use a small function — keep it simple unless you have many projects).

**Manual activate** (any time):

```bash
source ~/.virtualenvs/{VENV_NAME}/bin/activate
deactivate   # to leave venv
```

---

## 6. Git on this setup

| Topic | Notes |
|-------|--------|
| **Identity** | `git config user.name` / `user.email` — labels commits only; not auth |
| **Push auth** | Remote hosts require token/SSH/`gh auth login` — not account password |
| **CRLF warning** | Happens when using **Windows** Git/PowerShell on Linux line endings. Using WSL terminal avoids most of this |
| **Optional (Windows Git only)** | `git config --global core.autocrlf true` — prefer WSL Git for project work |

Check local config:

```bash
git config --local --list
```

---

## 7. Checklist (new project)

- [ ] Python `{PYTHON_VERSION}` + `python{PYTHON_VERSION}-venv` installed **in WSL**
- [ ] Venv at `~/.virtualenvs/{VENV_NAME}`
- [ ] PyCharm interpreter → WSL venv
- [ ] Terminal shell path → `wsl.exe` (or `wsl.exe -d {WSL_DISTRO}`)
- [ ] `.bashrc` auto-activate block for `{PROJECT_WSL_PATH}`
- [ ] New terminal shows `({VENV_NAME})` prefix
- [ ] `pip install -r requirements.txt` succeeds inside venv
- [ ] Git commands run from WSL terminal in project root

---

## SuperMemo values (copy-paste)

```bash
# ~/.bashrc snippet
if [ "$PWD" = "/mnt/c/Users/User/WORK/PycharmProjects/SuperMemo" ]; then
    source ~/.virtualenvs/SuperMemo/bin/activate
fi
```

- Venv: `~/.virtualenvs/SuperMemo`
- Python: 3.14 (WSL)
- Project path: `/mnt/c/Users/User/WORK/PycharmProjects/SuperMemo`

---

## Changelog

| Date | Change |
|------|--------|
| 2026-05-31 | Initial guide (from SuperMemo PyCharm/WSL setup) |
