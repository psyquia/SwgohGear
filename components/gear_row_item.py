import tkinter as tk
from tkinter import ttk
import colorsys 

def rgb_to_hex(rgb):
    r, g, b = rgb
    return f'#{r:02x}{g:02x}{b:02x}'

class GearRowItem:

    def __init__(
           self, 
           parent, 
           id, 
           row_num, 
           icon, 
           name, 
           equipped, 
           unused, 
           total, 
           unused_map, 
           bdcolor, 
           font_size,
           unused_callback,
           acquired_callback,
           progress_callback
        ):
        self.equipped_val = tk.StringVar(parent,equipped)
        self.unused_val = tk.StringVar(parent,unused)
        self.acquired_val = tk.StringVar(parent,equipped+unused)
        self.total_val = tk.StringVar(parent,total)
        self.progress_val = tk.StringVar(parent,(equipped+unused)/total if total != 0 else 0)
        self.unused_callback = unused_callback
        self.acquired_callback = acquired_callback
        self.progress_callback = progress_callback

        self.key = id
        self.unused_map = unused_map

        self.border = tk.Frame(parent, 
           height=5, 
           width=1000, 
           bg='#454545'
        )
        self.border.grid(row=row_num*2, column=0, columnspan=7,padx=(25,80), pady=12)
        self.name_widget = tk.Label(parent,
            font=("TkDefaultFont ",10), 
            wraplength=135,
            width=16,
            bg='#212121', 
            fg='white',
            text=name
        )
        self.name_str = name
        self.name_widget.grid(row=(row_num*2)+1,column=1)
        
        self.icon = icon
        self.icon_widget = tk.Label(parent, 
            height=80, 
            width=80, 
            image=icon,
            bg=bdcolor
        )
        self.icon_widget.grid(row=(row_num*2)+1,column=0)
        
        self.equipped_widget = tk.Label(parent, 
            textvariable=self.equipped_val, 
            width=5, 
            font=("TkDefaultFont ",font_size), 
            bg='#212121', 
            fg='white'
        )
        self.equipped_widget.grid(row=(row_num*2)+1,column=2)

        self.progress_widget = tk.Label(parent, 
            textvariable=self.progress_val, 
            font=("TkDefaultFont ",font_size), 
            bg='#212121', 
            fg='white'
        )
        self.progress_widget.grid(row=(row_num*2)+1,column=6, padx=(0,100), sticky='')

        vcmd = (parent.register(self.callback),'%P', '%s')

        self.acquired_widget = tk.Label(parent, 
            textvariable=self.acquired_val, 
            width=5, 
            font=("TkDefaultFont ",font_size), 
            bg='#212121', 
            fg='white'
        )
        self.acquired_widget.grid(row=(row_num*2)+1,column=4)

        self.unused_widget = tk.Spinbox(parent, 
            textvariable=self.unused_val,
            validate="key",
            from_=0,
            to=999999,
            validatecommand=vcmd, 
            width=5,
            font=("TkDefaultFont ",font_size),
            bg='#212121', 
            fg='white'
        )
        self.unused_widget.grid(row=(row_num*2)+1,column=3)
        
        self.total_widget = tk.Label(parent, 
            textvariable=self.total_val, 
            width=5, 
            font=("TkDefaultFont ",font_size), 
            bg='#212121', 
            fg='white'
        )
        self.total_widget.grid(row=(row_num*2)+1,column=5)

    def callback(self, P, s):
        new_acquired_val = 0
        
        equipped = 0
        unused = 0
        equipped_valid = True
        unused_valid = True

        try:
            equipped = int(self.equipped_val.get())
            equipped_valid = True if equipped >= 0 else False
        except:
            equipped_valid = False

        try:
            unused = int(P)
            if unused >= 0:
                self.unused_map[self.key] = int(P)
                self.unused_callback(self.key, int(P))
                self.acquired_callback(self.key, int(P))
            else:
                unused_valid = False
        except Exception:
            unused_valid = False

        if equipped_valid:
            new_acquired_val += equipped
        if unused_valid:
            new_acquired_val += unused

        total = self.total_val.get() if self.total_val.get() != '0' else 0.0001
        progress = float(new_acquired_val)/float(total)
        self.progress_val.set(f'{int(progress*100)}%')
        self.progress_callback(self.key, progress)
        
        new_color = self.get_new_color(progress)
        self.progress_widget['fg'] = new_color
        self.acquired_val.set(new_acquired_val)
        return True

    def get_new_color(self, ratio):
        green = colorsys.rgb_to_hsv(0/255, 176/255, 32/255)
        red = colorsys.rgb_to_hsv(186/255, 0/255, 0/255)
        ratio = 1 if ratio > 1 else ratio

        ncolor = (red[0] + ratio*(green[0]-red[0]), red[1] + ratio*(green[1]-red[1]), red[2] + ratio*(green[2]-red[2]))
        n_rgb = colorsys.hsv_to_rgb(ncolor[0], ncolor[1], ncolor[2])
        res = rgb_to_hex((int(n_rgb[0]*255), int(n_rgb[1]*255), int(n_rgb[2]*255)))
        return res

    def hide(self):
        self.name_widget.grid_remove()
        self.icon_widget.grid_remove()
        self.equipped_widget.grid_remove()
        self.acquired_widget.grid_remove()
        self.unused_widget.grid_remove()
        self.total_widget.grid_remove()
        self.progress_widget.grid_remove()
        self.border.grid_remove()

    def show(self):
        self.name_widget.grid()
        self.icon_widget.grid()
        self.equipped_widget.grid()
        self.acquired_widget.grid()
        self.unused_widget.grid()
        self.total_widget.grid()
        self.progress_widget.grid()
        self.border.grid()