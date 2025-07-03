
import tkinter as tk
from tkinter import messagebox

class YouTubeDownloaderApp:
    def __init__(self, master):
        self.master = master
        master.title("YouTube Downloader")

        self.url_label = tk.Label(master, text="YouTube URL:")
        self.url_label.pack()

        self.url_entry = tk.Entry(master, width=50)
        self.url_entry.pack()

        self.download_button = tk.Button(master, text="Download", command=self.download_video)
        self.download_button.pack()

        self.status_label = tk.Label(master, text="")
        self.status_label.pack()

        self.path_label = tk.Label(master, text="Download Path:")
        self.path_label.pack()

        self.download_path_var = tk.StringVar()
        self.download_path_entry = tk.Entry(master, textvariable=self.download_path_var, width=50, state='readonly')
        self.download_path_entry.pack()

        self.browse_button = tk.Button(master, text="Browse", command=self.select_download_path)
        self.browse_button.pack()

        # Set default download path to current working directory
        import os
        self.download_path_var.set(os.getcwd())

    def select_download_path(self):
        from tkinter import filedialog
        path = filedialog.askdirectory()
        if path:
            self.download_path_var.set(path)

    def download_video(self):
        url = self.url_entry.get()
        download_path = self.download_path_var.get()

        if not url:
            messagebox.showwarning("Input Error", "Please enter a YouTube URL.")
            return
        if not download_path:
            messagebox.showwarning("Input Error", "Please select a download path.")
            return

        self.status_label.config(text=f"Downloading: {url}")
        import threading
        import yt_dlp

        def download_thread():
            try:
                ydl_opts = {
                    'progress_hooks': [self.progress_hook],
                    'outtmpl': f'{download_path}/%(title)s.%(ext)s',
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                self.master.after(0, lambda: self.status_label.config(text="Download complete!"))
                self.master.after(0, lambda: messagebox.showinfo("Download Complete", "Video downloaded successfully!"))
            except Exception as e:
                self.master.after(0, lambda: self.status_label.config(text=f"Error: {e}"))
                self.master.after(0, lambda: messagebox.showerror("Download Error", f"An error occurred: {e}"))

        thread = threading.Thread(target=download_thread)
        thread.start()

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            p = d['_percent_str']
            self.master.after(0, lambda: self.status_label.config(text=f"Downloading: {p}"))
        elif d['status'] == 'finished':
            self.master.after(0, lambda: self.status_label.config(text="Processing..."))


if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloaderApp(root)
    root.mainloop()
