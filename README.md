# mixreveal-site

Public site for **Mix & Reveal: Color Puzzle** (TonTech). Static GitHub Pages project site:
https://tontechco.github.io/mixreveal-site/

- `/` landing, `/privacy/`, `/terms/`, `/support/`
- `/i/<CODE>`: invite page, `/c/<ID>`: challenge page. Project Pages cannot route, so GitHub serves
  `404.html` for any unknown path; its script reads the code from the URL, validates it against the
  friend-code format (`MIX-` + 4 of `ABCDEFGHJKLMNPQRSTUVWXYZ23456789`, see the game's
  `server/nakama/src/consts.ts`) or a 16-hex challenge id, and shows the inviter, the store buttons
  (auto-redirect on phones after 2.5 s unless the visitor touches the page) and "Open it"
  (`mixreveal://invite/<code>` / `mixreveal://challenge/<id>`).
- The page POSTs `{kind, id}` as `text/plain` to `https://mixreveal-api.tontech.co/claim` (the game's
  Node service, `server/links.js`) for the inviter's name and avatar. On iPhone that call also records
  the 2-hour deferred-invite claim (salted hash of the IP /24 or /48 prefix; no clipboard, unlike
  Saffron's copy-code button: the game asks "Were you invited by {name}?" instead). The API only
  accepts the origin `https://tontechco.github.io` with a Referer under `/mixreveal-site/`.
- Android: the Play button carries `referrer=mr_inv=<code>&mr_c=<id>`, read once by the game through
  the Play Install Referrer API.
- `assets/`: app icon (from the game repo), `og.png` (1200x630 share image), the art row,
  `site.css`. Regenerate the PNGs with `python3 tools/make_assets.py ~/IdeaProjects/MixReveal`.

Links use root-relative `/mixreveal-site/...` paths so `404.html` works at any depth. To preview
locally, serve the parent folder so the site sits under `/mixreveal-site/` and unknown paths return
`404.html`, e.g. `python3 tools/serve.py` (port 8765), then open
`http://127.0.0.1:8765/mixreveal-site/i/MIX-ABCD?api=http://127.0.0.1:<node port>`.

## Link previews

GitHub Pages answers `/i/...` and `/c/...` with HTTP status **404** (it is `404.html`), and some
preview crawlers skip pages that are not 200. So the game does not share these URLs directly: it
shares `https://mixreveal-api.tontech.co/i/<code>` (and `/c/<id>`), a 200 page with Open Graph tags
(inviter name, `assets/og.png`) that sends people here with a script redirect. Crawlers do not run
the script. The server's `LINK_BASE_URL` switches between the two; the game accepts both.

## Universal Links / App Links: later

`apple-app-site-association` and `assetlinks.json` must be served from the root of a host, which a
project page cannot do. Until a custom domain (or the org's `tontechco.github.io` repo) is used, the
game registers the `mixreveal://` scheme only. Do not edit `tontechco.github.io` for this.

Edit the HTML by hand; keep the privacy policy in sync with the game's App Privacy answers
(`docs/RELEASE.md` and `docs/INVITES.md` in the game repo). Store ids: `appStoreId` and `playLive` in
the `CONFIG` block of `404.html`, plus the badges in `index.html`.
