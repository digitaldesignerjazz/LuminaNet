# Git-Fehlerbaum — LuminaNet

Zuerst immer den Ort prüfen. Die meisten »Git-Fehler« sind Verzeichnisfehler.

```bash
pwd
ls -la
```

LuminaNet gilt nur in einem Ordner, der `.git/` enthält — üblicherweise `~/LuminaNet`.

---

## 1. `fatal: not a git repository`

**Bedeutung:** Git findet in diesem Ordner und seinen Eltern kein `.git`.

**Typischer Auslöser:** Befehl in `~` statt im Klon.

```bash
# falsch
cd ~
git pull

# richtig
cd ~/LuminaNet && git status
```

**Wenn `~/LuminaNet` fehlt:**

```bash
cd ~
git clone https://github.com/digitaldesignerjazz/LuminaNet.git
cd LuminaNet
git status
```

**Wenn der Ordner existiert, aber kein `.git` hat:**
Es ist eine Kopie ohne Historie (Zip, scp). Entweder löschen und neu klonen oder:

```bash
cd ~/LuminaNet
git rev-parse --is-inside-work-tree || echo "kein repo — neu klonen"
```

Nicht `git init` in einem halbvollen Ordner anlegen, wenn das Ziel der öffentliche Klon ist. Das erzeugt ein zweites, leeres Repo und verwirrt jeden weiteren `pull`.

---

## 2. `chmod: cannot access 'tools/...'` / `No such file or directory`

**Bedeutung:** Das Skript ist nicht *hier*. Fast immer Folge von Punkt 1.

```bash
cd ~/LuminaNet
ls tools/start-luminanet.sh
chmod +x tools/start-luminanet.sh tools/run-validate.sh
```

---

## 3. `command not found: git`

```bash
sudo apt update
sudo apt install -y git python3
git --version
```

---

## 4. `Could not resolve host: github.com`

Netz oder DNS. Kurztest:

```bash
ping -c 2 github.com
curl -I https://github.com
```

VPN/Tor/Proxy prüfen. Ohne Namensauflösung hilft kein `clone`.

---

## 5. `Repository not found` oder `403`

LuminaNet ist öffentlich. Diese Meldung heißt meist:

- Tippfehler im Pfad (`LuminaNET`, `lumina-net`)
- gespeicherte Credentials einer anderen Identität
- SSH-Remote ohne passenden Key

Öffentlich reicht HTTPS:

```bash
git remote -v
# erwartet:
# origin  https://github.com/digitaldesignerjazz/LuminaNet.git
```

Setzen falls falsch:

```bash
git remote set-url origin https://github.com/digitaldesignerjazz/LuminaNet.git
git fetch --prune
```

---

## 6. `Permission denied (publickey)` bei SSH

Du nutzt `git@github.com:...`, aber kein Key ist geladen.

Sofortweg: auf HTTPS wechseln (für dieses öffentliche Repo ausreichend).

```bash
git remote set-url origin https://github.com/digitaldesignerjazz/LuminaNet.git
git pull
```

---

## 7. `failed to fetch` / `unable to access` / Zertifikat

Uhr falsch, Proxy, oder altes CA-Bundle.

```bash
timedatectl status
sudo apt install -y ca-certificates
```

Nicht `GIT_SSL_NO_VERIFY=1` zur Gewohnheit machen.

---

## 8. `Your local changes would be overwritten by merge`

Lokale Änderungen blockieren `pull`.

Ansehen:

```bash
git status
git diff
```

Weg A — behalten:

```bash
git stash push -u -m "lokal"
git pull --ff-only
git stash pop
```

Weg B — verwerfen (endgültig):

```bash
git reset --hard HEAD
git pull --ff-only
```

---

## 9. `rejected non-fast-forward` / `fetch first`

Remote ist voraus. Erst holen, dann — nur wenn du wirklich pushen willst — integrieren.

```bash
git fetch origin
git log --oneline --decorate --graph HEAD..origin/main
git pull --ff-only origin main
```

Kein `push --force` auf `main`, solange andere mitlesen.

---

## 10. `dubious ownership` / `unsafe repository`

Ordner gehört einem anderen User als dem, der Git startet (typisch nach `sudo`).

```bash
ls -ld ~/LuminaNet
# reparieren:
sudo chown -R "$USER:$USER" ~/LuminaNet
```

Nicht dauerhaft `git config --global --add safe.directory` als Ersatz für falsche Besitzrechte.

---

## 11. Detached HEAD

```bash
git status
# "HEAD detached at ..."
git switch main
```

---

## 12. Merge-Konflikt

```bash
git status
# Dateien mit <<<<<<< ansehen, bereinigen, dann:
git add <datei>
git commit
```

In LuminaNet v0.1 lieber Konflikt vermeiden: lokale Spielereien in einer Branch `local-lab`, `main` sauber halten.

```bash
git switch -c local-lab
```

---

## Schnelldiagnose (eine Minute)

```bash
echo "PWD=$(pwd)"
command -v git && git --version
test -d .git && echo "HIER IST EIN REPO" || echo "HIER IST KEIN REPO"
test -f tools/luminanetd.py && echo "KNOTEN DA" || echo "KNOTEN FEHLT"
git remote -v 2>/dev/null
git status -sb 2>/dev/null
```

Erwartetes Bild nach korrekt geklontem Stand:

```
PWD=/home/<du>/LuminaNet
HIER IST EIN REPO
KNOTEN DA
origin  https://github.com/digitaldesignerjazz/LuminaNet.git
## main...origin/main
```
