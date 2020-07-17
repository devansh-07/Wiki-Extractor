import wikipedia
import threading
import time
from tkinter import *
from tkinter import ttk
from tkinter.font import Font
from fpdf import FPDF

global pd, flag, cache

flag = 0
cache = {}

def look(event):
    rs = related.curselection()
    phr = related.get(rs)
    phrase.delete(0, END)
    phrase.insert(0, phr)
    start_thrd()
    related.delete(0, END)

def get_info(wrd):
    global flag
    rltd = []
    related.delete(0, END)
    if not wrd:
        msg = "\t   Enter something in searchbox!"
        flag = 0
    elif cache.get(wrd, None):
        msg = cache[wrd][0]
        rltd = cache[wrd][1]
        flag = 1
    else:
        try:
            global wts, wiki_ans
            msg = wikipedia.summary(wrd)
            rltd = wikipedia.search(wrd)
            cache[wrd] = (msg, rltd)
            flag = 1
        except:
            msg = "\tNo connection or No search results!"
            flag = 0
    return (msg, rltd)

def helper():
    global ans, rltd, word
    word = phrase.get().title()
    ans, rltd = get_info(word)
    ans = ans.replace(" ( (listen))", "")

def start_thrd(event=None):
    global thrd
    thrd = threading.Thread(target=helper)
    thrd.daemon = True
    thrd.start()
    thrd2 = threading.Thread(target=show_banner)
    thrd2.daemon = True
    thrd2.start()

def show_banner():
    i = 0
    pd = "\n\n\n\n\n\n\t\t"
    s = "Getting results"
    while thrd.is_alive():
        n = i%(len(s))
        bnr = pd + s[:n] + '->' + s[n+1:]
        answer.config(state='normal')
        answer.delete(1.0, END)
        answer.insert(INSERT, bnr)
        answer.config(state='disabled')
        time.sleep(0.1)
        i += 1
    insert_ans()

def insert_ans():
    answer.config(state='normal')
    answer.delete(1.0, END)
    answer.insert(INSERT, ans)
    answer.config(state='disabled')
    related.delete(0, END)
    for i, v in enumerate(rltd):
        related.insert(i, v)

def save_txt():
    if flag == 1:
        with open(f'{word.title()}_info.txt', 'w+') as f:
            f.write(ans)
        lbl = Label(root, text="Text file saved.", padx=15, pady=3, fg="#099c5c", bg="#043b23")
        lbl.place(rely=1.0, anchor="sw")
        lbl.after(4000, lbl.destroy)
    else:
        lbl = Label(root, text="Nothing to save.", padx=15, pady=3, fg="#de1814", bg="#360403")
        lbl.place(rely=1.0, anchor="sw")
        lbl.after(4000, lbl.destroy)

def get_pieces(s, ll=80):
    l = s.split()
    newl, h, ln = [], [], 0
    for i in range(len(l)):
        h.append(l[i])
        ln += (len(l[i]) + 1)
        if ln + len(l[min(i+1, len(l)-1)]) >= ll:
            newl.append(' '.join(h))
            h, ln = [], 0
    newl.append(' '.join(h))
    return newl

def save_pdf():
    if flag == 1:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', size=16)
        pdf.cell(190, 10, str(word.upper()), 1, 0, 'C')
        pdf.ln(20)
        pdf.set_font('Arial', size=13)
        l = get_pieces(str(ans), 87)
        for i in l:
            pdf.cell(0, 7, str(i.replace('\u2013', '')), 0, 1)
        pdf.output(str(word.title()) + '_info.pdf')

        lbl = Label(root, text="PDF file saved.", padx=15, pady=3, fg="#099c5c", bg="#043b23")
        lbl.place(rely=1.0, anchor="sw")
        lbl.after(4000, lbl.destroy)
    else:
        lbl = Label(root, text="Nothing to save.", padx=15, pady=3, fg="#de1814", bg="#360403")
        lbl.place(rely=1.0, anchor="sw")
        lbl.after(4000, lbl.destroy)

root = Tk()
root.resizable(width=False, height=False)
root.title("Wikipedia search")
root.configure(bg="#292929")
root.geometry("400x510+400+400")

ttk.Style().configure("TButton", background="black")
myfont = Font(family="Trebuchet MS", size=10)

frame1 = Frame(root, bg="#292929")
frame1.pack(padx=10, pady=(10, 0))

frame2 = Frame(root, bg="#292929")
frame2.pack(padx=6, pady=(5, 0))

entFr = Frame(frame2, bg="#292929")
entFr.pack(pady=(5, 5))

frame3 = Frame(root, bg="#292929")
frame3.pack(side=LEFT, padx=10, pady=(0, 20))

frame4 = Frame(root, bg="#292929")
frame4.pack(side=RIGHT, pady=(0, 20))

l = Label(root, text="- Dsoni01  ", pady=5, padx=5, fg="#7a7a7a", bg="#292929")
l.place(relx=1.0, rely=1.0, x=0, y=0, anchor="se")

phrase = Entry(frame1, width=33)
phrase.pack(side=LEFT, padx=5)
phrase.configure()

button = Button(frame1, text="Search", fg="#ffffff", bg="#001010", command=start_thrd)
button.pack(side=LEFT, padx=5, pady=5)
root.bind('<Return>', start_thrd)

scrollbar = ttk.Scrollbar(entFr)
scrollbar.pack(side = RIGHT, fill=Y)

answer = Text(entFr, width=43, height=14, yscrollcommand=scrollbar.set, wrap=WORD, bd=0, background="lightgrey")
answer.pack(pady=0)
answer.configure(font=myfont, state='disabled')
scrollbar.config(command=answer.yview)

label1 = Label(frame2, text="Related :", bg="#292929", fg="lightgrey")
label1.pack(side=TOP, padx=0)

related = Listbox(frame2, width=45, height=5)
related.pack(pady=(5, 0))
related.bind('<<ListboxSelect>>', look)

label1 = Label(frame3, text="Save as :", bg="#292929", fg="lightgrey")
label1.pack(side=LEFT, padx=0)

button2 = Button(frame3, text="Text file", fg="#ffffff", bg="#001010", width=5, command=save_txt)
button2.pack(side=LEFT, padx=(5, 0))

button3 = Button(frame3, text="PDF file", fg="#ffffff", bg="#001010", width=5, command=save_pdf)
button3.pack(side=LEFT, padx=(10, 0))

quit_bt = Button(frame4, text="Quit", fg="#ffffff", bg="#001010", width=5, command=root.destroy)
quit_bt.pack(side=RIGHT, padx=15)

root.mainloop()
