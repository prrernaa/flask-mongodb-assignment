# Git Branching 

> **GitHub Repository:** https://github.com/prrernaa/flask-mongodb-assignment

---

## Task 1 — SSH Setup, Clone & Username Branch

### Step 1: Generate SSH Key
Generate an ED25519 SSH key and add the public key to GitHub Settings → SSH Keys.
```bash
ssh-keygen -t ed25519 -C "prernajangra02@gmail.com"
cat ~/.ssh/id_ed25519.pub
```

### Step 2: Configure SSH for Port 443 (WSL Fix)
Since WSL can block default SSH port 22, configure Git to use port 443 via ssh.github.com:
```bash
nano ~/.ssh/config
```
Add the following:
```
Host github.com
  Hostname ssh.github.com
  Port 443
  User git
```
Test the connection:
```bash
ssh -T git@github.com
# Expected: Hi prrernaa! You've successfully authenticated...
```

### Step 3: Clone Repository
Create an empty repo on GitHub (no README), then clone it using SSH:
```bash
git clone git@github.com:prrernaa/flask-mongodb-assignment.git
cd flask-mongodb-assignment
cp -r ~/devops-assignment/flask-assignment/* .
```

### Step 4: Initial Commit to main
```bash
git config --global user.name "prrernaa"
git config --global user.email "prernajangra02@gmail.com"
git add .
git commit -m "Initial commit - Add Flask MongoDB project files"
git push -u origin main
```

### Step 5: Create Username Branch & Merge to main
```bash
git checkout -b prrernaa
git push -u origin prrernaa
git checkout main
git merge prrernaa
git push origin main
```

---

## Task 2 — prrernaa_new Branch & Conflict Resolution

### Step 1: Create prrernaa_new Branch and Update data.json
```bash
git checkout -b prrernaa_new
nano data.json   # Updated with 4 new entries
git add data.json
git commit -m "Update data.json with new entries in prrernaa_new branch"
git push -u origin prrernaa_new
```
> Updated entries: Prerna Sharma, Raj Mehta, Sneha Gupta, Amit Kumar

### Step 2: Merge prrernaa_new into main
```bash
git checkout main
git merge prrernaa_new
# Result: Fast-forward merge — no conflict
git push origin main
```

### Step 3: Conflict Resolution (if applicable)
If a merge conflict occurs:
```bash
nano data.json
# Delete <<<<<<< HEAD, =======, >>>>>>> markers
# Keep prrernaa_new content only
git add data.json
git commit -m "Resolve conflict - accept changes from prrernaa_new"
git push origin main
```

---

## Task 3 — master_1 & master_2 Branches

### Step 1: Create master_1 and master_2 from main
```bash
git checkout main
git checkout -b master_1
git push -u origin master_1
git checkout main
git checkout -b master_2
git push -u origin master_2
```

### Step 2: master_1 — Create To-Do Frontend Page
```bash
git checkout master_1
nano templates/todo.html
# Form with: Item Name (text input) and Item Description (textarea)
git add templates/todo.html
git commit -m "Add To-Do frontend page with Item Name and Item Description fields"
git push origin master_1
```

### Step 3: master_2 — Create /submittodoitem Backend Route
```bash
git checkout master_2
nano app.py
# Added /todo GET route and /submittodoitem POST route
# Inserts itemName and itemDescription into MongoDB todos collection
git add app.py
git commit -m "Add /submittodoitem backend route to store todo items in MongoDB"
git push origin master_2
```

### Step 4: Merge master_1 and master_2 into main
```bash
git checkout main
git merge master_1
git push origin main
git merge master_2   # Save merge commit in editor (Ctrl+X)
git push origin main
git log --oneline
```

---

## Task 4 — Separate Commits, Git Reset & Rebase

### Step 1: Add 3 Fields with Separate Commits (in master_1)
```bash
git checkout master_1

# First commit: Item ID
nano templates/todo.html
git add templates/todo.html
git commit -m "Add Item ID field to To-Do form"

# Second commit: Item UUID
nano templates/todo.html
git add templates/todo.html
git commit -m "Add Item UUID field to To-Do form"

# Third commit: Item Hash
nano templates/todo.html
git add templates/todo.html
git commit -m "Add Item Hash field to To-Do form"

git push origin master_1
```

### Step 2: Merge master_1 into main
```bash
git checkout main
git merge master_1
git push origin main
git log --oneline
# All 3 commits visible: Item ID, Item UUID, Item Hash
```

### Step 3: Git Reset --soft to Item ID Commit
Roll back to the commit where only Item ID was added, keeping changes staged:
```bash
git reset --soft b8a79b2
git status
# Shows: Changes to be committed — app.py and templates/todo.html staged
git log --oneline
# HEAD is now at b8a79b2 — Add Item ID field to To-Do form
```

### Step 4: Re-commit and Force Push
```bash
git commit -m "Reset to Item ID only - recommit state"
git push origin main --force
# Force push required because history was rewritten with git reset
```

### Step 5: Rebase main into master_1
```bash
git checkout master_1
git rebase main
# Rebases master_1 on top of main, preserving all individual commits
git log --oneline
git push origin master_1 --force
```

---

## Branch Summary

| Branch        | Purpose          | Key Action                        |
|---------------|------------------|-----------------------------------|
| `main`        | Primary branch   | All features merged here          |
| `prrernaa`    | Username branch  | Initial Flask project files       |
| `prrernaa_new`| Updated data     | Updated data.json entries         |
| `master_1`    | Frontend branch  | To-Do page + 3 extra fields       |
| `master_2`    | Backend branch   | /submittodoitem POST route        |
