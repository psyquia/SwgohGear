import tkinter as tk
from tkinter import ttk
from gear_main import Backend
from lib.scrollable import *
from PIL import Image, ImageTk
from components.gear_row_item import GearRowItem
import requests

HEIGHT = 600
WIDTH = 10

class MainWindow:
  border_color_map = {
    1: '#A5D0DA',
    2: '#98FD33',
    4: '#00BDFE',
    7: '#9241FF',
    9: '#9241FF',
    11: '#9241FF',
    12: '#FFCC33'
  }
    
  def __init__(self):
        self.running = True
        self.root = tk.Tk()
        self.backend = Backend()

        self.toon_id = self.backend.get_last_toon()
        self.player_id = self.backend.get_last_player()
        data = self.backend.get_display_gear_data(self.toon_id, self.player_id)
        self.equipped_gear = data['equipped_gear']
        self.total_gear = data['total_gear']
        self.gear_map = data['gear_map']
        self.unused_gear = data['unused_gear']
        self.acquired_gear = data['acquired_gear']
        self.progress_gear = data['progress_gear']
        self.toon_data = data['toon_data']
        self.name_2_baseid = data['toonname_2_baseid']
        self.names = self.name_2_baseid.keys()

        self.om_sv = tk.StringVar()
        self.toonname_sv = tk.StringVar(self.root, self.toon_data['name'])
        self.allycode_sv = tk.StringVar(self.root, self.player_id)
        self.gearquery_sv = tk.StringVar(self.root)
        
        self.toon_bar = tk.Frame(self.root, height=70, bg='black')
        self.toon_bar.pack(expand=True, fill='both', ipadx=100)
        self.setup_toon_bar(self.toon_bar)

        canvas = tk.Canvas(self.root, height=HEIGHT, width=WIDTH, bg='#212121')
        canvas.pack(expand=True, fill='both', anchor='center')

        frame = tk.Frame(canvas,width=WIDTH,height=HEIGHT)
        frame.pack(expand=True, fill='both', padx=(0,0))
        self.scrollable_frame = Scrollable(frame, '#212121', WIDTH, HEIGHT, 20)

        self.setup_gear_list('total', True);
        self.toon_bar.tkraise()

        self.root.mainloop()

        # cleanup
        self.gear_rows.clear()

        self.backend.save_data({
          'unused_gear': self.unused_gear,
          'ally_code'  : self.player_id,
          'toon_id'    : self.toon_id
        })
        self.running = False


  def setup_header(self, parent, font_size):
      hwidth = 15
      btn_color = '#363636'
      tk.Label(parent, 
          font=("TkDefaultFont ",font_size),
          bg='#212121',
          fg='white',
          text='icon',
          width=hwidth+3
      ).grid(row=0,column=0)

      tk.Label(parent, 
          font=("TkDefaultFont ",font_size), 
          bg='#212121', 
          fg='white',
          text='name',
          width=hwidth
      ).grid(row=0,column=1)
        
      self.equipped_header = tk.Button(parent, 
          command=self.sort_by_equipped, 
          bd=2,
          relief='groove',
          activebackground = MainWindow.active_btn_color,
          activeforeground = 'grey',
          font=("TkDefaultFont ",font_size), 
          bg=btn_color, 
          fg='white',
          text='equipped',
          width=hwidth
      )
      self.equipped_header.grid(row=0,column=2, padx=2.5)

      self.unused_header = tk.Button(parent, 
          command=self.sort_by_unused, 
          bd=2,
          activebackground = MainWindow.active_btn_color,
          activeforeground = 'grey',
          relief='groove',
          font=("TkDefaultFont ",font_size), 
          bg=btn_color, 
          fg='white',
          text='unused',
          width=hwidth
      )
      self.unused_header.grid(row=0,column=3, padx=2.5)
        
      self.acquired_header = tk.Button(parent, 
          command=self.sort_by_acquired, 
          bd=2,
          activebackground = MainWindow.active_btn_color,
          activeforeground = 'grey',
          relief='groove',
          font=("TkDefaultFont ",font_size), 
          bg=btn_color, 
          fg='white',
          text='total acquired',
          width=hwidth
      )
      self.acquired_header.grid(row=0,column=4, padx=2.5)

      self.total_header = tk.Button(parent, 
          command=self.sort_by_total, 
          bd=2,
          activebackground = MainWindow.active_btn_color,
          activeforeground = 'grey',
          relief='groove',
          font=("TkDefaultFont ",font_size), 
          bg=btn_color,
          fg='white',
          text='total required',
          width=hwidth
      )
      self.total_header.grid(row=0,column=5, padx=2.5)

      self.progress_header = tk.Button(parent, 
          command=self.sort_by_progress, 
          bd=2,
          activebackground = MainWindow.active_btn_color,
          activeforeground = 'grey',
          font=("TkDefaultFont ",font_size), 
          bg=btn_color, 
          fg='white',
          text='progress',
          relief='groove',
          width=hwidth-2,
      )
      self.progress_header.grid(row=0,column=6, padx=(2.5,100))

  def setup_toon_bar(self, toon_bar):
        im = Image.open(requests.get("https://www.swgoh.gg"+self.toon_data['image'], stream=True).raw)
        self.toon_icon = ImageTk.PhotoImage(im)

        self.icon_widget = tk.Label(toon_bar, 
            height=80, 
            width=80, 
            image=self.toon_icon,
        )
        self.icon_widget.grid(row=0,column=0, pady=8, padx=(120,50))

        tk.Label(toon_bar, 
          font=("TkDefaultFont ",12), 
          bg='black', 
          fg='white',
          text=self.toon_data['name']
        ).grid(row=0,column=1,pady=(18,0))

        self.om = tk.OptionMenu(
          toon_bar, 
          self.om_sv, 
          (),
        )
        self.om.config(bg = "#454545", fg='white', activebackground='#666666', borderwidth=0)
        self.om["menu"].configure(bg='#454545', fg='white')
        self.om.grid(row=0,column=4, padx=(5,5), pady=(20,0), sticky=tk.W,)

        tk.Button(toon_bar,
          activebackground='#1a1a1a',
          activeforeground='#474747',
          command=self.change_toon, 
          font=("TkDefaultFont ",10), 
          bg='#474747', 
          fg='#d9d9d9',
          text="CHECK GEAR"
        ).grid(row=0,column=5, padx=(30,20), pady=(20,0))

        self.ally_frame = tk.Frame(toon_bar,
          bg='black',
        )
        self.ally_frame.grid(row=0,column=2, columnspan=1, padx=(50,10))
        tk.Label(self.ally_frame, 
          font=("TkDefaultFont ",10), 
          bg='black', 
          fg='white',
          text='Ally Code'
        ).grid(row=0,column=0)
        tk.Entry(self.ally_frame, 
          textvariable=self.allycode_sv,
          font=("TkDefaultFont ",10), 
          bg='#212121', 
          width=10,
          fg='white',
        ).grid(row=1,column=0)

        self.toonname_frame = tk.Frame(toon_bar,
          bg='black',
        )
        self.toonname_frame.grid(row=0,column=3, padx=(10,10))
        tk.Label(self.toonname_frame, 
          font=("TkDefaultFont ",10), 
          bg='black', 
          fg='white',
          text='Character'
        ).grid(row=0,column=0)
        vcmd = (self.root.register(self.update_search_results),'%P')
        tk.Entry(self.toonname_frame, 
            validate="key",
            validatecommand=vcmd, 
            textvariable=self.toonname_sv,
            width=20,
            font=("TkDefaultFont ",10),
            bg='#212121', 
            fg='white'
        ).grid(row=1,column=0,padx=(20,0))
        self.root.bind('<Return>', self.change_toon)

        self.gearfilter_frame = tk.Frame(toon_bar,
            bg='#303030',
        )
        self.gearfilter_frame.grid(row=1,column=0, padx=20, pady=8, sticky='W')
        tk.Label(self.gearfilter_frame, 
          font=("TkDefaultFont ",11), 
          bg='#303030', 
          fg='#a6a6a6',
          text='Gear Filter: '
        ).grid(row=0,column=0, pady=4, padx=4, sticky='W')

        gcmd = (self.root.register(self.query_gear_results),'%P')
        tk.Entry(self.gearfilter_frame, 
            validate="key",
            validatecommand=gcmd, 
            textvariable=self.gearquery_sv,
            width=20,
            font=("TkDefaultFont ",10),
            bg='#212121', 
            fg='white'
        ).grid(row=0,column=1, padx=(0,4), sticky='W')

  def setup_gear_list(self, sort_by, reverse):
        self.gear_rows = []
        sort_list = []
        if sort_by == 'equipped':
          sort_list = self.equipped_gear.items()
        elif sort_by == 'acquired':
          sort_list = self.acquired_gear.items()
        elif sort_by == 'unused':
          sort_list = [gear for gear in self.unused_gear.items() if gear[0] in self.total_gear]
        elif sort_by == 'progress':
          sort_list = self.progress_gear.items()
        else:
          sort_list = self.total_gear.items()
        i = 1
        font_size = 12
        self.setup_header(self.scrollable_frame, font_size)
        for key,val in sorted(sort_list, key=lambda x : x[1], reverse=reverse):
            imtk = MainWindow.get_gear_icon(key)

            self.gear_rows.append(GearRowItem(
                self.scrollable_frame,
                key,
                i,
                imtk,
                self.gear_map[key]["name"],
                self.equipped_gear.get(key,0), 
                self.unused_gear.get(key,0), 
                self.total_gear.get(key,0), 
                self.unused_gear,
                MainWindow.border_color_map[self.gear_map[key]["tier"]],
                font_size,
                lambda key, val : self.unused_gear.update({key:val}),
                lambda key, val : self.acquired_gear.update({key: self.equipped_gear[key] + val}),
                lambda key, val : self.progress_gear.update({key: val})
            ))
            i+=1

        self.scrollable_frame.update()
        self.query_gear_results(self.gearquery_sv.get())

  def clear_gear_list(self):
      for child in self.scrollable_frame.winfo_children():
          child.destroy()
      self.gear_rows.clear()

  def clear_toon_bar(self):
      for child in self.toon_bar.winfo_children():
          child.destroy()
      self.setup_toon_bar(self.toon_bar)

  def set_option_menu(self, list):
      menu = self.om["menu"]
      menu.delete(0, "end")
      for name in list:
          menu.add_command(
            label=name, 
            command=lambda value=name:
            self.toonname_sv.set(value)
          )

  def update_search_results(self, P):
      query = P
      results = [name for name in self.names if query.lower() in name.lower()]
      self.set_option_menu(results)
      return True

  def query_gear_results(self, P):
      query = P
      for gear in self.gear_rows:
        if not query.lower() in gear.name_str.lower():
          gear.hide()
        else:
          gear.show()
      return True

  def change_toon(self, evt={}):
      self.backend.save_data({
        'unused_gear': self.unused_gear,
        'ally_code'  : self.player_id,
        'toon_id'    : self.toon_id
      })
      self.toon_id = self.name_2_baseid[self.toonname_sv.get()]
      try:
        self.player_id = int(self.allycode_sv.get())
      except:
        return False
      print(self.player_id, " ",self.toon_id)
      data = self.backend.get_display_gear_data(self.toon_id, self.player_id)
      if not data:
        return False
      self.equipped_gear = data['equipped_gear']
      self.total_gear = data['total_gear']
      self.gear_map = data['gear_map']
      self.unused_gear = data['unused_gear']
      self.acquired_gear = data['acquired_gear']
      self.toon_data = data['toon_data']
      self.clear_toon_bar()
      self.clear_gear_list()
      self.setup_toon_bar(self.toon_bar)
      self.setup_gear_list('total', True)
      return True

  def sort_by_equipped(self):
      try:
        MainWindow.sort_by_equipped.asc = not MainWindow.sort_by_equipped.asc
      except AttributeError:
        MainWindow.sort_by_equipped.asc = True
      self.clear_gear_list()
      self.setup_gear_list('equipped', MainWindow.sort_by_equipped.asc)
      self.equipped_header.configure(bg=  MainWindow.active_btn_color, fg='#ffffff') 

  def sort_by_acquired(self):
      try:
        MainWindow.sort_by_acquired.asc = not MainWindow.sort_by_acquired.asc
      except AttributeError:
        MainWindow.sort_by_acquired.asc = True
      self.clear_gear_list()
      self.setup_gear_list('acquired', MainWindow.sort_by_acquired.asc)
      self.acquired_header.configure(bg=  MainWindow.active_btn_color, fg='#ffffff') 

  def sort_by_total(self):
      try:
        MainWindow.sort_by_total.asc = not MainWindow.sort_by_total.asc
      except AttributeError:
        MainWindow.sort_by_total.asc = True
      self.clear_gear_list()
      self.setup_gear_list('total', MainWindow.sort_by_total.asc)
      self.total_header.configure(bg=  MainWindow.active_btn_color, fg='#ffffff') 

  def sort_by_unused(self):
      try:
        MainWindow.sort_by_unused.asc = not MainWindow.sort_by_unused.asc
      except AttributeError:
        MainWindow.sort_by_unused.asc = True
      self.clear_gear_list()
      self.setup_gear_list('unused', MainWindow.sort_by_unused.asc)
      self.unused_header.configure(bg=  MainWindow.active_btn_color, fg='#ffffff') 

  def sort_by_progress(self):
      try:
        MainWindow.sort_by_progress.asc = not MainWindow.sort_by_progress.asc
      except AttributeError:
        MainWindow.sort_by_progress.asc = True
      self.clear_gear_list()
      self.setup_gear_list('progress', MainWindow.sort_by_progress.asc)
      self.progress_header.configure(bg= MainWindow.active_btn_color, fg='#ffffff') 

  def get_gear_icon(id):
    try:
      im = Image.open(f"icon/{id}.jpg")
    except:
      im = Image.open(requests.get(f"https://www.swgoh.gg/game-asset/g/{id}.png", stream=True).raw)
      im = im.resize((80,80)).convert('RGB')
      im.save(f"icon/{id}.jpg")
    return ImageTk.PhotoImage(im)

  def is_running(self):
    return self.running

  active_btn_color = '#3f495c'
