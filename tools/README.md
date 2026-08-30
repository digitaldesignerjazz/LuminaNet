# Tools

Auf vielen Debian/Ubuntu-Systemen heißt der Interpreter `python3`. `pip` und `python` sind oft nicht installiert.

## Schnellster Weg

```bash
sudo apt update
sudo apt install -y python3 python3-jsonschema
chmod +x tools/run-validate.sh
./tools/run-validate.sh
```

## Alternative ohne apt-Paket

```bash
sudo apt install -y python3 python3-pip python3-venv
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r tools/requirements.txt
python3 tools/validate.py
```

`.venv/` bleibt lokal und steht in `.gitignore`.
