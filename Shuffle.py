#Exceptions
class EmptyPlaylistError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)

#imports
import os
from random import randint
import sys

#Hide the annoying Pygame support prompt printed at the start of the console.
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

from pygame import Surface
from pygame.font import Font

pygame.init()

#Variables
playList: list[str] = []
playedSongs: list[int] = []
allPlayedSongs: list[int] = []
folderPath: str = os.getcwd()

pokemonFontPath = os.path.join(folderPath, "Pokemon Solid.ttf")

running: bool = True

count: int = 0
secondsPassed: int = 0
songCount: int = 0
currentSong: int = 0

pokemonFont: Font = pygame.font.Font(pokemonFontPath, 30) 

tick: float = 0.0
startTick: int = pygame.time.get_ticks()

paused: bool = False

back: bool = False

loop: bool = False
getCurrentTime: bool = False

#Set the screen:
screenInfo = pygame.display.Info()

screenW: int = screenInfo.current_w
screenH: int = screenInfo.current_h - 10

screen: Surface = pygame.display.set_mode((screenW, screenH))
screen.fill((0, 0, 0))

#Check for the amount of items in the playlist
def checkItems() -> bool:
    """
        Checks if there are any MP3 files in the playlist.

    Returns:
        bool: Whether there are any MP3 files in the playlist.
    """

    if len(playList) == 0:
        return False
    else:
        return True

#Go through the current folder the script is in
def goThroughFolder(folder: str) -> list[str]:
        for _, item in enumerate(os.listdir(folder), start=1):
            itemPath = os.path.join(folder, item)
            if os.path.isfile(itemPath) and item.upper().endswith(".MP3"):
                playList.append(f"{item}")
            
        return playList

#Get the amount of items
def numberOfItemsInFolder(folderPath: str) -> list[str]:

    """
    _summary_
        Takes a folder path and returns a list of the MP3 files in the folder.

    Raises:
        FileExistsError: Raises if the folder does not exist.
        FileNotFoundError: Raises if no mp3 files are found in the folder.

    Returns:
        list[str]: A list of the MP3 files in the folder. 
    """

    if not os.path.exists(folderPath):
        raise FileExistsError(f"Folder '{folderPath}' Does not exist!")

    goThroughFolder(folderPath)

    return playList

#Convert seconds to the format MM:SS
def minutesAndSecond(seconds: int) -> tuple[str, str, str]:
    """
    _summary_
        Takes a number of seconds and returns the number of minutes and seconds as a tuple.

    Returns:
        tuple[str, str]: a tuple of minutes and seconds.
    """
    minutes: int | float = seconds // 60
    remainingSeconds: int = seconds % 60
    hours: int = remainingSeconds // 60 // 60

    minutesStr: str = str(minutes).zfill(2)
    secondsStr: str = str(remainingSeconds).zfill(2)
    hoursStr: str = str(hours).zfill(2)

    return hoursStr, minutesStr, secondsStr

#Code

songs = numberOfItemsInFolder(folderPath)
print("Current Playlist:")

#Check for items in the playlist
playlistHasItems: bool = checkItems()

if not playlistHasItems:
    raise EmptyPlaylistError("Playlist has no items.")

#For each song in the playlist, print the number and the song name.
for eachSong in songs:
    count += 1
    print(f"{count}: {eachSong.replace(".mp3", "")}")

#Main loop
while running:
    pygame.time.Clock.tick(pygame.time.Clock(), 60)

    currentTick: float = (pygame.time.get_ticks() - startTick) / 1000

    if not back and not loop:
        songCount += 1
        currentSong = randint(0, len(songs) - 1)

    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

#If the number of songs played is equal to the number of songs in the playlist, clear the list.
    if len(playedSongs) == len(playList):
        playedSongs.clear()

#If a song generated is already in the list of played songs, keep generating until a new song is found.
    while currentSong in playedSongs and not back and not loop:    
        currentSong = randint(0, len(songs) - 1)

    if not back and not loop:
        playedSongs.append(currentSong)

    pygame.mixer.music.load(os.path.join(folderPath, str(songs[currentSong])))
    pygame.mixer.music.play()

    song: pygame.mixer.Sound = pygame.mixer.Sound(os.path.join(folderPath, str(songs[currentSong])))

#Print the current song being played.
    songRightNow: str = f"{songCount}: Currently Playing: {songs[currentSong].replace('.mp3', '')}"
    nameFont: Font = Font(pokemonFontPath, len(songRightNow) // 4)

    songText: Surface = nameFont.render(songRightNow, True, (255, 255, 255))
    screen.blit(songText, ((screenW - songText.get_width()) // 2, ((screenH - songText.get_height()) // 2) - 30))

    songLoopedText: Surface = pokemonFont.render(f"Song Looped: {loop}", True, (255, 255, 255))

    pygame.display.flip()

    allPlayedSongs.append(currentSong)

#Get the length of the song in seconds.
    audioLength: int = int(song.get_length())
    hours: str = minutesAndSecond(audioLength)[0]
    minutes: str = minutesAndSecond(audioLength)[1]
    seconds: str = minutesAndSecond(audioLength)[2]

    back = False

#While the song is playing, print the current time of the song.
    while pygame.mixer.music.get_busy() and running or paused:

        tick = (pygame.time.get_ticks() - startTick) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused

                    print(paused)
                elif event.key == pygame.K_RIGHT:

                    pygame.mixer.music.stop()

                elif event.key == pygame.K_LEFT:
                    if songCount > 1:
                        currentSong = allPlayedSongs[songCount - 2]
                        allPlayedSongs.pop(songCount - 1)
                        playedSongs.pop(songCount - 1)

                        songCount -= 1

                        back = True

                        pygame.mixer.music.stop()

                elif event.key == pygame.K_d:
                    secondsPassed += 5 if secondsPassed < audioLength else audioLength

                    pygame.mixer.music.set_pos(secondsPassed)

                elif event.key == pygame.K_a:
                    secondsPassed = 0 if secondsPassed < 5 else secondsPassed - 5

                    pygame.mixer.music.set_pos(secondsPassed)

        screen.fill((0, 0, 0))

        if tick - currentTick >= 1 and not paused:
            secondsPassed += 1
            currentTick = (pygame.time.get_ticks() - startTick) / 1000
            tick = 0.0

        if paused:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

        Hours: str = minutesAndSecond(secondsPassed)[0]
        Minutes: str = minutesAndSecond(secondsPassed)[1]
        Seconds: str = minutesAndSecond(secondsPassed)[2]

        text = pokemonFont.render(f"{Hours}:{Minutes}:{Seconds}/{hours}:{minutes}:{seconds}", True, (255, 255, 255))
        screen.blit(text, ((screenW - text.get_width()) // 2, (screenH - text.get_height()) // 2))

        songText = nameFont.render(songRightNow, True, (255, 255, 255))
        screen.blit(songText, ((screenW - songText.get_width()) // 2, ((screenH - songText.get_height()) // 2) - 50))

        pygame.display.flip()

#Reset the amount of time passed.
    secondsPassed = 0
    tick = 0.0

pygame.quit()
sys.exit()
