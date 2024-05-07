#final copy
from tkinter import *
from tkinter import ttk
import tkinter as tk
import tkinter.font as tkFont
import sqlite3 
from tkinter import messagebox

window = Tk()
window.title("Art Gallery")
window.geometry("850x500")
window.configure(bg="#eed9c4")

def save():
    A_id = art_id.get()
    conn = sqlite3.connect('artdatacopy.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM Artwork_data WHERE ArtID=?''', (A_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        messagebox.showerror("Error", "Art ID already exists!")
        return
        
    Art_name = art_name.get()
    painter = artist_name.get()
    L = length.get()
    W = width.get()
    Style = style.get()
    Cost = cost.get()

    conn = sqlite3.connect('artdatacopy.db')
    cursor = conn.cursor()

    table_create = '''CREATE TABLE IF NOT EXISTS Artwork_data(ArtID INT PRIMARY KEY, ArtName TEXT, Artist TEXT, Length INT, Width INT, Style TEXT, Cost INT)'''
    cursor.execute(table_create)

    cursor.execute('''INSERT INTO Artwork_data (ArtID, ArtName, Artist, Length, Width, Style, Cost) VALUES (?, ?, ?, ?, ?, ?, ?)''',
                   (A_id, Art_name, painter, L, W, Style, Cost))
    #cursor.execute('''ALTER TABLE Artwork_data''')
    conn.commit()
    conn.close()

    #print("Art ID:", A_id)
    #print("Art name:", Art_name)
    #print("Artist:", painter)
    #print("Length:", L)
    #print("Width", W)
    #print("Style of art:", Style)
    #print("Cost:", Cost)

    clear_fields()

def update():
    def fetch_record():
        search_id = art_id1.get()

        conn = sqlite3.connect('artdatacopy.db')
        cursor = conn.cursor()

        cursor.execute('''SELECT * FROM Artwork_data WHERE ArtID=?''', (search_id,))
        search_result = cursor.fetchone()

        conn.close()

        if search_result:
            art_name.delete(0, tk.END)
            art_name.insert(0, search_result[1])
            artist_name.delete(0, tk.END)
            artist_name.insert(0, search_result[2])
            length.delete(0, tk.END)
            length.insert(0, search_result[3])
            width.delete(0, tk.END)
            width.insert(0, search_result[4])
            style.delete(0, tk.END)
            style.insert(0, search_result[5])
            cost.delete(0, tk.END)
            cost.insert(0, search_result[6])
        else:
            display_label.config(text="No record found with that Art ID.")

    def updaterecord():
        A_id = art_id1.get()
        Art_name = art_name.get()
        painter = artist_name.get()
        L = length.get()
        W = width.get()
        Style = style.get()
        Cost = cost.get()
    
        conn = sqlite3.connect("artdatacopy.db")
        cursor = conn.cursor()
    
        cursor.execute('''UPDATE Artwork_data SET ArtName=?, Artist=?, Length=?, Width=?, Style=?, Cost=? WHERE ArtID=?''',
                       (Art_name, painter, L, W, Style, Cost, A_id))
        conn.commit()
        conn.close()
        addroot.destroy()

    addroot = Toplevel(master=window)
    addroot.grab_set()
    addroot.geometry("470x500")
    addroot.title("Update record")
    addroot.config(bg="#eed9c4")
    
    Label(addroot, text="Update existing record", bg="#eed9c4", font=font_style, padx=20).pack(anchor="w")
    
    Label(addroot, text="Enter Art ID:", bg="#eed9c4", font=font_style, padx=20).pack(anchor="w")
    art_id1 = Entry(addroot, bg="#ADD8E6")
    art_id1.pack(anchor="w", padx=20)

    btn_fetch = Button(addroot, text="Fetch Record", bg="#ADD8E6", command=fetch_record)
    btn_fetch.pack(anchor="w", padx=20, pady= 10)

    Label(addroot, text="Updated Art Name:", bg="#eed9c4", font=font_style, padx=20).pack(anchor="w")
    art_name = Entry(addroot, bg="#ADD8E6")
    art_name.pack(anchor="w", padx=20)
    
    Label(addroot, text="Updated Artist Name:", bg="#eed9c4", font=font_style, padx=20).pack(anchor="w")
    artist_name = Entry(addroot, bg="#ADD8E6")
    artist_name.pack(anchor="w", padx=20)
    
    Label(addroot, text="Updated Length:", bg="#eed9c4", font=font_style, padx=20).pack(anchor="w")
    length = Entry(addroot, bg="#ADD8E6")
    length.pack(anchor="w", padx=20)
    
    Label(addroot, text="Updated Width:", bg="#eed9c4", font=font_style, padx=20).pack(anchor="w")
    width = Entry(addroot, bg="#ADD8E6")
    width.pack(anchor="w", padx=20)
    
    Label(addroot, text="Updated Style:", bg="#eed9c4", font=font_style, padx=20).pack(anchor="w")
    style = Entry(addroot, bg="#ADD8E6")
    style.pack(anchor="w", padx=20)
    
    Label(addroot, text="Updated Cost:", bg="#eed9c4", font=font_style, padx=20).pack(anchor="w")
    cost = Entry(addroot, bg="#ADD8E6")
    cost.pack(anchor="w", padx=20)
    
    btn = Button(addroot, text="Update", bg="#ADD8E6", command=updaterecord)
    btn.pack(side=LEFT, padx=20)

def search():
    def searchrecord():
        search_id = AID.get()
        search_name= AName.get()

        conn = sqlite3.connect('artdatacopy.db')
        cursor = conn.cursor()

        if not search_id and not search_name:  # If neither ID nor Name is provided
            display_label.config(text="Please enter Art ID or Art Name.")
        else:
            if search_id and search_name:  # If both ID and Name are provided
                cursor.execute('''SELECT * FROM Artwork_data WHERE ArtID=? AND ArtName=?''', (search_id, search_name))
            elif search_id:  # If only ID is provided
                cursor.execute('''SELECT * FROM Artwork_data WHERE ArtID=?''', (search_id,))
            elif search_name:  # If only Name is provided
                cursor.execute('''SELECT * FROM Artwork_data WHERE ArtName=?''', (search_name,))

            search_results = cursor.fetchall()

            if search_results:
                display_search_results(search_results)
            else:
                display_label.config(text="No results found.")

        conn.close()
        
        #addroot.destroy()

    addroot = Toplevel(master=window)
    addroot.grab_set()
    addroot.geometry("570x200")
    addroot.title("Search record")
    addroot.config(bg="#eed9c4")

    tk.Label(addroot, text="Search by Art ID or Art Name", bg="#eed9c4", font=font_style, padx=20).pack(anchor="w")

    tk.Label(addroot, text="Enter Art ID:", bg="#eed9c4", font=font_style, padx=20).pack(anchor="w")
    AID = tk.Entry(addroot, bg="#ADD8E6")
    AID.pack(anchor="w", padx=20)

    tk.Label(addroot, text="Enter Art Name:", bg="#eed9c4", font=font_style, padx=20).pack(anchor="w")
    AName = tk.Entry(addroot, bg="#ADD8E6")
    AName.pack(anchor="w", padx=20)

    display_label = tk.Label(addroot, text="", bg="#eed9c4", font=font_style)
    display_label.pack()

    btn = tk.Button(addroot, text="Search", bg="#ADD8E6", command=searchrecord)
    btn.pack(side=LEFT, padx=20)

def delete():
    def deleterecord():
        A_id = AID.get()
        A_name= AName.get()

        conn = sqlite3.connect('artdatacopy.db')
        cursor = conn.cursor()

        if A_id:
            cursor.execute('''DELETE FROM Artwork_data WHERE ArtID=?''', (A_id,))
        else:
            cursor.execute('''DELETE FROM Artwork_data WHERE ArtName=?''', (A_name,))
        
        popup=Toplevel(master=addroot)
        popup.grab_set()
        popup.geometry("100x100")
        popup.config(bg="#eed9c4")
        tk.Label(popup, text="Record successfully deleted", bg="#eed9c4", font=font_style, padx=20).pack(anchor="center")

        conn.commit()
        conn.close()
        
        addroot.destroy()
        
    addroot = Toplevel(master=window)
    addroot.grab_set()
    addroot.geometry("470x200")
    addroot.title("Delete record")
    addroot.config(bg="#eed9c4")

    tk.Label(addroot, text="Delete by Art ID or Art Name", bg="#eed9c4", font=font_style, padx=20).pack(anchor="w")

    tk.Label(addroot, text="Enter Art ID:", bg="#eed9c4", font=font_style, padx=20).pack(anchor="w")
    AID = tk.Entry(addroot, bg="#ADD8E6")
    AID.pack(anchor="w", padx=20)

    tk.Label(addroot, text="Enter Art Name:", bg="#eed9c4", font=font_style, padx=20).pack(anchor="w")
    AName = tk.Entry(addroot, bg="#ADD8E6")
    AName.pack(anchor="w", padx=20)

    btn = tk.Button(addroot, text="Delete", bg="#ADD8E6", command=deleterecord)
    btn.pack(side=LEFT, padx=20)

def clear_fields():
    art_id.delete(0, END)
    art_name.delete(0, END)
    artist_name.delete(0, END)
    length.delete(0, END)
    width.delete(0, END)
    style.delete(0, END)
    cost.delete(0, END)

def display_search_results(results):
    addroot= Toplevel(master=window)
    addroot.geometry("600x400")
    treeview = ttk.Treeview(addroot)
    treeview.pack()

    treeview["columns"] = ("ArtID", "ArtName", "Artist", "Length", "Width", "Style", "Cost")

    treeview.column("#0", width=0, stretch=NO)
    treeview.column("ArtID", anchor=E, width=70)
    treeview.column("ArtName", anchor=E, width=100)
    treeview.column("Artist", anchor=E, width=70)
    treeview.column("Length", anchor=E, width=70)
    treeview.column("Width", anchor=E, width=70)
    treeview.column("Style", anchor=E, width=70)
    treeview.column("Cost", anchor=E, width=70)

    treeview.heading("#0", text="", anchor=W)
    treeview.heading("ArtID", text="ArtID", anchor=W)
    treeview.heading("ArtName", text="Art Name", anchor=W)
    treeview.heading("Artist", text="Artist", anchor=W)
    treeview.heading("Length", text="Length", anchor=W)
    treeview.heading("Width", text="Width", anchor=W)
    treeview.heading("Style", text="Style", anchor=W)
    treeview.heading("Cost", text="Cost", anchor=W)

    for row in results:
        treeview.insert("", END, values=row)

def display():
    conn= sqlite3.connect('artdatacopy.db')
    cursor= conn.cursor()

    display_window= Toplevel(master=window)
    display_window.title("Display Data")
    display_window.geometry("700x400")

    treeview= ttk.Treeview(display_window)
    treeview.pack()

    treeview["columns"] = ("ArtID", "ArtName", "Artist", "Length", "Width", "Style", "Cost")

    cursor.execute("SELECT * from Artwork_data")
    data= cursor.fetchall()

    conn.commit()
    conn.close()

    for row in data:
        treeview.insert("", END, values=row)

    treeview.column("#0", width=0, stretch=NO)
    treeview.column("ArtID", anchor=E, width=70)
    treeview.column("ArtName", anchor=E, width=100)
    treeview.column("Artist", anchor=E, width=70)
    treeview.column("Length", anchor=E, width=70)
    treeview.column("Width", anchor=E, width=70)
    treeview.column("Style", anchor=E, width=70)
    treeview.column("Cost", anchor=E, width=70)

    treeview.heading("#0", text="", anchor=W)
    treeview.heading("ArtID", text="ArtID", anchor=W)
    treeview.heading("ArtName", text="Art Name", anchor=W)
    treeview.heading("Artist", text="Artist", anchor=W)
    treeview.heading("Length", text="Length", anchor=W)
    treeview.heading("Width", text="Width", anchor=W)
    treeview.heading("Style", text="Style", anchor=W)
    treeview.heading("Cost", text="Cost", anchor=W)

font_style = ("Rockwell", 16)
font_style1 = ("Rockwell", 20)

Label(window, text="Art Gallery Database", font=font_style1, bg="#ADD8E6").pack()

frame = Frame(window, bg="#eed9c4")
frame.pack(anchor="nw", pady=20)

btn = Button(frame, text="Save", bg="#ADD8E6", command=save)
btn.pack(side=LEFT, padx=20)

btn_update = Button(frame, text="Update", bg="#ADD8E6", command=update)
btn_update.pack(side=LEFT, padx=20)

btn_search = Button(frame, text="Search", bg="#ADD8E6", command=search)
btn_search.pack(side=LEFT, padx=20)

btn_delete = Button(frame, text="Delete", bg="#ADD8E6", command=delete)
btn_delete.pack(side=LEFT, padx=20)

btn_display= Button(frame, text="Display", bg="#ADD8E6", command=display)
btn_display.pack(side=LEFT, padx=20)

Label(window, text="Art ID:", bg="#eed9c4", font=font_style, padx=20).pack(anchor="w")
art_id = Entry(window, bg="#ADD8E6")
art_id.pack(anchor="w", padx=20)

Label(window, text="Art Name:", bg="#eed9c4", font=font_style, padx=20).pack(anchor="w")
art_name = Entry(window, bg="#ADD8E6")
art_name.pack(anchor="w", padx=20)

Label(window, text="Artist Name:", bg="#eed9c4", font=font_style, padx=20).pack(anchor="w")
artist_name = Entry(window, bg="#ADD8E6")
artist_name.pack(anchor="w", padx=20)

Label(window, text="Length:", bg="#eed9c4", font=font_style, padx=20).pack(anchor="w")
length = Entry(window, bg="#ADD8E6")
length.pack(anchor="w", padx=20)

Label(window, text="Width:", bg="#eed9c4", font=font_style, padx=20).pack(anchor="w")
width = Entry(window, bg="#ADD8E6")
width.pack(anchor="w", padx=20)

Label(window, text="Style:", bg="#eed9c4", font=font_style, padx=20).pack(anchor="w")
style = Entry(window, bg="#ADD8E6")
style.pack(anchor="w", padx=20)

Label(window, text="Cost of painting:", bg="#eed9c4", font=font_style, padx=20).pack(anchor="w")
cost = Entry(window, bg="#ADD8E6")
cost.pack(anchor="w", padx=20)

display_label = Label(window, text="", bg="#eed9c4", font=font_style)
display_label.pack()

window.mainloop()
