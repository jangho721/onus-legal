# On/Us — Legal Pages

Static pages served at `https://joinonus.app/privacy`, `/terms`, and `/support` through GitHub Pages.

This repo is public on purpose: GitHub Pages on the free plan only serves from a public repo, and this repo holds no app source code or secrets, only these pages.

## Source of truth

`privacy/index.html` and `terms/index.html` are generated from the On/Us main repo (private): `docs/legal/privacy_policy.md` and `terms_of_service.md`.

To update them after editing those Markdown files, with both repos checked out as siblings:

```
pip install markdown
python3 scripts/convert_legal.py
git commit -am "update legal pages"
git push
```

Do not hand-edit `privacy/index.html` or `terms/index.html` — edit the Markdown in the main repo and regenerate.

`support/index.html` and `index.html` have no Markdown source; edit them directly.
