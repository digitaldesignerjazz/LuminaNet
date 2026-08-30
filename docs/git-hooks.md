# Git Hooks — LuminaNet

Hooks liegen versioniert in `.githooks/`, nicht in `.git/hooks`.  
`.git/hooks` wird nicht mitgeklont und wäre bei jedem Klon tot.

## Einmal aktivieren

Im geklonten Repo:

```bash
cd ~/LuminaNet
chmod +x tools/install-hooks.sh
./tools/install-hooks.sh
```

Das setzt lokal:

```bash
git config core.hooksPath .githooks
```

Prüfen:

```bash
git config --get core.hooksPath
ls -l .githooks
```

## Was läuft

| Hook | Wann | tut |
|---|---|---|
| `pre-commit` | vor jedem Commit | blockiert `.env`, Keys, `*_state.md`; parst JSON; läuft `validate.py` wenn Schema-Dateien staged sind |
| `commit-msg` | nach der Nachricht | Betreff ≤ 72 Zeichen, kein Key-Text, Hinweis auf `type: subject` |
| `pre-push` | vor `git push` | `validate.py`, falls `python3-jsonschema` da ist |

Fehlt `jsonschema`, warnen die Hooks und lassen den Rest durch. Die Kante bleibt dann CI-Sache.

```bash
sudo apt install -y python3-jsonschema
```

## Umgehen (bewusst, selten)

```bash
git commit --no-verify -m "docs: notfall"
git push --no-verify
```

Nicht zur Gewohnheit machen. `--no-verify` umgeht genau den Schutz, der Secrets aus `main` fernhalten soll.

## Abschalten

```bash
git config --unset core.hooksPath
```

## Warum nicht Husky / pre-commit.com

v0.1 bleibt bei Bash + python3. Kein Node, kein extra Framework. Ein Klon plus `./tools/install-hooks.sh` reicht.
