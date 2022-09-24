import random
from tkinter import *
import threading
import time


words =["off", "around", "only", "about", "sometimes", "to", "man", "book", "often", "still", "book", "young", "red", "there", "always", "talk", "take", "begin", "letter", "country", "night", "me", "if", "may", "plant", "were", "to", "every", "work", "that", "had", "country", "will", "you", "face", "without", "said", "on", "family", "miss", "day", "time", "go", "you", "father", "way", "I", "what", "other", "never", "this", "children", "can", "much", "both", "want", "for", "set", "use", "year", "song", "more", "my", "kind", "end", "both", "use", "large", "look", "just", "sea", "use", "found", "put", "may", "face", "eye", "car", "not", "could", "here", "list", "thought", "so", "water", "land", "by", "are", "both", "up", "about", "these", "second", "is", "father", "talk", "would", "took", "sea", "get", "here", "who", "father", "study", "some", "hard", "because", "own", "did", "last", "with", "high", "water", "follow", "show", "make", "world", "mile", "us", "face", "at", "use", "state", "learn", "began", "head", "miss", "play", "together", "where", "turn", "such", "who", "us", "talk", "up", "seem", "they", "leave", "no", "very", "there", "very", "far", "find", "sometimes", "leave", "thought", "any", "often", "sometimes", "two", "all", "have", "who", "night", "answer", "had", "sound", "home", "also", "us", "between", "mother", "world", "same", "which", "later", "white", "men", "she", "because", "tell", "feet", "said", "food", "face", "being", "side", "only"]


def check_score():
    global cpm
    cpm_label.config(text=f"CPM: {cpm}")
    wpm_label.config(text=f"WPM: {cpm / 5}")


def handler_5s():
    # run for 12x5=1 min
    for i in range(12):
        check_score()
        time.sleep(5)
    user_entry.config(state='disabled')


def try_again():
    global start_test, words
    user_entry.delete(0, END)
    user_entry.config(state='normal')
    reshuffle()
    init()
    start_test = False


def next_word():
    global tag_word, tag_char, word_index
    w_end = text.tag_nextrange(tag_word, '1.0')[1]
    w_len = len(words[word_index]) + 1
    # Delete all character tags for previous word
    for n in range(w_len):
        text.tag_delete(f'char{n}')
    word_index += 1
    w_len = len(words[word_index]) + 1
    w_start = f"{w_end} + 1c"
    w_end = f"{w_end} + {w_len}c"
    tag_word = f'word{word_index}'
    text.tag_add(tag_word, w_start, w_end)
    text.tag_config(tag_word, background="green", foreground="black")
    tag_char = 'char0'
    text.tag_add(tag_char, w_start)
    text.tag_config(tag_char, foreground="white")
    w_start = text.tag_nextrange(tag_word, '1.0')[0]
    text.see(f'{w_start} + 1lines')
    user_entry.delete(0, END)


def check_key(entry_char):
    global word_index, cpm, tag_word, tag_char, entry_word
    entry_index = user_entry.index(INSERT)
    entry_word = user_entry.get()
    # Remove leading spaces.
    if entry_word == ' ' or entry_word == '':
        user_entry.delete(0, END)
        return
    # 1st char missing, put it back.
    if entry_index == 0:
        user_entry.insert(0, entry_char)
    entry_word = entry_word.strip(' ')
    entry_index -= 1
    correct_word = words[word_index]
    correct_len = len(correct_word)
    # Check whole word
    if entry_char == ' ':
        # Remove word highlight.
        text.tag_config(tag_word, background="white")
        if entry_word == correct_word:
            cpm += correct_len
            text.tag_config(tag_word, foreground="green")
        else:
            text.tag_config(tag_word, foreground="red")
        next_word()
    else:
        # Get position of correct character,
        char_start = text.tag_nextrange(tag_char, '1.0')[0]
        if entry_index < correct_len:
            if correct_word[entry_index] == entry_word[entry_index]:
                text.tag_config(tag_char, foreground="black")
            else:
                text.tag_config(tag_char, foreground="red")
            # Move to next character
            tag_char = f"char{entry_index + 1}"
            char_start = f"{char_start} + 1c"
            text.tag_add(tag_char, char_start)
            text.tag_config(tag_char, foreground="white")
        # else:
        #     print(f'wrong: entry_{entry_word}_, correct_{correct_word}_, entry_index: {entry_index}')
    pos_label.config(text=f"POS: {word_index}.{entry_index}")


def click(key):
    global start_test, t_5s
    if not start_test:
        init()
        start_test = True
        pos_label.config(text=f"POS: 0.0")
        # Start 5 second thread.
        t_5s = threading.Thread(target=handler_5s)
        t_5s.start()
    check_key(key.char)
    return True


def init():
    global tag_word, tag_char, word_index, cpm, start_test
    word_index = 0
    cpm = 0
    tag_word = 'word0'
    tag_char = 'char0'
    for tag in text.tag_names():
        text.tag_delete(tag, '1.0', END)
    # Highlight first word and first character
    text.tag_add('tag_center', '1.0', END)
    text.tag_config('tag_center', justify=CENTER)
    text.tag_add(tag_word, "1.0", f"1.{len(words[0])}")
    text.tag_config(tag_word, background="green", foreground="black")
    text.tag_add(tag_char, '1.0')
    text.tag_config(tag_char, foreground="white")
    text.see('1.0')
    user_entry.delete(0, END)
    user_entry.config(state='normal')
    start_test = False


def reshuffle():
    global words
    # Setup database.Group of 5, so that .see() can scroll to different line
    text.config(state="normal")
    random.shuffle(words)
    for i in range(1, int(len(words)/5) + 1):
        text.delete(f'{i}.0', END)
    for i in range(len(words), -1, -5):
        line = ' '.join(words[i:i + 5]) + '\n'
        text.insert('1.0', line)
    text.config(state="disabled")


# Create the window
window = Tk()
window.title("Speed Test Software")
window.minsize(width=100, height=100)
window.config(padx=10, pady=10)
# Create labels
cpm_label = Label(text="CPM: 0", width=20)
cpm_label.grid(column=1, row=1)
wpm_label = Label(text="WPM: 0", width=20)
wpm_label.grid(column=2, row=1)
pos_label = Label(text="POS: 0", width=20)
pos_label.grid(column=3, row=1)
# Create text box to list the test words
text = Text(window, height=3, width=32, takefocus=False, font='Arial, 18', wrap=WORD)
text.grid(column=2, row=2, pady=5)
# Create user entry
user_entry = Entry(window, width=20, font='Arial, 18', justify='center', validate='key')
user_entry.grid(column=2, row=3, pady=5)
user_entry.focus()
# <KeyPress> is more reliable tha <KeyRelease>.
user_entry.bind('<KeyPress>', click)
# Create button
button = Button(window, text="Try Again", command=try_again)
button.grid(column=3, row=3, pady=10)

cpm = 0
word_index = 0
tar_word = ''
tar_char = ''
reshuffle()
init()

# Start 5 sec thread
t_5s = threading.Thread(target=handler_5s)
t_5s.start()
# Must put at the end
window.mainloop()





