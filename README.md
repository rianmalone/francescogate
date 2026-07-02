# Francesco's Gate 🚪

A personalized "There Is No Game" style puzzle gift site. It looks intentionally
broken/glitchy and the visitor has to figure out how to progress through **3 gates**:

1. **Security Check (face match)** — camera-based identity verification.
2. **Swedish Test** — translate 5 phrases to earn a (fake) Swedish passport & citizenship certificate.
3. **Codeword Puzzle** — the whole alphabet is scattered in an open field; drag the letters so `F R A N C E S C O` line up side by side, in order, anywhere in the field, then `Enter`.

After Gate 3 a short plane-on-a-runway cutscene plays, then it redirects to
`game.html` — a **2D walk-around game** where Francesco (a pixel sprite) roams
a white map (WASD / arrow keys, or the on-screen d-pad on touch).

Built with **plain HTML/CSS/JS** — no frameworks, no build step. Designed to be
opened on a phone via **NFC tap** and is fully mobile responsive + dark mode.

---

## Project structure

```
index.html      # the whole experience (all 3 gates + cutscene)
game.html       # the 2D walk-around game
serve.py        # tiny no-cache local server (so previews never go stale)
assets/         # music.mp3, francesco.jpg, plane.png
assets/sprites/ # Francesco's pixel walk sprites (front/back/side + foot frames)
README.md
```

---

## The game (`game.html`)

- A white map whose border is the screen edge; the **camera does not follow** —
  Francesco moves inside the fixed screen and stops at the borders.
- **Controls:** WASD or arrow keys; an on-screen d-pad appears on touch devices.
- **Sprites** live in `assets/sprites/`. Each direction has a standing frame plus
  two walking frames (left foot / right foot) that alternate while moving.
  Facing *right* reuses the *side* (left-facing) art, mirrored via CSS.
  Edit the `SPRITES` table in `game.html` to swap art.
- **Background:** currently plain white — drop a background image on `.map` in
  `game.html` when you have one (marked with a `TODO`).

### Dev shortcut: skip the puzzle while testing
When served from **localhost**, `index.html` auto-redirects straight to
`game.html` so you don't replay all 3 gates every time. To play the real intro
locally, open **`index.html?full`**. On the deployed site the intro always runs.

---

## Running locally

Because Gate 1 uses the **camera** (`getUserMedia`), browsers require a *secure
context*. `file://` and `http://localhost` both count as secure, so either:

```bash
# any static server works, e.g.:
python3 -m http.server 8000
# then open http://localhost:8000
```

> Camera access over a plain `http://` LAN IP (e.g. from your phone) is blocked.
> Use the deployed HTTPS URL (see Vercel below) when testing on a real phone.

---

## How to swap the background music 🎵

1. Put your track at `assets/music.mp3`.
2. That's it — the `<audio id="bgm">` element in `index.html` already points there.

To use a different filename/format, edit this line in `index.html`:

```html
<source src="assets/music.mp3" type="audio/mpeg" />
```

Notes:
- Music starts on the **first tap/click** anywhere (browsers block autoplay until
  a user gesture) and loops. A 🔊/🔇 mute button sits in the top-right corner.
- Default volume is `0.4` — change `bgm.volume` in the `tryPlayMusic()` function.

### Wrong-answer sound effects 🔔
When a puzzle answer is wrong (Swedish test, or a failed face check), **both**
of these play at the same time:

- `assets/wrong-buzzer.mp3`
- `assets/angry-man.mp3`

Swap either file (keep the names) or edit the two `<audio id="sfxWrong1/2">`
elements. They respect the mute button. Logic lives in the `playWrong()` function.

---

## Where to insert Francesco's reference photo (face matching) 📸

Save his headshot as **`assets/francesco.jpg`** — one file is used for *both*
the passport photo (Gate 2) and the face-match reference (Gate 1). CSS
auto-crops it (`object-fit: cover`) so it frames the face; tweak
`object-position` on `.photo-img` if you want it higher/lower.

The current build uses a **placeholder** that passes after 3 seconds of active
camera. To wire up real matching:

1. Confirm his photo is at `assets/francesco.jpg`.
2. Add face-api.js (e.g. `<script src="https://cdn.jsdelivr.net/npm/face-api.js"></script>`)
   and its model weights.
3. In `index.html`, find the block marked:

   ```js
   // TODO: replace with face-api.js match against reference photo
   ```

   inside `Gate1.runFaceMatch()`. Replace the `setTimeout(...)` placeholder with
   a real detect → descriptor → `faceapi.euclideanDistance()` comparison
   (pass when distance < ~0.5).

Also two spots in the passport/certificate markup are labelled
`<!-- TODO: insert Francesco photo here -->` if you want his face on the documents.

### Hidden bypass
Typing the letters **`francesco`** anywhere on Gate 1 skips the camera check
instantly (no on-screen hint). Handy if the camera misbehaves during the gift reveal.

---

## How to change the Swedish phrases 🇸🇪

In `index.html`, find the `Gate2` block and edit the `PHRASES` array:

```js
const PHRASES = [
  { sv: "Hej, hur mår du?", correct: "Hi, how are you?",
    options: ["Hi, how are you?", "Goodbye, see you soon", "What time is it?", "Where do you live?"] },
  // ...
];
```

- `sv` = the Swedish phrase shown.
- `correct` = the correct English answer (must exactly match one of `options`).
- `options` = the 4 multiple-choice answers (order is shuffled automatically).

All 5 must be answered correctly. A wrong answer shows a sarcastic Italian insult
(edit the `INSULTS` array right below) and reshuffles that question.

---

## Editing / testing tips 🛠️

- **Dev gate-jump:** press `Ctrl+Shift+S` anywhere to jump to any gate. Options
  are logged to the console and offered in a prompt (`boot`, `gate1`, `gate2`,
  `gate3`, `cutscene`).
- Each gate is a `<section class="gate" id="gateN">` with its own clearly-labelled
  JS module (`Gate1` / `Gate2` / `Gate3`) — edit them independently.
- **Italian translations:** every on-screen string has a grey `[IT: …]`
  placeholder underneath (`<span class="it">`). Fill these in later.
- **Glitch vibe:** subtle screen-shake fires randomly; `.glitch` text has a
  flickering shadow. Tune in the `@keyframes flicker` / `shake` CSS.

---

## Deploy to Vercel ▲

No build config needed — it's a static site.

**Option A — CLI**
```bash
npm i -g vercel
cd francescogate
vercel          # follow prompts; accept defaults
vercel --prod   # promote to production
```

**Option B — Git/dashboard**
1. Push this folder to a GitHub repo.
2. On [vercel.com](https://vercel.com) → **New Project** → import the repo.
3. Framework preset: **Other**. Build command: *(none)*. Output dir: `./`.
4. Deploy → you get an `https://` URL (needed for camera access on phones).

For the **NFC tag**, write that production `https://…` URL to the tag.

> Netlify works identically: drag-and-drop the folder at app.netlify.com, or
> connect the repo with no build command.
