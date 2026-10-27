import sys
from pathlib import Path
from os.path import join
from pygame.image import load


def resource_path(relative_path):
    base_path = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    return str(base_path / relative_path)


# The path to the event sound file.
event_sound = resource_path(join("sounds", "event.ogg"))

# The path to the first disc drop sound file.
disc_drop_1 = resource_path(join("sounds", "disc_drop_1.wav"))

# The path to the second disc drop sound file.
disc_drop_2 = resource_path(join("sounds", "disc_drop_2.wav"))

# Load the red coin image from the images folder.
red_coin = load(resource_path(join("images", "redball90px.png")))

# Load the yellow coin image from the images folder.
yellow_coin = load(resource_path(join("images", "yellowball90px.png")))

# Load the black coin image from the images folder.
black_coin = load(resource_path(join("images", "blackball91px.png")))
