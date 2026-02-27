# File System Emulator - Complete Demo Guide

This guide will help you demonstrate how Operating Systems organize files. No coding knowledge required!

---

## What is This?

This is a computer program that simulates how different operating systems organize files. It shows three different ways computers can store and organize your documents, just like real operating systems do.

---

## How to Start (Very Simple)

### Step 1: Open the Program

1. Find the folder called "os" on your computer
2. Open it
3. Double-click on the file named `main.py` OR
4. If that doesn't work, open your terminal/command prompt and type:
   ```
   python main.py
   ```
5. Press Enter

You should see something like this:
```
============================================================
  File System Emulator
  Demonstrating OS Directory Structures
============================================================

Type 'help' for commands or 'demo' to see a demonstration

[HIERARCHICAL] /$ 
```

The `[HIERARCHICAL] /$` is where you type commands.

---

## Quick Demo (Easiest Way)

Just type `demo` and press Enter. The program will automatically show you everything!

---

## Manual Demo (Step-by-Step)

### Part 1: Single-Level Mode (The Simplest Way)

This is how very old computers (like early 1980s) organized files - everything in one big pile.

**Type these commands one by one:**

1. `mode single` 
   - Press Enter
   - This switches to the simplest file organization
   - You'll see: `[SINGLE] /$`

2. `create fileA.txt`
   - Press Enter
   - Creates a file named "fileA.txt"
   - You'll see: `Created file 'fileA.txt' (XX.XKB)`

3. `create fileB.txt`
   - Press Enter
   - Creates another file

4. `mkdir folder`
   - Press Enter
   - **This will show an ERROR** - this is normal!
   - Error message: `ERROR: Subdirectories not allowed in Single-Level structure`
   - **This proves** that Single-Level mode doesn't allow folders inside folders

5. `ls`
   - Press Enter
   - Shows all files in a nice table
   - You'll see only fileA.txt and fileB.txt - no folders

**What to say:** "In the old days, computers couldn't organize files into folders. Everything was just in one big list. That's what Single-Level mode shows."

---

### Part 2: Two-Level Mode (Better Organization)

This is how some systems organized files for multiple users - each user gets their own folder.

**Type these commands:**

1. `mode two-level`
   - Press Enter
   - Switches to Two-Level mode
   - You'll see: `[TWO-LEVEL] /$`

2. `mkdir User1`
   - Press Enter
   - Creates a folder for User1

3. `mkdir User2`
   - Press Enter
   - Creates a folder for User2

4. `cd User1`
   - Press Enter
   - "cd" means "change directory" (go into a folder)
   - Now you're inside User1's folder
   - You'll see: `[TWO-LEVEL] /User1$`

5. `create doc.txt`
   - Press Enter
   - Creates a file inside User1's folder

6. `mkdir subfolder`
   - Press Enter
   - **This will show an ERROR** - this is normal!
   - Error message: `ERROR: Maximum depth (2 levels) exceeded`
   - **This proves** that Two-Level mode only allows 2 levels of folders

7. `cd ..`
   - Press Enter
   - Goes back to the previous folder (up one level)
   - You'll see: `[TWO-LEVEL] /$`

8. `tree`
   - Press Enter
   - Shows a visual tree of all folders and files
   - You'll see something like:
   ```
   /
   ├── User1/
   │   └── doc.txt [XX.XKB | XX:XX]
   └── User2/
   ```

**What to say:** "Two-Level mode is like giving each person their own folder. But you can't go deeper than that - no folders inside folders inside folders."

---

### Part 3: Hierarchical Mode (Modern Computers)

This is how modern computers organize files - unlimited folders inside folders, just like you're used to.

**Type these commands:**

1. `mode hierarchical`
   - Press Enter
   - Switches to Hierarchical mode
   - You'll see: `[HIERARCHICAL] /$`

2. `mkdir Home`
   - Press Enter
   - Creates a Home folder

3. `cd Home`
   - Press Enter
   - Go into the Home folder
   - You'll see: `[HIERARCHICAL] /Home$`

4. `mkdir Documents`
   - Press Enter
   - Creates a Documents folder inside Home

5. `mkdir Pictures`
   - Press Enter
   - Creates a Pictures folder inside Home

6. `cd Documents`
   - Press Enter
   - Go into the Documents folder
   - You'll see: `[HIERARCHICAL] /Home/Documents$`

7. `create resume.pdf`
   - Press Enter
   - Creates a resume file

8. `cd ..`
   - Press Enter
   - Go back to Home folder

9. `cd ..`
   - Press Enter
   - Go back to the root (top level)
   - You'll see: `[HIERARCHICAL] /$`

10. `tree`
    - Press Enter
    - Shows the complete tree structure
    - You'll see something like:
    ```
    /
    └── Home/
        ├── Documents/
        │   └── resume.pdf [XX.XKB | XX:XX]
        └── Pictures/
    ```

11. `search "*.pdf"`
    - Press Enter
    - Searches for all PDF files
    - You'll see: `Found 1 result(s) for '*.pdf':`
    - And the path: `/Home/Documents/resume.pdf`

**What to say:** "This is how modern computers work. You can have folders inside folders as deep as you want. This is what we use every day!"

---

### Part 4: Viewing Information

**Type these commands:**

1. `ls`
   - Press Enter
   - Shows a table with:
     - Name (file/folder name)
     - Type (File or Dir)
     - Size (how big it is)
     - Created (when it was made)

2. `pwd`
   - Press Enter
   - Shows your current location
   - Example: `/Home/Documents`

3. `logs`
   - Press Enter
   - Shows a history of everything you've done
   - Each operation is logged with time and details

---

## All Commands Explained Simply

| Command | What It Does | Example |
|---------|--------------|---------|
| `mode single` | Switch to simple mode (no folders in folders) | `mode single` |
| `mode two-level` | Switch to user mode (max 2 levels deep) | `mode two-level` |
| `mode hierarchical` | Switch to modern mode (unlimited folders) | `mode hierarchical` |
| `create filename` | Create a new file | `create report.txt` |
| `mkdir foldername` | Create a new folder | `mkdir Documents` |
| `delete name` | Delete a file or empty folder | `delete oldfile.txt` |
| `cd foldername` | Go into a folder | `cd Documents` |
| `cd ..` | Go back to previous folder | `cd ..` |
| `cd /` | Go to the top level | `cd /` |
| `pwd` | Show where you are | `pwd` |
| `ls` | List all files and folders | `ls` |
| `tree` | Show visual tree of everything | `tree` |
| `search word` | Find files matching a word | `search report` |
| `search *.txt` | Find all text files | `search *.txt` |
| `reset` | Start fresh (delete everything) | `reset` |
| `help` | Show all commands | `help` |
| `exit` | Close the program | `exit` |

---

## Tips for a Great Demo

### Before You Start
- Make sure you have Python installed (most computers have it)
- Practice the commands once before showing someone
- Keep this guide open for reference

### During the Demo
1. **Start with the demo command** - Type `demo` first to show everything automatically
2. **Explain each mode** - Tell them what makes each mode special
3. **Show the errors** - The error messages are actually features! They prove the rules work
4. **Use the tree command** - It's the most visual and impressive part
5. **Try search** - Show how you can find files anywhere in the system

### Common Questions People Ask

**Q: Why are the file sizes random?**
A: Since this is a simulation, we don't actually store real files. The sizes are randomly generated to look realistic.

**Q: Can I save my work?**
A: This is a demonstration program, so everything is temporary. Type `reset` to start fresh anytime.

**Q: What do the symbols in the tree mean?**
A: `├──` means "this item has more items below it" and `└──` means "this is the last item at this level."

**Q: Why can't I create folders in Single-Level mode?**
A: That's the whole point! Single-Level mode shows how old computers worked - they couldn't organize files into folders at all.

**Q: What's the difference between Two-Level and Hierarchical?**
A: Two-Level is like giving each person one folder. Hierarchical is like giving each person unlimited folders inside folders.

---

## Quick Reference Card

Print this or keep it handy:

```
START: python main.py

QUICK DEMO: demo

MODES:
  mode single         - Simple, no folders in folders
  mode two-level      - Users get folders, max 2 levels
  mode hierarchical   - Modern, unlimited folders

FILES:
  create name.txt     - Make a file
  mkdir name          - Make a folder
  delete name         - Remove file/folder

NAVIGATION:
  cd name             - Go into folder
  cd ..               - Go back
  cd /                - Go to top
  pwd                 - Show location

VIEW:
  ls                  - List contents
  tree                - Show tree
  search *.txt        - Find files

OTHER:
  reset               - Start over
  help                - Show help
  exit                - Quit
```

---

## Troubleshooting

**Problem: Program won't start**
- Solution: Make sure Python is installed. Type `python --version` to check.

**Problem: Commands don't work**
- Solution: Make sure you press Enter after each command. Check for typos.

**Problem: Can't see what I typed**
- Solution: The program might be waiting for input. Just press Enter.

**Problem: Want to start over**
- Solution: Type `reset` and press Enter. This clears everything.

---

## What This Demonstrates

This program shows three important concepts about how computers organize files:

1. **Single-Level**: The simplest way - everything in one list (like old computers)
2. **Two-Level**: Better organization - each user gets a folder (like early multi-user systems)
3. **Hierarchical**: Modern way - unlimited folders inside folders (like your computer today)

Each mode has strict rules that are enforced automatically. This is exactly how real operating systems work!

---

## Need Help?

If something doesn't work or you have questions:
1. Type `help` in the program
2. Check this guide
3. Try the `demo` command again
4. Type `reset` to start fresh

---

**Enjoy demonstrating how computers organize files!** 🎉
