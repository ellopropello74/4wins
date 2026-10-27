# Vier gewinnt (Connect Four)

Dieses Projekt ist die stabile Spielbasis für die BELL. Die vorhandene
Pygame-Oberfläche, Spielsteine, Menüs, Sounds und der lokale Zwei-Spieler-Modus
bleiben erhalten. Die Regeln liegen in GameBoard und benötigen weder Pygame
noch Mausereignisse oder den Event-Bus. Ein Minimax-Gegner ist absichtlich noch
nicht enthalten.

## Starten

Voraussetzung ist Python 3.9 oder neuer. Im Projektordner:

~~~bash
python -m pip install -r requirements.txt
python main.py
~~~

game.py bleibt als kompatibler Startpunkt verfügbar (python game.py).
Unter Windows kann statt python je nach Installation py verwendet werden.
In GitHub Codespaces muss die grafische Desktop-Weiterleitung laufen; dort
können die Variablen wie folgt gesetzt werden:

~~~bash
export DISPLAY=:1
export SDL_AUDIODRIVER=dummy
python main.py
~~~

## Aufbau und Zuständigkeiten

- main.py: empfohlener Programmeinstieg.
- game.py: Pygame-Hauptmenü und Zustandswechsel zwischen Menü, Spiel, Pause
  und Spielende.
- connect_game.py: verbindet Eingaben und Darstellung mit den Regeln,
  verwaltet Züge und bietet den Einstiegspunkt für eine spätere KI.
- game_board.py: reine Spiellogik, Brettzustand, legale Züge, Kopieren,
  Simulation, Gewinn- und Remiserkennung.
- game_data.py: Laufzeitdaten der Oberfläche und aktueller Spieler.
- game_renderer.py, assets.py, config.py: Zeichnen, Grafiken, Sounds und
  Farben.
- events.py: bestehender Event-Bus und Ereignistypen der Oberfläche.
- tests/: automatisierte Regel- und Schnittstellentests.

## Spielfeld und Spieler

Das Brett ist eine Liste von rows Zeilen mit je cols Einträgen. Im normalen
Spiel ist board eine Liste mit 6 Zeilen und 7 Spalten. Indizes beginnen bei
null: board[row][column]. Zeile 0 ist die unterste Reihe; Spalte 0 ist links.
Die Zellen enthalten Ganzzahlen: 0 bedeutet leer, 1 Spieler 1 (rot), 2
Spieler 2 (gelb). GameData.current_player gibt den nächsten Spieler als 1
oder 2 zurück.

## Schnittstelle für KI-Implementierungen

Die Regeln können direkt und ohne grafische Initialisierung verwendet werden:

~~~python
board.get_valid_moves()                 # list[int], nullbasierte Spalten
board.get_next_open_row(column)         # int oder None, nullbasierte Zeile
board.copy()                            # unabhängiges GameBoard
board.simulate_move(column, player)     # neue Position, Original unverändert
board.play_move(column, player)         # ändert dieses Brett; gibt die Zeile zurück
board.winning_move(player)              # list[(row, column)] oder None
board.get_winner()                      # 1, 2 oder None
board.is_draw()                         # bool
board.is_terminal()                     # Sieg oder Remis: bool
~~~

Ungültige Züge lösen bei play_move und simulate_move ValueError aus.
Nach einem Sieg oder Remis liefert get_valid_moves() eine leere Liste.

Eine spätere KI implementiert das Protokoll aus ai_interface.py:

~~~python
def choose_move(board: GameBoard, player: int, difficulty: Difficulty) -> int:
    ...
~~~

difficulty ist "easy", "medium" oder "hard"; player ist 1 oder 2.
ConnectGame.choose_ai_move(ai_player, difficulty) übergibt der KI eine
unabhängige Brettkopie und den aktuellen Spieler. Der Rückgabewert ist eine
validierte, nullbasierte Spaltennummer vom Typ int. Ein unbekannter
Schwierigkeitswert oder ein ungültiger KI-Zug löst ValueError aus. Nach
Spielende löst die Anfrage RuntimeError aus. ConnectGame.play_move(column)
führt einen Zug des aktuellen Spielers aus und gibt bool zurück (angenommen oder
abgelehnt). Die KI darf keine Oberfläche, Sounds oder Event-Bus-Objekte
benötigen. Die Schwierigkeit ist nur ein Eingabeparameter; Suchtiefe und
Bewertungsverfahren bleiben der späteren Implementierung überlassen.

## Abgrenzung für den Vergleich

Die gemeinsame Basis und ai_interface.py sollten für alle vier Assistenten
unverändert bleiben. Jeder Assistent sollte seine Implementierung in einer
eigenen Datei unter ai/ ergänzen und dort nur KI-spezifische Tests hinzufügen.
So bearbeiten alle dasselbe Protokoll, während Spielregeln und Schnittstelle
gemeinsam bleiben. game_board.py, connect_game.py, game_data.py und die
Oberflächendateien sind Teil der gemeinsamen Basis und keine KI-Lösungsdateien.

## Tests

Die Tests verwenden das in Python enthaltene unittest; zusätzliche
Test-Frameworks sind nicht erforderlich. Im Projektordner ausführen:

~~~bash
python -m unittest discover -s tests -v
~~~

Abgedeckt sind legale Züge, volle Spalten, horizontale/vertikale/diagonale
Siege, ein volles Standardbrett ohne Gewinner, unabhängige Kopien,
Zugsimulation, gültige Züge, terminale Zustände und der KI-Aufrufvertrag.
