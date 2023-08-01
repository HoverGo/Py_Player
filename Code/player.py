# Импортировать библиотеки
import os
from tkinter import *
from tkinter.ttk import *

from mutagen.wave import WAVE
from pygame import mixer
import time
from mutagen.mp3 import MP3

DEFAULT_PATH = "C:/Users/HoverGo/PycharmProjects/player"
print(DEFAULT_PATH)

# Создание окна
root = Tk()
root.title("Music Player")
root.geometry("750x600+290+85")
root.configure(background='#212121')
root.resizable(False, False)
mixer.init()

# Список путей для жанров
album_paths = {
    'blues': DEFAULT_PATH + '/images/blues.png',
    'classical': DEFAULT_PATH + '/images/classical.png',
    'country': DEFAULT_PATH + '/images/country.png',
    'disco': DEFAULT_PATH + '/images/disco.png',
    'hiphop': DEFAULT_PATH + '/images/hiphop.png',
    'jazz': DEFAULT_PATH + '/images/jazz.png',
    'metal': DEFAULT_PATH + '/images/metal.png',
    'pop': DEFAULT_PATH + '/images/pop.png',
    'reggae': DEFAULT_PATH + '/images/reggae.png',
    'rock': DEFAULT_PATH + '/images/rock.png'
}

font = ('Ubuntu', 10)
last_song = ''  # Последняя проигрываемая песня
paused = False  # Проверка стоит ли выбранная песня на паузе


def AddSongs(path):
    global songs
    if path:
        songs = os.listdir(path)
    for song in songs:
        if song.endswith(".wav"):
            Playlist.insert(END, song)


# Function to change album cover
def change_album_logo(curr_genre):
    Label(root, image=album_covers[curr_genre], background="#FFFFFF").place(x=45, y=140)


def time_update():
    # Display song position
    current_time = mixer.music.get_pos() / 1000
    # MM:SS format
    conv_time = time.strftime('%M:%S', time.gmtime(current_time))

    music_time = MP3(
        DEFAULT_PATH + "/Data/genres_original/" + Playlist.get(ACTIVE).split(".")[0] + "/" + Playlist.get(ACTIVE))

    song_pos.config(text=conv_time)
    # костыль, чтобы избежать 59:59
    if song_pos['text'] == '59:59':
        song_pos.config(text='00:00')
    # Обновление слайдера
    slider.config(to=music_time.info.length, value=current_time)

    song_pos.after(1000, time_update)


# Проигрывать музыку, когда кнопка нажата
def PlayMusic(is_paused, last_played):
    # Сохранить название последнего проигранного трека
    global last_song
    last_song = last_played
    # Получить название выбранного трека
    Music_Name = Playlist.get(ACTIVE)
    # Название жанра
    curr_genre = Music_Name.split(".")[0]
    # Если трек не выбран, то выбрать самый первый
    if Playlist.curselection() == ():
        Playlist.selection_set((0,), last=None)
    # Получить путь к выбранному треку
    Music_Name = DEFAULT_PATH + '/Data/genres_original/' + curr_genre + '/' + Music_Name
    # Если выбранный трек отличается от последнего проигрываемого, то необходимо его подгрузить и запустить
    if last_song != Music_Name:
        # Загрузить трек
        mixer.music.load(Music_Name)
        # Начать проигрывание
        mixer.music.play(loops=10)
        # Обновить имя последнего запущенного трека
        last_song = Music_Name
        # Изменить картинку кнопки на "пауза"
        ButtonPlay.configure(image=ButtonPause_Image)
    # Если выбранный трек тот же, что и последний проигрываемый, то запустить его
    else:
        global paused
        paused = is_paused
        # Если трек на паузе, то включаем его
        if paused:
            mixer.music.unpause()
            paused = False
            # Изменить картинку кнопки на "пауза"
            ButtonPlay.configure(image=ButtonPause_Image)
        # Иначе поставить на паузу
        else:
            mixer.music.pause()
            paused = True
            # Изменить картинку кнопки на "проигрывать"
            ButtonPlay.configure(image=ButtonPlay_Image)

    # Изменить логотип альбома
    change_album_logo(curr_genre)

    time_update()


# Запустить следующий трек
def PlayNext():
    global last_song, paused
    # Получить индекс выбранного трека
    next_song = Playlist.curselection()
    # Получить индекс следующего трека
    next_song = next_song[0] + 1
    # Получить имя следующего трека
    Music_Name = Playlist.get(next_song)
    # Название жанра
    curr_genre = Music_Name.split(".")[0]
    # Путь к треку
    Music_Name = DEFAULT_PATH + '/Data/genres_original/' + \
                 curr_genre + '/' + Music_Name
    # Загрузить и включить трек
    mixer.music.load(Music_Name)
    mixer.music.play()

    # Обновить название последнего проигрываемого трека
    last_song = Music_Name
    # Update the state of the song
    paused = False
    # Изменить картинку кнопки на "пауза"
    ButtonPlay.configure(image=ButtonPause_Image)

    # Switch selection to the next song
    Playlist.selection_clear(0, END)
    Playlist.activate(next_song)
    Playlist.selection_set(next_song, last=None)

    change_album_logo(curr_genre)


# Запустить предыдущий трек
def PlayPrev():
    global last_song, paused
    # Получить индекс выбранного трека
    prev_song = Playlist.curselection()
    # Получить индекс предыдущего трека
    prev_song = prev_song[0] - 1
    # Получить название предыдущего трека
    Music_Name = Playlist.get(prev_song)
    # Название жанра
    curr_genre = Music_Name.split(".")[0]
    # Путь к треку
    Music_Name = DEFAULT_PATH + '/Data/genres_original/' + \
                 curr_genre + '/' + Music_Name
    # Загрузить и запустить трек
    mixer.music.load(Music_Name)
    mixer.music.play()

    # Обновить название последнего проигрываемого трека
    last_song = Music_Name
    # Update the state of the song
    paused = False
    # Изменить картинку кнопки на "пауза"
    ButtonPlay.configure(image=ButtonPause_Image)

    # Switch selection to the previous song
    Playlist.selection_clear(0, END)
    Playlist.activate(prev_song)
    Playlist.selection_set(prev_song, last=None)

    change_album_logo(curr_genre)


# Изменить выбранный жанр
def ChangeGenre(event):
    # Получение названия жанра из бокса выбора
    global songs
    curr_genre = selected_genre.get()
    # Опустошить плейлист
    Playlist.delete(0, END)
    # append it to path
    path = DEFAULT_PATH + '/Data/genres_original/' + curr_genre
    # Открыть все файлы в выбранной папке
    if path:
        songs = os.listdir(path)

    for song in songs:
        if song.endswith(".mp3"):
            Playlist.insert(END, song)


image_path = '/home/liza/Study/pmldl/Project/images'
# Иконка
image_icon = PhotoImage(file=DEFAULT_PATH + "/images/icon3.png")
root.iconphoto(False, image_icon)

# Фоновая картинка
Background = PhotoImage(file=DEFAULT_PATH + "/images/top_image.png")
Label(root, image=Background, background="#0f1a2b").pack()

# Логотип
logo_img = PhotoImage(file=DEFAULT_PATH + "/images/logo.png")
Label(root, image=logo_img, background="#000000").place(x=45, y=140)

# Рамка для кнопок
Frame_buttons = Frame(root, relief=RIDGE, width=204)
Frame_buttons.pack()
Frame_buttons.place(x=45, y=370)

# Кнопки
ButtonPlay_Image = PhotoImage(file=DEFAULT_PATH + "/images/play.png")
ButtonPause_Image = PhotoImage(file=DEFAULT_PATH + "/images/pause.png")

ButtonPlay = Button(Frame_buttons, image=ButtonPlay_Image,
                    command=lambda: PlayMusic(paused, last_song))
ButtonPlay.grid(row=0, column=1, pady=5, padx=7)

ButtonPrev_Image = PhotoImage(file=DEFAULT_PATH + "/images/prev.png")
ButtonNext_Image = PhotoImage(file=DEFAULT_PATH + "/images/next.png")

ButtonPrev = Button(Frame_buttons, image=ButtonPrev_Image,
                    command=PlayPrev)
ButtonPrev.grid(row=0, column=0, pady=5, padx=3)

ButtonNext = Button(Frame_buttons, image=ButtonNext_Image,
                    command=PlayNext)
ButtonNext.grid(row=0, column=2, pady=5, padx=3)

# Слайдер
slider = Scale(root, from_=0, to=100, orient=HORIZONTAL, value=0, length=204)
slider.place(x=45, y=345)

# Время трека
song_pos = Label(Frame_buttons, text='00:00', font=font)
song_pos.grid(row=1, column=1)

Frame_Music = Frame(root, relief=RIDGE)
Frame_Music.place(x=330, y=350, width=180, height=250)

# Текст: выбор жанра
label_genre = Label(text='Select genre:', font=font)
label_genre.place(x=331, y=280)

# Список жанров
genres = ['blues', 'country', 'classical', 'disco', 'hiphop', 'jazz', 'metal', 'pop', 'reggae', 'rock']
selected_genre = StringVar(root)
# Бокс со списком жанров
genre_choice = Combobox(root, values=genres, textvariable=selected_genre)
genre_choice.place(x=330, y=300)
# prevent typing a value in the list
genre_choice['state'] = 'readonly'

# Запуск смены жанра
genre_choice.bind('<<ComboboxSelected>>', ChangeGenre)

# album dictionary genre: album-cover
album_covers = {genre: PhotoImage(file=album_paths[genre], width=200, height=200) for genre in genres}

Scroll = Scrollbar(Frame_Music)
Playlist = Listbox(Frame_Music, width=100, font=font, background="#333333", fg="grey", selectbackground="lightblue",
                   cursor="heart", bd=0, yscrollcommand=Scroll.set)
Scroll.config(command=Playlist.yview)
Scroll.pack(side=RIGHT, fill=Y)
Playlist.pack(side=LEFT, fill=BOTH)

# Запуск окна tkinter

root.mainloop()
