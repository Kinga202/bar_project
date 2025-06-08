from tkinter import *
from tkinter import ttk, messagebox
import tkintermapview
import requests
from bs4 import BeautifulSoup

root = Tk()
root.title("Zarządzanie Barami")
root.geometry("1300x750")
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

def get_coords(location):
    try:
        adres_url = f'https://pl.wikipedia.org/wiki/{location}'
        response_html = BeautifulSoup(requests.get(adres_url).text, 'html.parser')
        lat = float(response_html.select('.latitude')[1].text.replace(',', '.'))
        lon = float(response_html.select('.longitude')[1].text.replace(',', '.'))
        return [lat, lon]
    except:
        return [52.23, 21.00]

# ================== Zakładka 1: Bary ===================
tab1 = Frame(notebook)
notebook.add(tab1, text='Bary')
bars, bar_markers = [], []

frame1_l, frame1_f, frame1_d, frame1_m = Frame(tab1), Frame(tab1), Frame(tab1), Frame(tab1)
frame1_l.grid(row=0, column=0), frame1_f.grid(row=0, column=1)
frame1_d.grid(row=1, column=0, columnspan=2), frame1_m.grid(row=2, column=0, columnspan=2)

listbox_bars = Listbox(frame1_l, width=50)
listbox_bars.pack()

Label(frame1_f, text="Nazwa baru").grid(row=0, column=0)
entry_b_name = Entry(frame1_f)
entry_b_name.grid(row=0, column=1)
Label(frame1_f, text="Miejscowość").grid(row=1, column=0)
entry_b_loc = Entry(frame1_f)
entry_b_loc.grid(row=1, column=1)
Label(frame1_f, text="Ocena (1-5)").grid(row=2, column=0)
entry_b_rating = Entry(frame1_f)
entry_b_rating.grid(row=2, column=1)

map1 = tkintermapview.TkinterMapView(frame1_m, width=1200, height=400)
map1.pack()
map1.set_position(52.23, 21.00)
map1.set_zoom(6)

Label(frame1_d, text='Nazwa:').grid(row=0, column=0)
label_b_n = Label(frame1_d, text='---')
label_b_n.grid(row=0, column=1)
Label(frame1_d, text='Miejscowość:').grid(row=0, column=2)
label_b_l = Label(frame1_d, text='---')
label_b_l.grid(row=0, column=3)
Label(frame1_d, text='Ocena:').grid(row=0, column=4)
label_b_r = Label(frame1_d, text='---')
label_b_r.grid(row=0, column=5)

def get_coords(location):
    try:
        adres_url = f'https://pl.wikipedia.org/wiki/{location}'
        response_html = BeautifulSoup(requests.get(adres_url).text, 'html.parser')
        lat = float(response_html.select('.latitude')[1].text.replace(',', '.'))
        lon = float(response_html.select('.longitude')[1].text.replace(',', '.'))
        return [lat, lon]
    except:
        return [52.23, 21.00]

def add_bar():
    name, loc, rating = entry_b_name.get(), entry_b_loc.get(), entry_b_rating.get()
    try:
        rating = int(rating)
        if not (1 <= rating <= 5): raise ValueError
        coords = get_coords(loc)
        bar = {'name': name, 'loc': loc, 'rating': rating, 'coords': coords}
        bars.append(bar)
        marker = map1.set_marker(*coords, text=f"{name} ({rating}/5)")
        bar_markers.append(marker)
        listbox_bars.insert(END, name)
    except:
        messagebox.showwarning("Błąd", "Nieprawidłowe dane")

def show_bar():
    i = listbox_bars.curselection()
    if i:
        b = bars[i[0]]
        label_b_n.config(text=b['name'])
        label_b_l.config(text=b['loc'])
        label_b_r.config(text=b['rating'])
        map1.set_position(*b['coords'])
        map1.set_zoom(15)

def remove_bar():
    i = listbox_bars.curselection()
    if i:
        bar_markers[i[0]].delete()
        del bars[i[0]], bar_markers[i[0]]
        listbox_bars.delete(i)

def edit_bar():
    i = listbox_bars.curselection()
    if i:
        b = bars[i[0]]
        entry_b_name.delete(0, END); entry_b_name.insert(0, b['name'])
        entry_b_loc.delete(0, END); entry_b_loc.insert(0, b['loc'])
        entry_b_rating.delete(0, END); entry_b_rating.insert(0, b['rating'])
        def update():
            b['name'] = entry_b_name.get()
            b['loc'] = entry_b_loc.get()
            b['rating'] = int(entry_b_rating.get())
            b['coords'] = get_coords(b['loc'])
            bar_markers[i[0]].delete()
            bar_markers[i[0]] = map1.set_marker(*b['coords'], text=f"{b['name']} ({b['rating']}/5)")
            listbox_bars.delete(i); listbox_bars.insert(i, b['name'])
            btn_add.config(text="Dodaj", command=add_bar)
        btn_add.config(text="Zapisz", command=update)

btn_add = Button(frame1_f, text="Dodaj", command=add_bar)
btn_add.grid(row=3, column=0, columnspan=2)
Button(frame1_l, text="Szczegóły", command=show_bar).pack()
Button(frame1_l, text="Usuń", command=remove_bar).pack()
Button(frame1_l, text="Edytuj", command=edit_bar).pack()

root.mainloop()
