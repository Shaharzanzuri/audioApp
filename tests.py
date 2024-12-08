import os
import webbrowser
import yt_dlp
from tkinter import Tk, Label, Entry, Button, StringVar, PhotoImage


# Function to trim the URL before '&list'
def trim_url_before_list(url):
    if '&list' in url:
        return url.split('&list')[0]
    return url  # Return original URL if '&list' is not present


class DownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Downtube")
        self.root.geometry("500x600")
        self.root.configure(bg="#E74C3C")

        # Set app icon
        icon_path = "WaveMusic.jpg"  # Update with your image path
        try:
            self.root.iconphoto(False, PhotoImage(file=icon_path))
        except Exception:
            pass

        # Add headline image
        self.headline_image = PhotoImage(file="design photos/Untitled design.png")  # Update with your image path
        Label(self.root, image=self.headline_image, bg="#E74C3C").pack(pady=20)

        # YouTube link prompt
        Label(self.root, text="Please Enter the YouTube link to Download",
              bg="#E74C3C", fg="#F1C40F", font=("Arial", 14)).pack(pady=10)

        # Input field for the YouTube link
        self.link_var = StringVar()
        self.link_input = Entry(self.root, textvariable=self.link_var, font=("Arial", 14), width=40)
        self.link_input.pack(pady=5)

        # Enable pasting with Ctrl+V
        self.link_input.bind("<Control-v>", self.paste_text)

        # Download button
        self.download_button = Button(self.root, text="Click to Download the Song", bg="#8D6E63", fg="#FFF",
                                      font=("Arial", 12), command=self.get_link_info)
        self.download_button.pack(pady=20)

        # Status label
        self.status_label = Label(self.root, text="", bg="#E74C3C", fg="#F1C40F", font=("Arial", 12), wraplength=400)
        self.status_label.pack(pady=10)

        # Placeholder for the "Open File" button
        self.open_file_button = None

    def paste_text(self, event):
        """Paste text from clipboard into the input field."""
        try:
            clipboard_text = self.root.clipboard_get()
            self.link_input.insert("insert", clipboard_text)
        except Exception as e:
            self.status_label.config(text=f"Failed to paste text: {e}")

    def show_success_message(self, filepath):
        """Display success message and create a button to open the file."""
        self.status_label.config(text=f"Download complete! File saved to:\n{filepath}")

        # Add "Open File" button
        if self.open_file_button:
            self.open_file_button.destroy()
        self.open_file_button = Button(self.root, text="Open File", bg="#3498DB", fg="#FFF",
                                       font=("Arial", 12), command=lambda: webbrowser.open(filepath))
        self.open_file_button.pack(pady=10)

    def get_link_info(self):
        """Process the YouTube link and download the file."""
        link = trim_url_before_list(self.link_var.get())
        download_path = "songs"
        filepath = ""
        try:
            # Ensure the download path exists
            os.makedirs(download_path, exist_ok=True)

            # Configure yt-dlp with the desired download path
            ydl_opts = {
                'format': 'bestaudio/best',  # Best available audio format
                'postprocessors': [],  # No additional processing
                'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),  # Save with title as filename
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(link, download=True)
                filepath = os.path.join(download_path, f"{info['title']}.{info['ext']}")
        except Exception as e:
            self.status_label.config(text=f"An error occurred: {e}")
        finally:
            if filepath:
                self.show_success_message(filepath)


if __name__ == "__main__":
    root = Tk()
    app = DownloaderApp(root)
    root.mainloop()
