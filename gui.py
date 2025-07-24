from tkinter import filedialog
from tkinter.messagebox import showerror
import customtkinter as ctk
from PIL import Image
from confusion import confuse, deconfuse
import config as cfg
from config import IMG_VIEW_SIZE, DEFAULT_COLOR, DEFAULT_SEED

pad = dict(padx=10, pady=10)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('图片混淆工具')
        self.resizable(False, False)

        self.label = ctk.CTkLabel(self, text='欢迎使用图片混淆工具！')
        self.button_confuse = ctk.CTkButton(self, text='混淆图片', command=self.confuse)
        self.button_deconfuse = ctk.CTkButton(self, text='解混淆图片', command=self.deconfuse)

        self.load_file_button = ctk.CTkButton(self, text='加载图片', command=self.load_file)
        self.save_file_button = ctk.CTkButton(self, text='保存图片', command=self.save_file)
        self.reset_img_button = ctk.CTkButton(self, text='重置图片', command=self.reset_img)

        self.seed_label = ctk.CTkLabel(self, text='种子：')
        self.seed = ctk.StringVar(value=DEFAULT_SEED)
        self.seed_entry = ctk.CTkEntry(self, textvariable=self.seed)

        self.config_button = ctk.CTkButton(self, text='配置……', command=self.config)

        self.img_view_frame = ctk.CTkFrame(self)
        self.loaded_img = self.img = Image.new('RGB', IMG_VIEW_SIZE, DEFAULT_COLOR)
        self.img_view_label = ctk.CTkLabel(self.img_view_frame, text='',
                                           image=ctk.CTkImage(self.img, size=IMG_VIEW_SIZE))
        self.img_size_label = ctk.CTkLabel(self.img_view_frame, text='{0}×{1}'.format(*IMG_VIEW_SIZE))

        self.grid_widgets()

    def grid_widgets(self):
        self.label.grid(row=0, column=0, columnspan=2, **pad)

        self.button_confuse.grid(row=1, column=0, **pad)
        self.button_deconfuse.grid(row=1, column=1, **pad)

        self.load_file_button.grid(row=2, column=0, **pad)
        self.save_file_button.grid(row=2, column=1, **pad)

        self.reset_img_button.grid(row=3, column=0, columnspan=2, **pad)

        self.seed_label.grid(row=4, column=0, **pad)
        self.seed_entry.grid(row=4, column=1, columnspan=2, **pad)

        self.config_button.grid(row=5, column=0, columnspan=3, **pad)

        self.img_view_label.pack()
        self.img_size_label.pack(side=ctk.RIGHT, **pad)
        self.img_view_frame.grid(row=0, column=3, rowspan=6, **pad)

    def set_img(self, img: Image.Image):
        self.img = img
        self.img_view_label.configure(image=ctk.CTkImage(light_image=self.img, size=IMG_VIEW_SIZE))
        self.img_size_label.configure(text=f'{img.width}×{img.height}')

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[('Image Files', '*.png;*.jpg;*.jpeg')])
        if file_path:
            self.loaded_img = Image.open(file_path)
            self.set_img(self.loaded_img)

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension='.png', filetypes=[('Image Files', '*.png')])
        if file_path:
            self.img.save(file_path)

    def reset_img(self):
        self.set_img(self.loaded_img)

    def confuse(self):
        self.set_img(confuse(
            self.img,
            (cfg.BLOCK_SIZE, cfg.BLOCK_SIZE), cfg.GRID_WIDTH, cfg.RULER_SIZE,
            self.seed.get()
        ))

    def deconfuse(self):
        img = deconfuse(self.img, self.seed.get())

        if img is None:
            showerror('错误', '无法解密，可能是标尺损坏！')
        else:
            self.set_img(img)

    def config(self):
        ConfigWindow(self).grab_set()


class ConfigWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Config")
        self.resizable(False, False)
        self.parent = parent

        self.block_size = ctk.IntVar(value=cfg.BLOCK_SIZE)
        self.grid_width = ctk.IntVar(value=cfg.GRID_WIDTH)
        self.ruler_size = ctk.IntVar(value=cfg.RULER_SIZE)
        self.black_threshold = ctk.IntVar(value=cfg.BLACK_THRESHOLD)
        self.white_threshold = ctk.IntVar(value=cfg.WHITE_THRESHOLD)

        self.widget_pairs = [
            (ctk.CTkLabel(self, text="混淆　 块大小"), ctk.CTkEntry(self, textvariable=self.block_size)),
            (ctk.CTkLabel(self, text="混淆　 网格宽度"), ctk.CTkEntry(self, textvariable=self.grid_width)),
            (ctk.CTkLabel(self, text="混淆　 标尺大小"), ctk.CTkEntry(self, textvariable=self.ruler_size)),
            (ctk.CTkLabel(self, text="解混淆 标尺黑色阈值"), ctk.CTkEntry(self, textvariable=self.black_threshold)),
            (ctk.CTkLabel(self, text="解混淆 标尺白色阈值"), ctk.CTkEntry(self, textvariable=self.white_threshold))
        ]
        self.confirm_button = ctk.CTkButton(self, text="确定", command=self.on_confirm)

        self.grid_widgets()

    def grid_widgets(self):
        for i, (label, entry) in enumerate(self.widget_pairs):
            label.grid(row=i, column=0, padx=10, pady=5, sticky='W')
            entry.grid(row=i, column=1, padx=10, pady=5)
        self.confirm_button.grid(row=len(self.widget_pairs), column=0, columnspan=2, pady=10)

    def on_confirm(self):
        if not (0 <= self.black_threshold.get() < self.white_threshold.get() < 256):
            showerror('错误', '黑色阈值必须小于白色阈值，且都应在 [0, 256) 范围内')
            return

        if self.block_size.get() <= 0 or self.grid_width.get() <= 0 or self.ruler_size.get() <= 0:
            showerror('错误', '所有值必须大于 0')
            return

        cfg.BLOCK_SIZE = self.block_size.get()
        cfg.GRID_WIDTH = self.grid_width.get()
        cfg.RULER_SIZE = self.ruler_size.get()
        cfg.BLACK_THRESHOLD = self.black_threshold.get()
        cfg.WHITE_THRESHOLD = self.white_threshold.get()

        self.destroy()
