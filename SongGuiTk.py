import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
from tkinter import StringVar, END
from SongSqlite import PlaylistDbSqlite
import json

class PlaylistGuiTk(tk.Tk):

    def __init__(self, dataBase=PlaylistDbSqlite('PlaylistAppDb.db')):
        super().__init__()
        self.id_entryVar = StringVar()
        self.title_entryVar = StringVar()
        self.artist_entryVar = StringVar()
        self.album_entryVar = StringVar()
        self.rating_var = StringVar()
        self.db = dataBase

        self.title('Playlist Management System')
        self.geometry('1000x600') 
        self.config(bg='#FFB6C1') 
        self.resizable(False, False)

        self.font1 = ('Roboto', 20, 'bold')
        self.font2 = ('Roboto', 12, 'bold')

        imgsrc = 'image.png'
        img = Image.open(imgsrc)
        imgres = img.resize((1000, 600), Image.Resampling(3))
        imgtk = ImageTk.PhotoImage(imgres)

        self.logo = Label(self, image=imgtk, bd=0)
        self.logo.photo = imgtk
        self.logo.place(x=0, y=0)

        self.id_label = self.newCtkLabel('ID')
        self.id_label.place(x=80, y=350)
        self.id_entry = self.newCtkEntry(entryVariable=self.id_entryVar)
        self.id_entry.place(x=125, y=350)

        self.title_label = self.newCtkLabel('Title')
        self.title_label.place(x=80, y=390)
        self.title_entry = self.newCtkEntry(entryVariable=self.title_entryVar)
        self.title_entry.place(x=125, y=390)

        self.artist_label = self.newCtkLabel('Artist')
        self.artist_label.place(x=80, y=430)
        self.artist_entry = self.newCtkEntry(entryVariable=self.artist_entryVar)
        self.artist_entry.place(x=125, y=430)

        self.album_label = self.newCtkLabel('Album')
        self.album_label.place(x=80, y=470)
        self.album_entry = self.newCtkEntry(entryVariable=self.album_entryVar)
        self.album_entry.place(x=125, y=470)

        self.rating_label = self.newCtkLabel('Rating')
        self.rating_label.place(x=80, y=510)
        self.rating_entryVar = StringVar()
        self.rating_dropdown = ['S-Tier', 'A-Tier', 'C-Tier', 'F-Tier', 'Will not listen again']
        self.rating_entry = self.newCtkComboBox(options=self.rating_dropdown, entryVariable = self.rating_entryVar)
        self.rating_entry.place(x=125, y=510)

        self.add_button = self.newCtkButton(text='Add Song',
                                            onClickHandler=self.add_entry,
                                            fgColor='#05A312',
                                            hoverColor='#00850B',
                                            borderColor='#05A312')
        self.add_button.place(x=360, y=350)

        self.new_button = self.newCtkButton(text='New Song',
                                            onClickHandler=lambda: self.clear_form(True))
        self.new_button.place(x=360, y=400)
        
        self.update_button = self.newCtkButton(text='Update Song',
                                                onClickHandler=self.update_entry)
        self.update_button.place(x=360, y=450)

        self.delete_button = self.newCtkButton(text='Delete Song',
                                                onClickHandler=self.delete_entry,
                                                fgColor='#E40404',
                                                hoverColor='#AE0000',
                                                borderColor='#E40404')
        self.delete_button.place(x=560, y=350)

        self.export_button = self.newCtkButton(text='Export to CSV',
                                                onClickHandler=self.export_to_csv)
        self.export_button.place(x=560, y=400)

        self.import_csv_button = self.newCtkButton(text='Import from CSV',
                                                    onClickHandler=self.import_from_csv)
        self.import_csv_button.place(x=560, y=450)

        self.export_json_button = self.newCtkButton(text='Export to JSON',
                                                     onClickHandler=self.export_to_json)
        self.export_json_button.place(x=760, y=350)

        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure('Custom.Treeview',
                             font=self.font2,
                             foreground='#000', 
                             background='#FFFFE0',  
                             fieldbackground='#FFFFE0', 
                             bordercolor='#0C9295',  
                             highlightbackground='#FFC0CB',  
                             selectforeground='#FFF',  
                             selectbackground='#FF69B4')

        self.style.map('Custom.Treeview', background=[('selected', '#FF69B4')])

        self.tree = ttk.Treeview(self, height=15, style='Custom.Treeview')
        self.tree['columns'] = ('ID', 'Title', 'Artist', 'Album', 'Rating')
        self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('ID', anchor=tk.CENTER, width=50)
        self.tree.column('Title', anchor=tk.CENTER, width=150)
        self.tree.column('Artist', anchor=tk.CENTER, width=150)
        self.tree.column('Album', anchor=tk.CENTER, width=150)
        self.tree.column('Rating', anchor=tk.CENTER, width=100) 

        self.tree.heading('ID', text='ID')
        self.tree.heading('Title', text='Title')
        self.tree.heading('Artist', text='Artist')
        self.tree.heading('Album', text='Album')
        self.tree.heading('Rating', text='Rating')  

        self.tree.place(x=50, y=20, relwidth=0.9, height=300)
        self.tree.bind('<ButtonRelease>', self.read_display_data)

        self.add_to_treeview()

    def newCtkLabel(self, text='CTK Label'):
        widget_Font=self.font1
        widget_TextColor='#FFF'
        widget_BgColor='#161C25'

        widget = ttk.Label(self, text=text)
        return widget

    def newCtkEntry(self, text='CTK Label', entryVariable=None):
        widget_Font=self.font1
        widget_TextColor='#000'
        widget_FgColor='#FFF'
        widget_BorderColor='#0C9295'
        widget_BorderWidth=2
        widget_Width=25

        widget = ttk.Entry(self, textvariable=entryVariable, width=widget_Width)
        return widget

    def newCtkButton(self, text='CTK Button', onClickHandler=None, fgColor='#161C25', hoverColor='#FF5002', bgColor='#161C25', borderColor='#F15704'):
        widget_Font=self.font1
        widget_TextColor='#FFF'
        widget_FgColor=fgColor
        widget_HoverColor=hoverColor
        widget_BackgroundColor=bgColor
        widget_BorderColor=borderColor
        widget_BorderWidth=2
        widget_Cursor='hand2'
        widget_CornerRadius=15
        widget_Width=25
        widget_Function=onClickHandler

        widget = ttk.Button(self,
                            text=text,
                            command=widget_Function,
                            width=widget_Width)
        return widget
    
    def newCtkComboBox(self, options=['DEFAULT', 'OTHER'], entryVariable=None):
        widget_Font = self.font1
        widget_TextColor = '#000'
        widget_FgColor = '#FFF'
        widget_DropdownHoverColor = '#0C9295'
        widget_ButtonColor = '#0C9295'
        widget_ButtonHoverColor = '#0C9295'
        widget_BorderColor = '#0C9295'
        widget_BorderWidth = 2
        widget_Width = 25
        widget_Options = options

        widget = ttk.Combobox(self, textvariable=entryVariable, width=widget_Width)
        widget['values'] = options
        widget.set(options[0])

        return widget

    def add_to_treeview(self):
        songs = self.db.fetch_playlist()
        self.tree.delete(*self.tree.get_children())
        for song in songs:
            self.tree.insert('', END, values=song)

    def clear_form(self, *clicked):
        if clicked:
            self.tree.selection_remove(self.tree.focus())
            self.tree.focus('')
        self.id_entryVar.set('')
        self.title_entryVar.set('')
        self.artist_entryVar.set('')
        self.album_entryVar.set('')
        self.rating_entryVar.set('S-Tier')

    def read_display_data(self, event):
        selected_item = self.tree.focus()
        if selected_item:
            row = self.tree.item(selected_item)['values']
            self.clear_form()
            self.id_entryVar.set(row[0])
            self.title_entryVar.set(row[1])
            self.artist_entryVar.set(row[2])
            self.album_entryVar.set(row[3])
            self.rating_entryVar.set(row[4])

    def add_entry(self):
        id = self.id_entryVar.get()
        title = self.title_entryVar.get()
        artist = self.artist_entryVar.get()
        album = self.album_entryVar.get()
        rating = self.rating_entryVar.get()

        if not (id and title and artist and album):
            messagebox.showerror('Error', 'Enter all fields.')
        elif self.db.id_exists(id):
            messagebox.showerror('Error', 'ID already exists')
        else:
            self.db.insert_song(id, title, artist, album, rating)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Data has been inserted')

    def delete_entry(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Choose a song to delete')
        else:
            id = self.id_entryVar.get()
            self.db.delete_song(id)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Data has been deleted')

    def update_entry(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Choose a song to update')
        else:
            id=self.id_entryVar.get()
            title=self.title_entryVar.get()
            artist=self.artist_entryVar.get()
            album=self.album_entryVar.get()
            rating=self.rating_entryVar.get()
            self.db.update_song(title, artist, album, rating, id)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Data has been updated')

    def export_to_csv(self):
        self.db.export_csv()
        messagebox.showinfo('Success', f'Data exported to {self.db.dbName}.csv')

    def import_from_csv(self):
        self.db.import_csv()
        self.add_to_treeview()
        messagebox.showinfo('Success', f'Data imported from {self.db.dbName}.csv')

    def export_to_json(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])

        if file_path:
            entries_dict = {
                'Playlist': [
                    {'id': entry[0],
                    'title': entry[1],
                    'artist': entry[2],
                    'album': entry[3]}
                    for entry in self.db.fetch_playlist()
                ]
            }

            try:
                with open(file_path, 'w') as json_file:
                    json.dump(entries_dict, json_file, indent=4)
                messagebox.showinfo("Export Successful", f"Data exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Export Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    app = PlaylistGuiTk()
    app.mainloop()