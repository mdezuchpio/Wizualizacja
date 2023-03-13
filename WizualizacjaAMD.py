import tkinter as tk
import pyodbc
from functools import partial
from sys import exit
import re

# JSON z układem stacji
stacje = {
    "PS2_711": {
        "702": [
            {
                "miejsce_start": 2,
                "miejsce_koniec": 20,
                "stacja_1": 10,
                "stacja_2": 11,
            }
        ],
        "711": [
            {
                "miejsce_start": 3,
                "miejsce_koniec": 21,
            }
        ],
    },
    "PS2_712": {
        "702": [
            {
                "miejsce_start": 21,
                "miejsce_koniec": 37,
                "stacja_1": 27,
                "stacja_2": 28,
            }
        ],
        "711": [
            {
                "miejsce_start": 22,
                "miejsce_koniec": 38,
            }
        ],
    },
    "PS2_713": {
        "702": [
            {
                "miejsce_start": 38,
                "miejsce_koniec": 54,
                "stacja_1": 44,
                "stacja_2": 45,
            }
        ],
        "711": [
            {
                "miejsce_start": 39,
                "miejsce_koniec": 55,
            }
        ],
    },
    "PS2_714": {
        "702": [
            {
                "miejsce_start": 55,
                "miejsce_koniec": 71,
                "stacja_1": 61,
                "stacja_2": 62,
            }
        ],
        "711": [
            {
                "miejsce_start": 56,
                "miejsce_koniec": 72,
            }
        ],
    },
    "PS2_715": {
        "702": [
            {
                "miejsce_start": 72,
                "miejsce_koniec": 88,
                "stacja_1": 78,
                "stacja_2": 79,
            }
        ],
        "711": [
            {
                "miejsce_start": 73,
                "miejsce_koniec": 89,
            }
        ],
    },
    "PS2_716": {
        "702": [
            {
                "miejsce_start": 89,
                "miejsce_koniec": 105,
                "stacja_1": 95,
                "stacja_2": 96,
            }
        ],
        "711": [
            {
                "miejsce_start": 90,
                "miejsce_koniec": 106,
            }
        ],
    },
    "PS2_717": {
        "702": [
            {
                "miejsce_start": 106,
                "miejsce_koniec": 125,
                "stacja_1": 112,
                "stacja_2": 113,
            }
        ],
        "711": [
            {
                "miejsce_start": 107,
                "miejsce_koniec": 126,
            }
        ],
    },
    "PS2_721": {
        "722": [
            {
                "miejsce_start": 3,
                "miejsce_koniec": 21,
                "stacja_1": 15,
                "stacja_2": 16,
            }
        ],
        "731": [
            {
                "miejsce_start": 3,
                "miejsce_koniec": 21,
            }
        ],
    },
    "PS2_722": {
        "722": [
            {
                "miejsce_start": 22,
                "miejsce_koniec": 38,
                "stacja_1": 32,
                "stacja_2": 33,
            }
        ],
        "731": [
            {
                "miejsce_start": 22,
                "miejsce_koniec": 38,
            }
        ],
    },
    "PS2_723": {
        "722": [
            {
                "miejsce_start": 39,
                "miejsce_koniec": 55,
                "stacja_1": 49,
                "stacja_2": 50,
            }
        ],
        "731": [
            {
                "miejsce_start": 39,
                "miejsce_koniec": 55,
            }
        ],
    },
    "PS2_724": {
        "722": [
            {
                "miejsce_start": 56,
                "miejsce_koniec": 72,
                "stacja_1": 66,
                "stacja_2": 67,
            }
        ],
        "731": [
            {
                "miejsce_start": 56,
                "miejsce_koniec": 72,
            }
        ],
    },
    "PS2_725": {
        "722": [
            {
                "miejsce_start": 73,
                "miejsce_koniec": 89,
                "stacja_1": 83,
                "stacja_2": 84,
            }
        ],
        "731": [
            {
                "miejsce_start": 73,
                "miejsce_koniec": 89,
            }
        ],
    },
    "PS2_726": {
        "722": [
            {
                "miejsce_start": 90,
                "miejsce_koniec": 106,
                "stacja_1": 100,
                "stacja_2": 101,
            }
        ],
        "731": [
            {
                "miejsce_start": 90,
                "miejsce_koniec": 106,
            }
        ],
    },
    "PS2_727": {
        "722": [
            {
                "miejsce_start": 107,
                "miejsce_koniec": 126,
                "stacja_1": 117,
                "stacja_2": 118,
            }
        ],
        "731": [
            {
                "miejsce_start": 107,
                "miejsce_koniec": 126,
            }
        ],
    },
    "PS2_731": {
        "752": [
            {
                "miejsce_start": 3,
                "miejsce_koniec": 21,
                "stacja_1": 10,
                "stacja_2": 11,
            }
        ],
        "761": [
            {
                "miejsce_start": 3,
                "miejsce_koniec": 21,
            }
        ],
    },
    "PS2_732": {
        "752": [
            {
                "miejsce_start": 22,
                "miejsce_koniec": 38,
                "stacja_1": 27,
                "stacja_2": 28,
            }
        ],
        "761": [
            {
                "miejsce_start": 22,
                "miejsce_koniec": 38,
            }
        ],
    },
    "PS2_733": {
        "752": [
            {
                "miejsce_start": 39,
                "miejsce_koniec": 55,
                "stacja_1": 44,
                "stacja_2": 45,
            }
        ],
        "761": [
            {
                "miejsce_start": 39,
                "miejsce_koniec": 55,
            }
        ],
    },
    "PS2_734": {
        "752": [
            {
                "miejsce_start": 56,
                "miejsce_koniec": 72,
                "stacja_1": 61,
                "stacja_2": 62,
            }
        ],
        "761": [
            {
                "miejsce_start": 56,
                "miejsce_koniec": 72,
            }
        ],
    },
    "PS2_735": {
        "752": [
            {
                "miejsce_start": 73,
                "miejsce_koniec": 89,
                "stacja_1": 78,
                "stacja_2": 79,
            }
        ],
        "761": [
            {
                "miejsce_start": 73,
                "miejsce_koniec": 89,
            }
        ],
    },
    "PS2_736": {
        "752": [
            {
                "miejsce_start": 90,
                "miejsce_koniec": 106,
                "stacja_1": 95,
                "stacja_2": 96,
            }
        ],
        "761": [
            {
                "miejsce_start": 90,
                "miejsce_koniec": 106,
            }
        ],
    },
    "PS2_737": {
        "752": [
            {
                "miejsce_start": 107,
                "miejsce_koniec": 126,
                "stacja_1": 112,
                "stacja_2": 113,
            }
        ],
        "761": [
            {
                "miejsce_start": 107,
                "miejsce_koniec": 126,
            }
        ],
    },
    "PS2_741": {
        "772": [
            {
                "miejsce_start": 3,
                "miejsce_koniec": 21,
                "stacja_1": 15,
                "stacja_2": 16,
            }
        ],
        "781": [
            {
                "miejsce_start": 2,
                "miejsce_koniec": 20,
            }
        ],
    },
    "PS2_742": {
        "772": [
            {
                "miejsce_start": 22,
                "miejsce_koniec": 38,
                "stacja_1": 32,
                "stacja_2": 33,
            }
        ],
        "781": [
            {
                "miejsce_start": 21,
                "miejsce_koniec": 37,
            }
        ],
    },
    "PS2_743": {
        "772": [
            {
                "miejsce_start": 39,
                "miejsce_koniec": 55,
                "stacja_1": 49,
                "stacja_2": 50,
            }
        ],
        "781": [
            {
                "miejsce_start": 38,
                "miejsce_koniec": 54,
            }
        ],
    },
    "PS2_744": {
        "772": [
            {
                "miejsce_start": 56,
                "miejsce_koniec": 72,
                "stacja_1": 66,
                "stacja_2": 67,
            }
        ],
        "781": [
            {
                "miejsce_start": 55,
                "miejsce_koniec": 71,
            }
        ],
    },
    "PS2_745": {
        "772": [
            {
                "miejsce_start": 73,
                "miejsce_koniec": 89,
                "stacja_1": 83,
                "stacja_2": 84,
            }
        ],
        "781": [
            {
                "miejsce_start": 72,
                "miejsce_koniec": 88,
            }
        ],
    },
    "PS2_746": {
        "772": [
            {
                "miejsce_start": 90,
                "miejsce_koniec": 106,
                "stacja_1": 100,
                "stacja_2": 101,
            }
        ],
        "781": [
            {
                "miejsce_start": 89,
                "miejsce_koniec": 105,
            }
        ],
    },
    "PS2_747": {
        "772": [
            {
                "miejsce_start": 107,
                "miejsce_koniec": 126,
                "stacja_1": 117,
                "stacja_2": 118,
            }
        ],
        "781": [
            {
                "miejsce_start": 106,
                "miejsce_koniec": 125,
            }
        ],
    },
    "PS2_751": {
        "702": [
            {
                "miejsce_start": 2,
                "miejsce_koniec": 20,
                "stacja_1": 10,
                "stacja_2": 11,
            }
        ],
        "711": [
            {
                "miejsce_start": 3,
                "miejsce_koniec": 21,
            }
        ],
    },
    "PS2_752": {
        "702": [
            {
                "miejsce_start": 21,
                "miejsce_koniec": 37,
                "stacja_1": 27,
                "stacja_2": 28,
            }
        ],
        "711": [
            {
                "miejsce_start": 22,
                "miejsce_koniec": 38,
            }
        ],
    },
    "PS2_753": {
        "702": [
            {
                "miejsce_start": 38,
                "miejsce_koniec": 54,
                "stacja_1": 44,
                "stacja_2": 45,
            }
        ],
        "711": [
            {
                "miejsce_start": 39,
                "miejsce_koniec": 55,
            }
        ],
    },
    "PS2_754": {
        "702": [
            {
                "miejsce_start": 55,
                "miejsce_koniec": 71,
                "stacja_1": 61,
                "stacja_2": 62,
            }
        ],
        "711": [
            {
                "miejsce_start": 56,
                "miejsce_koniec": 72,
            }
        ],
    },
    "PS2_755": {
        "702": [
            {
                "miejsce_start": 72,
                "miejsce_koniec": 88,
                "stacja_1": 78,
                "stacja_2": 79,
            }
        ],
        "711": [
            {
                "miejsce_start": 73,
                "miejsce_koniec": 89,
            }
        ],
    },
    "PS2_756": {
        "702": [
            {
                "miejsce_start": 89,
                "miejsce_koniec": 105,
                "stacja_1": 95,
                "stacja_2": 96,
            }
        ],
        "711": [
            {
                "miejsce_start": 90,
                "miejsce_koniec": 106,
            }
        ],
    },
    "PS2_757": {
        "702": [
            {
                "miejsce_start": 106,
                "miejsce_koniec": 125,
                "stacja_1": 112,
                "stacja_2": 113,
            }
        ],
        "711": [
            {
                "miejsce_start": 107,
                "miejsce_koniec": 126,
            }
        ],
    },
    "PS2_761": {
        "722": [
            {
                "miejsce_start": 3,
                "miejsce_koniec": 21,
                "stacja_1": 15,
                "stacja_2": 16,
            }
        ],
        "731": [
            {
                "miejsce_start": 3,
                "miejsce_koniec": 21,
            }
        ],
    },
    "PS2_762": {
        "722": [
            {
                "miejsce_start": 22,
                "miejsce_koniec": 38,
                "stacja_1": 32,
                "stacja_2": 33,
            }
        ],
        "731": [
            {
                "miejsce_start": 22,
                "miejsce_koniec": 38,
            }
        ],
    },
    "PS2_763": {
        "722": [
            {
                "miejsce_start": 39,
                "miejsce_koniec": 55,
                "stacja_1": 49,
                "stacja_2": 50,
            }
        ],
        "731": [
            {
                "miejsce_start": 39,
                "miejsce_koniec": 55,
            }
        ],
    },
    "PS2_764": {
        "722": [
            {
                "miejsce_start": 56,
                "miejsce_koniec": 72,
                "stacja_1": 66,
                "stacja_2": 67,
            }
        ],
        "731": [
            {
                "miejsce_start": 56,
                "miejsce_koniec": 72,
            }
        ],
    },
    "PS2_765": {
        "722": [
            {
                "miejsce_start": 73,
                "miejsce_koniec": 89,
                "stacja_1": 83,
                "stacja_2": 84,
            }
        ],
        "731": [
            {
                "miejsce_start": 73,
                "miejsce_koniec": 89,
            }
        ],
    },
    "PS2_766": {
        "722": [
            {
                "miejsce_start": 90,
                "miejsce_koniec": 106,
                "stacja_1": 100,
                "stacja_2": 101,
            }
        ],
        "731": [
            {
                "miejsce_start": 90,
                "miejsce_koniec": 106,
            }
        ],
    },
    "PS2_767": {
        "722": [
            {
                "miejsce_start": 107,
                "miejsce_koniec": 126,
                "stacja_1": 117,
                "stacja_2": 118,
            }
        ],
        "731": [
            {
                "miejsce_start": 107,
                "miejsce_koniec": 126,
            }
        ],
    },
    "PS2_771": {
        "752": [
            {
                "miejsce_start": 3,
                "miejsce_koniec": 21,
                "stacja_1": 10,
                "stacja_2": 11,
            }
        ],
        "761": [
            {
                "miejsce_start": 3,
                "miejsce_koniec": 21,
            }
        ],
    },
    "PS2_772": {
        "752": [
            {
                "miejsce_start": 22,
                "miejsce_koniec": 38,
                "stacja_1": 27,
                "stacja_2": 28,
            }
        ],
        "761": [
            {
                "miejsce_start": 22,
                "miejsce_koniec": 38,
            }
        ],
    },
    "PS2_773": {
        "752": [
            {
                "miejsce_start": 39,
                "miejsce_koniec": 55,
                "stacja_1": 44,
                "stacja_2": 45,
            }
        ],
        "761": [
            {
                "miejsce_start": 39,
                "miejsce_koniec": 55,
            }
        ],
    },
    "PS2_774": {
        "752": [
            {
                "miejsce_start": 56,
                "miejsce_koniec": 72,
                "stacja_1": 61,
                "stacja_2": 62,
            }
        ],
        "761": [
            {
                "miejsce_start": 56,
                "miejsce_koniec": 72,
            }
        ],
    },
    "PS2_775": {
        "752": [
            {
                "miejsce_start": 73,
                "miejsce_koniec": 89,
                "stacja_1": 78,
                "stacja_2": 79,
            }
        ],
        "761": [
            {
                "miejsce_start": 73,
                "miejsce_koniec": 89,
            }
        ],
    },
    "PS2_776": {
        "752": [
            {
                "miejsce_start": 90,
                "miejsce_koniec": 106,
                "stacja_1": 95,
                "stacja_2": 96,
            }
        ],
        "761": [
            {
                "miejsce_start": 90,
                "miejsce_koniec": 106,
            }
        ],
    },
    "PS2_777": {
        "752": [
            {
                "miejsce_start": 107,
                "miejsce_koniec": 126,
                "stacja_1": 112,
                "stacja_2": 113,
            }
        ],
        "761": [
            {
                "miejsce_start": 107,
                "miejsce_koniec": 126,
            }
        ],
    },
    "PS2_781": {
        "772": [
            {
                "miejsce_start": 3,
                "miejsce_koniec": 21,
                "stacja_1": 15,
                "stacja_2": 16,
            }
        ],
        "781": [
            {
                "miejsce_start": 2,
                "miejsce_koniec": 20,
            }
        ],
    },
    "PS2_782": {
        "772": [
            {
                "miejsce_start": 22,
                "miejsce_koniec": 38,
                "stacja_1": 32,
                "stacja_2": 33,
            }
        ],
        "781": [
            {
                "miejsce_start": 21,
                "miejsce_koniec": 37,
            }
        ],
    },
    "PS2_783": {
        "772": [
            {
                "miejsce_start": 39,
                "miejsce_koniec": 55,
                "stacja_1": 49,
                "stacja_2": 50,
            }
        ],
        "781": [
            {
                "miejsce_start": 38,
                "miejsce_koniec": 54,
            }
        ],
    },
    "PS2_784": {
        "772": [
            {
                "miejsce_start": 56,
                "miejsce_koniec": 72,
                "stacja_1": 66,
                "stacja_2": 67,
            }
        ],
        "781": [
            {
                "miejsce_start": 55,
                "miejsce_koniec": 71,
            }
        ],
    },
    "PS2_785": {
        "772": [
            {
                "miejsce_start": 73,
                "miejsce_koniec": 89,
                "stacja_1": 83,
                "stacja_2": 84,
            }
        ],
        "781": [
            {
                "miejsce_start": 72,
                "miejsce_koniec": 88,
            }
        ],
    },
    "PS2_786": {
        "772": [
            {
                "miejsce_start": 90,
                "miejsce_koniec": 106,
                "stacja_1": 100,
                "stacja_2": 101,
            }
        ],
        "781": [
            {
                "miejsce_start": 89,
                "miejsce_koniec": 105,
            }
        ],
    },
    "PS2_787": {
        "772": [
            {
                "miejsce_start": 107,
                "miejsce_koniec": 126,
                "stacja_1": 117,
                "stacja_2": 118,
            }
        ],
        "781": [
            {
                "miejsce_start": 106,
                "miejsce_koniec": 125,
            }
        ],
    },
}


selectedStation = None
oldTote = 0
volume_dict = dict()
rackTPA = list()
stationTPA = list()
lastStation = set()
stamp = 0
V_koszyka = 22815


Lstacja = "Stacja"
Loststacja = "Ostatnia stacja"
Lkoszyk = "Weź koszyk"
Lpowrot = "Powrót"
Lwyjdz = "Wyjdź"
Lwybierz_stacje = "Wybierz stację"
Lwyczysc = "Wyczyść"
Lzmien = "Zmień język"


def main():
    global root
    root = tk.Tk()
    root.bind("<Escape>", closeApp)
    root.bind("<F12>", back)
    root.title("AMD")
    root.attributes("-fullscreen", True)
    menuLayout()
    root.mainloop()

# layout okna do wyboru stacji


def menuLayout():
    global layoutStation, exitButton, titleLabel
    backgroundFrame = tk.Frame(
        root,
        background="#7f7f7f",
    )
    titleframe = tk.Frame(
        backgroundFrame,
        height=50,
        background="yellow",
    )
    layoutStation = tk.Frame(
        backgroundFrame,
        background="#b1b1b1",
    )
    exitButton = tk.Button(
        titleframe,
        text=Lwyjdz,
        command=exit,
        font=(None, 18),
    )
    titleLabel = tk.Label(
        titleframe,
        text=Lwybierz_stacje,
        font=(None, 20),
        fg="black",
        bg=titleframe.cget("background"),
    )
    PLlanguage = tk.Button(
        titleframe,
        text="PL",
        command=plLanguage,
        font=(None, 18),
        width=5,
    )
    UAlanguage = tk.Button(
        titleframe,
        text="UA",
        command=uaLanguage,
        font=(None, 18),
        width=5,
    )
    backgroundFrame.pack(fill="both", expand=True)
    titleframe.pack(fill="x", side="top", anchor="n")
    titleframe.grid_columnconfigure(0, weight=1)
    titleframe.grid_columnconfigure(2, weight=1)
    layoutStation.pack(fill="both", expand=True, padx=365, pady=130)
    titleLabel.grid(row=0, column=1)
    PLlanguage.grid(row=0, column=3, padx=5)
    UAlanguage.grid(row=0, column=4, padx=5)
    exitButton.grid(row=0, column=5)
    setButtonsInMenu()

# układanie przycisków z numerami stacji


def setButtonsInMenu():
    row = 0
    column = 0
    for index, stacja in enumerate(stacje):
        button = tk.Button(
            layoutStation,
            text=str(stacja),
            command=partial(selectStation, stacja),
            font=("Cambria", 12),
            height=3,
            width=11,
        )
        button.grid(row=row, column=column, padx=20, pady=20)
        row += 1
        if row in (7, 14, 21, 28, 35, 42, 49):
            column += 1
            row = 0


def selectStation(stacja):
    global selectedStation
    selectedStation = stacja
    stationLayout()

# czyszczenie pola z numerem kuwety


def wipeEntry():
    global barcode_entry
    barcode_entry.delete(0, tk.END)
    resetColors()


def closeApp(event=None):
    exit()


def back():
    global selectedStation, handle
    selectedStation = None
    for widget in root.winfo_children():
        widget.destroy()
    menuLayout()

# Zmiana na język PL


def plLanguage():
    global Lstacja, Loststacja, Lkoszyk, Lpowrot, Lwyjdz, Lwybierz_stacje, Lwyczysc, Lzmien
    Lstacja = "Stacja"
    Loststacja = "Ostatnia stacja"
    Lkoszyk = "Weź koszyk"
    Lpowrot = "Powrót"
    Lwyjdz = "Wyjdź"
    Lwybierz_stacje = "Wybierz stację"
    Lwyczysc = "Wyczyść"
    Lzmien = "Zmień język"
    try:
        exitButton.configure(text=Lwyjdz)
        if selectedStation == None:
            titleLabel.configure(text=Lwybierz_stacje)
        else:
            titleLabel.configure(text=f"{Lstacja} {selectedStation}")
        backButton.configure(text=Lpowrot)
        koszykLabel.configure(text=Lkoszyk)
        ost_stacja.configure(text=Loststacja)
        wipeButton.configure(text=Lwyczysc)
        stacja_marker.configure(text=Lstacja)
    except:
        Lstacja = "Stacja"
        Loststacja = "Ostatnia stacja"
        Lkoszyk = "Weź koszyk"
        Lpowrot = "Powrót"
        Lwyjdz = "Wyjdź"
        Lwybierz_stacje = "Wybierz stację"
        Lwyczysc = "Wyczyść"
        Lzmien = "Zmień język"

# Zmiana na język UA


def uaLanguage():
    global Lstacja, Loststacja, Lkoszyk, Lpowrot, Lwyjdz, Lwybierz_stacje, Lwyczysc, Lzmien
    Lstacja = "Станція"
    Loststacja = "Остання станція"
    Lkoszyk = "Візьміть кошик"
    Lpowrot = "Повернення"
    Lwyjdz = "Вийдіть"
    Lwybierz_stacje = "Виберіть станцію"
    Lwyczysc = "Вичистіть"
    Lzmien = "змінити мову"
    try:
        exitButton.configure(text=Lwyjdz)
        if selectedStation == None:
            titleLabel.configure(text=Lwybierz_stacje)
        else:
            titleLabel.configure(text=f"{Lstacja} {selectedStation}")
        backButton.configure(text=Lpowrot)
        koszykLabel.configure(text=Lkoszyk)
        ost_stacja.configure(text=Loststacja)
        wipeButton.configure(text=Lwyczysc)
        stacja_marker.configure(text=Lstacja)
    except:
        Lstacja = "Станція"
        Loststacja = "Остання станція"
        Lkoszyk = "Візьміть кошик"
        Lpowrot = "Повернення"
        Lwyjdz = "Вийдіть"
        Lwybierz_stacje = "Виберіть станцію"
        Lwyczysc = "Вичистіть"
        Lzmien = "змінити мову"

# Layout wybranej stacji


def stationLayout():
    global layoutStation, layoutRack, barcode_entry, ost_stacja, koszykLabel, exitButton, backButton, wipeButton, titleLabel

    for widget in root.winfo_children():
        widget.destroy()
    backgroundFrame = tk.Frame(
        background="#7f7f7f",
    )
    titleframe = tk.Frame(
        backgroundFrame,
        height=50,
        background="yellow",
    )
    layoutStation = tk.Frame(
        backgroundFrame,
        background="#b1b1b1",
    )
    layoutRack = tk.Frame(
        backgroundFrame,
        background="#b1b1b1",
    )
    exitButton = tk.Button(
        titleframe,
        text=Lwyjdz,
        command=closeApp,
        font=(None, 18),
    )
    backButton = tk.Button(
        titleframe,
        text=Lpowrot,
        command=back,
        font=(None, 18),
    )
    barcode_entry = tk.Entry(
        titleframe,
        font=(None, 20),
        width=12,
        fg="black",
    )
    wipeButton = tk.Button(
        titleframe,
        text=Lwyczysc,
        command=wipeEntry,
        font=(None, 18),
    )
    titleLabel = tk.Label(
        titleframe,
        text=f"{Lstacja} {selectedStation}",
        font=(None, 20),
        bg=titleframe.cget("background"),
        fg="black",
    )
    ost_stacja = tk.Label(
        layoutStation,
        text=Loststacja,
        font=("Arial", 24),
        bg="#9ffc6d",
        fg="black",
        height=2,
        width=13,
    )
    koszykLabel = tk.Label(
        layoutStation,
        text=Lkoszyk,
        font=("Arial", 24),
        bg="#fa6b6f",
        fg="black",
        height=2,
        width=13,
    )
    PLlanguage = tk.Button(
        titleframe,
        text="PL",
        command=plLanguage,
        font=(None, 18),
        width=5,
    )
    UAlanguage = tk.Button(
        titleframe,
        text="UA",
        command=uaLanguage,
        font=(None, 18),
        width=5,
    )
    backgroundFrame.pack(fill="both", expand=True)
    titleframe.pack(fill="x", side="top", anchor="n")
    titleframe.grid_columnconfigure(2, weight=1)
    titleframe.grid_columnconfigure(4, weight=1)
    barcode_entry.grid(row=0, column=0)
    wipeButton.grid(row=0, column=1, padx=10)
    titleLabel.grid(row=0, column=3)
    PLlanguage.grid(row=0, column=5, padx=5)
    UAlanguage.grid(row=0, column=6, padx=5)
    backButton.grid(row=0, column=7, padx=5)
    exitButton.grid(row=0, column=8)
    layoutStation.pack(fill="both", expand=True)
    layoutRack.pack(fill="both", expand=True)
    setStationLed()

# rozmieszczanie elementów dla wybranej stacji


def setStationLed():
    global selectedStation, layoutStation, layoutRack, stationLed, rackLed, stationLocation, stacja_marker
    rackList = list()
    stationLocation = list()
    stationPlaces = list()
    rackPlaces = list()

    font = ("Roboto", 30, "bold")
    kolor_led = "#abd6f8"

    for i in stacje:
        if i == selectedStation:
            for j in stacje[i]:
                rackList.append(j)
                try:
                    stationLocation.append(
                        stacje[selectedStation][j][0]["stacja_1"])
                    stationLocation.append(
                        stacje[selectedStation][j][0]["stacja_2"])

                except KeyError:
                    pass
            miejsce_start_first = min(
                {stacje[i][rackList[0]][0]["miejsce_start"]})
            miejsce_koniec_first = min(
                {stacje[i][rackList[0]][0]["miejsce_koniec"]})
            miejsce_start_second = min(
                {stacje[i][rackList[1]][0]["miejsce_start"]})
            miejsce_koniec_second = min(
                {stacje[i][rackList[1]][0]["miejsce_koniec"]})

            for miejsce in range(miejsce_start_first, miejsce_koniec_first + 1):
                stationPlaces.append(miejsce)
            for miejsce in range(miejsce_start_second, miejsce_koniec_second + 1):
                rackPlaces.append(miejsce)

    # layout miejsc z stacją w regale
    ile_mk = miejsce_koniec_first - miejsce_start_first
    if ile_mk <= 17:
        na_x = 80
        stacja_marker = tk.Label(
            layoutStation,
            text=Lstacja,
            font=(None, 22),
            height=2,
            width=12,
            bg="#ADECB1",
        )
        for i in stationPlaces:
            if i in stationLocation:
                stationLed = tk.Label(
                    layoutStation,
                    text=str(i),
                    font=(font),
                    height=2,
                    width=4,
                    bg=kolor_led,
                )
            else:
                stationLed = tk.Label(
                    layoutStation,
                    text=str(i),
                    font=(font),
                    height=3,
                    width=4,
                    bg=kolor_led,
                )
            if i in stationLocation:
                stationLed.place(x=na_x, y=265, anchor="n", relheight=0.18)
                stacja_marker.place(x=na_x - 55, y=445, anchor="s")
            else:
                stationLed.place(x=na_x, y=340, anchor="center")
            na_x += 110

        na_x = 80
        for i in rackPlaces:
            rackLed = tk.Label(
                layoutRack,
                text=str(i),
                font=(font),
                height=3,
                width=4,
                bg=kolor_led,
            )
            rackLed.place(x=na_x, y=180, anchor="center")
            na_x += 110

    elif ile_mk > 17:
        na_x = 65
        font = ("Roboto", 20, "bold")
        stacja_marker = tk.Label(
            layoutStation,
            text=Lstacja,
            font=(
                None,
                15,
            ),
            height=2,
            width=15,
            bg="#ADECB1",
        )
        for i in stationPlaces:
            if i in stationLocation:
                stationLed = tk.Label(
                    layoutStation,
                    text=str(i),
                    font=font,
                    height=3,
                    width=5,
                    bg=kolor_led,
                )
            else:
                stationLed = tk.Label(
                    layoutStation,
                    text=str(i),
                    font=font,
                    height=4,
                    width=5,
                    bg=kolor_led,
                )
            if i in stationLocation:
                stationLed.place(x=na_x, y=262, anchor="n")
                stacja_marker.place(x=na_x - 47, y=425, anchor="s")

            else:
                stationLed.place(x=na_x, y=330, anchor="center")
            na_x += 92

        # layout miejsc regalu bez stacji

        na_x = 65
        for i in rackPlaces:
            rackLed = tk.Label(
                layoutRack,
                text=str(i),
                font=font,
                height=4,
                width=5,
                bg=kolor_led,
            )
            rackLed.place(x=na_x, y=180, anchor="center")
            na_x += 93
    barcode_entry.focus_set()
    refresh()


def select_all():
    global barcode_entry
    try:
        barcode_entry.select_range(0, "end")
    except tk.TclError:
        pass

# Odświeżanie całej pętli


def refresh():
    global layoutStation, layoutRack, handle, rackLed, stationLed, barcode_entry, oldTote
    if selectedStation != None:
        actTote = barcode_entry.get()
        if actTote != "":
            query()
            oldTote = actTote
        root.after(700, lambda: [refresh(), select_all()])

# główna kwerenda pobieranie miejsc komisji


def query():
    global barcode_entry, selectedStation, stationTPA, rackTPA, lastStation, c1, koszyczek
    koszyczek = False
    rackTPA.clear()
    stationTPA.clear()
    lastStation.clear()
    volume_dict.clear()
    tote = barcode_entry.get()
    wynik = re.match("((^9411)([0-9]{8}))", tote)
    if wynik is not None:
        if len(tote) == 12:
            tote = tote[2:-1]
        elif len(tote) > 12:
            barcode_entry.delete(0, tk.END)
        sql = "select trim(tpfa10), \
                    tpvreg, \
                    tpvhor, \
                    tpiden,\
                    tpbmen\
                    from rcedatv5.pbesttp \
                    where tpbenr = ? \
                    and tpvort='AMD' \
                    and tpnsst=320\
                    and tpkstd=0\
                    and tpfirm=101\
                    and tpkonz=100"
        connection_status = pyodbc.connect(
            driver="{iSeries Access ODBC Driver}",
            system="192.168.172.10",
            uid="skl3",
            pwd="skl3",
        )
        c1 = connection_status.cursor()
        c1.execute(sql, tote)
        data = c1.fetchall()
        for x in stacje[selectedStation]:
            try:
                if stacje[selectedStation][x][0]["stacja_1"]:
                    stationRack = x
            except KeyError:
                pass
        for i in data:
            lastStation.add(i[0])
            if i[0] == selectedStation:
                art = int(i[3])
                pcs = int(i[4])
                volume_dict[art] = pcs
                if int(i[1]) == int(stationRack):
                    stationTPA.append(str(i[2]))
                else:
                    rackTPA.append(str(i[2]))

# dodawanie do okna znaczników koszyka i ostatniej stacji

    if len(rackTPA) != 0 or len(stationTPA) != 0:
        koszyczek = get_volume()
        if koszyczek == True:
            layoutStation.grid_columnconfigure(0, weight=1)
            layoutStation.grid_columnconfigure(3, weight=1)
            koszykLabel.grid(row=0, column=2)
        else:
            koszykLabel.grid_forget()
        configTpaLed()
    elif len(rackTPA) == 0 and len(stationTPA) == 0:
        for widget in layoutStation.winfo_children():
            if (
                widget.cget("text") != Lstacja
                and widget.cget("text") != Loststacja
                and widget.cget("text") != Lkoszyk
            ):
                widget.configure(bg="#abd6f8")
            for widget in layoutRack.winfo_children():
                if (
                    widget.cget("text") != Lstacja
                    and widget.cget("text") != Loststacja
                    and widget.cget("text") != Lkoszyk
                ):
                    widget.configure(bg="#abd6f8")


# zmiana koloru kafelków z pozycjami do pobrania

def configTpaLed():
    global stationTPA, rackTPA, ost_mk, stamp, layoutStation, layoutRack, stationLed, rackLed, stationLocation

    polaczona_lista = stationTPA + rackTPA
    maxstation = int(max(stationLocation))
    stamp += 1
    ost_mk = 0
    if len(polaczona_lista) > 2:
        ost_mk = int(
            *{max(polaczona_lista, key=lambda x: abs(int(x) - maxstation))})

    for widget in layoutStation.winfo_children():
        if widget.winfo_class() == "Label":
            if str(widget.cget("text")) in stationTPA:
                if widget.cget("text") == str(ost_mk):
                    widget.configure(bg="#faff33")
                    if widget.cget("bg") == "#faff33" and stamp % 2 == 0:
                        widget.configure(bg="#eb4343")
                else:
                    widget.configure(bg="#eb4343")
            elif (
                widget.cget("text") != Lstacja
                and widget.cget("text") != Loststacja
                and widget.cget("text") != Lkoszyk
            ):
                widget.configure(bg="#abd6f8")
    for widget in layoutRack.winfo_children():
        if widget.winfo_class() == "Label":
            if str(widget.cget("text")) in rackTPA:
                if str(widget.cget("text")) == str(ost_mk):
                    widget.configure(bg="#faff33")
                    if widget.cget("bg") == "#faff33" and stamp % 2 == 0:
                        widget.configure(bg="#eb4343")
                else:
                    widget.configure(bg="#eb4343")
            elif (
                widget.cget("text") != Lstacja
                and widget.cget("text") != Loststacja
                and widget.cget("text") != Lkoszyk
            ):
                widget.configure(bg="#abd6f8")
    if len(lastStation) == 1:
        blinkLastStation()
    else:
        ost_stacja.grid_forget()


def resetColors():
    for widget in layoutStation.winfo_children():
        if widget.winfo_class() == "Label":
            if (
                widget.cget("text") != Lstacja
                and widget.cget("text") != Loststacja
                and widget.cget("text") != Lkoszyk
            ):
                widget.configure(bg="#abd6f8")
    for widget in layoutRack.winfo_children():
        if widget.winfo_class() == "Label":
            if (
                widget.cget("text") != Lstacja
                and widget.cget("text") != Loststacja
                and widget.cget("text") != Lkoszyk
            ):
                widget.configure(bg="#abd6f8")


def blinkLastStation():
    if koszyczek == False:
        layoutStation.grid_columnconfigure(0, weight=1)
        layoutStation.grid_columnconfigure(2, weight=1)
        ost_stacja.grid(row=0, column=1)
    else:
        layoutStation.grid_columnconfigure(0, weight=1)
        layoutStation.grid_columnconfigure(2, weight=1)
        ost_stacja.grid(row=0, column=1)
    bg = ost_stacja.cget("background")
    fg = ost_stacja.cget("foreground")
    ost_stacja.configure(background=fg, foreground=bg)

# kwerenda pobierania objętości komisji


def get_volume():
    total_volume = 0
    sql = "select tzcm3 from rcedatv5.pbfstss where tziden=? and TZFIRM='101'"
    for keys, values in volume_dict.items():
        c1.execute(sql, keys)
        volume = c1.fetchone()
        volume = int(volume[0])
        szt = int(values)
        total_volume = total_volume + (volume * szt)
    if total_volume > (V_koszyka * 0.55):
        return True


if __name__ == "__main__":
    main()
