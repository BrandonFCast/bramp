import customtkinter as ctk
import os
import vlc

class Window:
    def __init__(self):
        self.current_index = 0
        self.current_playlist = None
        self.current_player = None

        self.app = ctk.CTk()
        self.app.title("Bramp")
        self.app.overrideredirect(True)
        self.app.bind("<Button-3>", lambda e: self.app.destroy())
        self.init_gui()

        self.load_playlist(self.get_all_songs_list())
    
    def show(self):
        self.app.mainloop()
    
    def get_all_songs_list(self):
        path = "./music"
        files = os.listdir(path)
        return files

    def load_playlist (self, list):
        self.current_playlist = list

        for c in self.current_playlist_frame.winfo_children():
            c.destroy()

        for name in list:
            lbl = ctk.CTkLabel(self.current_playlist_frame, text=name)
            lbl.grid(sticky="w")
            lbl.bind("<Button-1>", lambda e, song=name: self.play_song('./music/' + song))
    
    def play_song(self, path):
        if hasattr(self, 'current_player') and not self.current_player == None:
            self.current_player.stop()
        player = vlc.MediaPlayer(path)
        player.play()
        self.current_player = player

    def next_song(self):
        pass

    def seek_backward(self):
        self.current_player.set_time(max(self.current_player.get_time() - 5000, 0))
    
    def seek_forward(self):
        self.current_player.set_time(self.current_player.get_time() + 5000)
    
    def pause(self):
        self.current_player.pause()

    def init_gui(self):
        # region label
        lbl = ctk.CTkLabel(self.app, text="nombre de cancion")
        lbl.grid(row=0, column=0, columnspan=5, sticky="we")
        lbl.bind("<ButtonPress-1>", self.start_move)
        lbl.bind("<ButtonRelease-1>", self.stop_move)
        lbl.bind("<B1-Motion>", self.move)
        self.lbl = lbl
        # endregion

        # region buttons
        buttons = [
                ("<<", self.next_song, "e"),
                ("<", self.seek_backward, ""),
                ("||", self.pause, "nsew"),
                (">", self.seek_forward, ""),
                (">>", self.next_song, "w")
            ]

        for i, (txt, method, pos) in enumerate(buttons):
            btn = ctk.CTkButton(self.app, text=txt, width=30, command=method)
            btn.grid(row=2, column=i, ipadx=0, columnspan=1, sticky=pos)
        # endregion

        # region current playlist frame
        curret_playlist_frame = ctk.CTkScrollableFrame(self.app)
        curret_playlist_frame.grid(row=3, column=0, columnspan=5, pady=10, padx=10)
        curret_playlist_frame._scrollbar.configure(width=0)
        self.current_playlist_frame = curret_playlist_frame
        # endregion

        # mid line
        self.app.grid_columnconfigure(5, minsize=10)

        # region playlists frame
        playlists_frame = ctk.CTkScrollableFrame(self.app)
        playlists_frame.grid(row=0, column=6, columnspan=5, rowspan=4, pady=10, padx=10, sticky="n")
        playlists_frame._scrollbar.configure(width=0)
        self.playlists_frame = playlists_frame
        # endregion
    
    # region window drag
    def start_move(self, event):
        self.app.x = event.x
        self.app.y = event.y

    def stop_move(self, event):
        self.app.x = None
        self.app.y = None

    def move(self, event):
        deltax = event.x - self.app.x
        deltay = event.y - self.app.y
        x = self.app.winfo_x() + deltax
        y = self.app.winfo_y() + deltay
        self.app.geometry(f"+{x}+{y}")
    # endregion