# Far Sight — myopia prevention project website

The entire website is one file: **`index.html`**. Photos live in **`images/`**.
No build step, no framework, nothing to install. Edit the file, commit, and the live site updates.

---

## 1. Put it on GitHub (once, ~5 minutes)

1. Go to <https://github.com/new>. Name the repository (e.g. `far-sight-site`), set it **Public**, and click **Create repository**.
2. On the new repo page click **uploading an existing file**.
3. Drag in `index.html` **and** the `images` folder, then click **Commit changes**.
4. Go to **Settings → Pages**. Under *Build and deployment*, set **Source: Deploy from a branch**, **Branch: `main` / `(root)`**, and click **Save**.
5. Wait about a minute, then reload that page. GitHub shows the live address:
   `https://<your-username>.github.io/far-sight-site/`

That address is the real website. Every commit from now on republishes it automatically.

## 2. Give your partners access

**Settings → Collaborators → Add people** → their GitHub username → they accept the emailed invite.
Collaborators can edit files and commit directly. There is no other setup.

## 3. How to edit (in the browser, no software needed)

1. Click `index.html` in the repo.
2. Click the **pencil icon** (top right of the file).
3. Make the change.
4. Scroll down, write a short note in *Commit changes* (e.g. "added Dr. Li's profile"), click **Commit changes**.
5. Wait ~60 seconds and refresh the live site.

### Where things are

| To change | Search the file for | What to do |
|---|---|---|
| Any unwritten text | `[` | Every `[square bracket]` is a placeholder — replace it, brackets included |
| The big hero headline | `Protecting young eyes` | Replace the words between `<h1>` and `</h1>` |
| A photo placeholder | `class="frame"` | Replace the whole `<div class="frame">…</div>` with `<img src="images/your-photo.jpg" alt="who is in the photo">` |
| An expert's portrait | `class="portrait"` | Upload the photo to `images/`, then change the `src="…"` |
| A video | `video-frame` | Replace the block with the YouTube embed code (YouTube → Share → Embed) |
| Team names | `[Teammate 2 Full Name]` | Replace all three |
| Colours | `--accent:` | Change the hex codes near the top of the `<style>` block |

### Adding a photo

1. Open the `images` folder in the repo → **Add file → Upload files** → commit.
2. In `index.html`, reference it as `images/your-file-name.jpg`.
   Keep file names lowercase with hyphens, no spaces.

## 4. Two rules that prevent 99% of breakage

- **Never delete a `<` or `>`.** Change the words *between* the tags, not the tags themselves.
- **If something looks broken, undo it.** Open the repo's **Commits** list, find the last good one, and use **Revert**. Nothing is ever permanently lost.

## 5. Working with more than one person at a time

For two or three people, editing `main` directly is fine — just don't edit the same file at the same minute.
If you would rather review each other's work first: when committing, choose **Create a new branch and start a pull request**. The other person reviews and clicks **Merge**. The live site only changes on merge.

## 6. Still to do before launch

- [ ] Replace the project name (`Far Sight`) if you want a different one — it appears in the header, footer and `<title>`
- [ ] Fill in every `[bracketed]` placeholder
- [ ] Add the hero image or short film
- [ ] Paste real YouTube embeds into the interview cards
- [ ] Verify the three statistics on the home page against their cited sources
- [ ] Get written permission from every expert whose photo and name appear
- [ ] Turn off the "Fill-in guide" button before launch, or ask for it to be removed entirely

---

Educational content only — not medical advice.
