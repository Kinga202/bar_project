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


# ================== Zakładka 2: Klienci ===================
tab2 = Frame(notebook)
notebook.add(tab2, text='Klienci')
clients, client_markers = [], {}

f2_l, f2_f, f2_d, f2_m = Frame(tab2), Frame(tab2), Frame(tab2), Frame(tab2)
f2_l.grid(row=0, column=0), f2_f.grid(row=0, column=1)
f2_d.grid(row=1, column=0, columnspan=2), f2_m.grid(row=2, column=0, columnspan=2)

listbox_clients = Listbox(f2_l, width=50)
listbox_clients.pack()

Label(f2_f, text='Bar').grid(row=0, column=0)
entry_cb = Entry(f2_f); entry_cb.grid(row=0, column=1)
Label(f2_f, text='Miasto').grid(row=1, column=0)
entry_cl = Entry(f2_f); entry_cl.grid(row=1, column=1)
Label(f2_f, text='Imię').grid(row=2, column=0)
entry_cf = Entry(f2_f); entry_cf.grid(row=2, column=1)
Label(f2_f, text='Nazwisko').grid(row=3, column=0)
entry_cn = Entry(f2_f); entry_cn.grid(row=3, column=1)
Label(f2_f, text='Wizyty').grid(row=4, column=0)
entry_cv = Entry(f2_f); entry_cv.grid(row=4, column=1)

map2 = tkintermapview.TkinterMapView(f2_m, width=1200, height=400)
map2.pack()
map2.set_position(52.23, 21.00)
map2.set_zoom(6)

Label(f2_d, text='Bar:').grid(row=0, column=0)
label_cb = Label(f2_d, text='---'); label_cb.grid(row=0, column=1)
Label(f2_d, text='Miasto:').grid(row=0, column=2)
label_cl = Label(f2_d, text='---'); label_cl.grid(row=0, column=3)
Label(f2_d, text='Imię:').grid(row=0, column=4)
label_cf = Label(f2_d, text='---'); label_cf.grid(row=0, column=5)
Label(f2_d, text='Nazwisko:').grid(row=0, column=6)
label_cn = Label(f2_d, text='---'); label_cn.grid(row=0, column=7)
Label(f2_d, text='Wizyty:').grid(row=0, column=8)
label_cv = Label(f2_d, text='---'); label_cv.grid(row=0, column=9)

def add_client():
    c = {
        'bar': entry_cb.get(), 'loc': entry_cl.get(),
        'fname': entry_cf.get(), 'lname': entry_cn.get(),
        'visits': entry_cv.get(), 'coords': get_coords(entry_cl.get())
    }
    clients.append(c)
    key = (c['bar'], c['loc'])
    text = f"{c['bar']}\n" + "\n".join(f"{x['fname']} {x['lname']}" for x in clients if (x['bar'], x['loc']) == key)
    if key in client_markers: client_markers[key].delete()
    client_markers[key] = map2.set_marker(*c['coords'], text=text)
    listbox_clients.insert(END, f"{c['fname']} {c['lname']}")

    entry_cb.delete(0, END)
    entry_cl.delete(0, END)
    entry_cf.delete(0, END)
    entry_cn.delete(0, END)
    entry_cv.delete(0, END)

def show_client():
    i = listbox_clients.curselection()
    if i:
        c = clients[i[0]]
        label_cb.config(text=c['bar'])
        label_cl.config(text=c['loc'])
        label_cf.config(text=c['fname'])
        label_cn.config(text=c['lname'])
        label_cv.config(text=c['visits'])
        map2.set_position(*c['coords'])
        map2.set_zoom(15)

def remove_client():
    i = listbox_clients.curselection()
    if i:
        c = clients.pop(i[0])
        key = (c['bar'], c['loc'])
        if key in client_markers:
            client_markers[key].delete()
            del client_markers[key]
        listbox_clients.delete(i)

def edit_client():
    i = listbox_clients.curselection()
    if i:
        c = clients[i[0]]
        entry_cb.delete(0, END); entry_cb.insert(0, c['bar'])
        entry_cl.delete(0, END); entry_cl.insert(0, c['loc'])
        entry_cf.delete(0, END); entry_cf.insert(0, c['fname'])
        entry_cn.delete(0, END); entry_cn.insert(0, c['lname'])
        entry_cv.delete(0, END); entry_cv.insert(0, c['visits'])
        def update():
            c['bar'] = entry_cb.get()
            c['loc'] = entry_cl.get()
            c['fname'] = entry_cf.get()
            c['lname'] = entry_cn.get()
            c['visits'] = entry_cv.get()
            c['coords'] = get_coords(c['loc'])
            key = (c['bar'], c['loc'])
            if key in client_markers: client_markers[key].delete()
            text = f"{c['bar']}\n" + "\n".join(f"{x['fname']} {x['lname']}" for x in clients if (x['bar'], x['loc']) == key)
            client_markers[key] = map2.set_marker(*c['coords'], text=text)
            listbox_clients.delete(i); listbox_clients.insert(i, f"{c['fname']} {c['lname']}")
            btn_client_add.config(text="Dodaj", command=add_client)
        btn_client_add.config(text="Zapisz", command=update)

btn_client_add = Button(f2_f, text='Dodaj', command=add_client)
btn_client_add.grid(row=5, column=0, columnspan=2)
Button(f2_l, text='Szczegóły', command=show_client).pack()
Button(f2_l, text='Edytuj', command=edit_client).pack()
Button(f2_l, text='Usuń', command=lambda: remove_client()).pack()


root.mainloop()
