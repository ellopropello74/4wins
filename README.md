## 🖥️ Ausführung in GitHub Codespaces (GUI)

Wenn du diese Projekt in GitHub Codespaces öffnen möchtest sind zusätzliche Schritte erforderlich, um das Fenster im Browser anzuzeigen.

### 1. Virtuellen Desktop öffnen
1. Klicke im VS Code Terminal-Bereich auf den Reiter **Ports**.
2. Suche den Port **6080** (Label: "desktop").
3. Klicke auf das Weltkugel-Icon (**Open in Browser**).
4. Es öffnet sich ein neuer Tab mit einem virtuellen Desktop (Passwort falls nötig: `vscode`).

### 2. Programm starten
Kopiere den folgenden Befehl in dein **Codespaces-Terminal**, um alle nötigen Variablen (Grafikumleitung und Audio-Dummy) zu setzen und das Spiel zu starten:

```bash
export DISPLAY=:1 && export SDL_AUDIODRIVER=dummy && python main.py
