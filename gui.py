import tkinter as tk
import tkinter.font as font
from tkinter import ttk

from piece_classifier import Classifier
import cv2
import numpy as np
from logger import Logger
from PIL import Image, ImageTk

IMAGE_SIZE = (720, 480)


class Application(tk.Frame):
    def __init__(self, master=None, src=0) -> None:
        super().__init__(master)
        self.logReport = Logger("GUI")
        self.logReport.logger.info("initializing GUI")
        self.src = src
        self.master = master
        self.width = 1080
        self.height = 720
        self.zetas = 0
        self.tensores = 0
        self.anillos = 0
        self.arandelas = 0
        self.rotas = 0
        self.master.geometry("%dx%d" % (self.width, self.height))
        self.createWidgets()
        self.createFeedFrame()
        self.createPieceFrame()
        self.createStateFrame()
        self.createTableFrame()
        self.master.mainloop()

    def createWidgets(self):
        self.fontLabelText = font.Font(family="Helvetica", size=8)
        # self.labelNameCamera = tk.Label(self.master, text="camera 1", fg="#000000")
        # self.labelNameCamera["font"] = self.fontLabelText
        # self.labelNameCamera.place(x=10, y=10)
        self.btInitCamera = tk.Button(
            self.master,
            text="Iniciar Camara",
            bg="#007a39",
            fg="#ffffff",
            width=12,
            command=self.initCamera,
        )
        self.btInitCamera.place(x=10, y=90 + IMAGE_SIZE[1] * 2)

        self.btStopCamera = tk.Button(
            self.master,
            text="Parar camara",
            bg="#7a0039",
            fg="#ffffff",
            width=12,
            command=self.stopCamera,
        )
        self.btStopCamera.place(x=10 + IMAGE_SIZE[0], y=90 + IMAGE_SIZE[1] * 2)

    def createFeedFrame(self):
        self.labelVideo_1 = tk.Label(self.master, borderwidth=2, relief="solid")
        self.labelVideo_1.place(x=10, y=30)
        imageTk = self.createImageZeros()
        self.labelVideo_1.configure(image=imageTk)
        self.labelVideo_1.image = imageTk

    def createPieceFrame(self):
        self.labelVideo_2 = tk.Label(self.master, borderwidth=2, relief="solid")
        self.labelVideo_2.place(x=IMAGE_SIZE[0] + 20, y=30)
        imageTk = self.createImageZeros()
        self.labelVideo_2.configure(image=imageTk)
        self.labelVideo_2.image = imageTk

    def createStateFrame(self):
        # 1. Create the Frame container with pixel dimensions and background
        self.frameState = tk.Frame(
            self.master,
            width=IMAGE_SIZE[0],
            height=IMAGE_SIZE[1],
            background="light yellow",
        )
        self.frameState.place(x=IMAGE_SIZE[0] + 20, y=IMAGE_SIZE[1] + 60)

        # 2. Create the Label inside the Frame
        self.labelStateText = tk.Label(
            self.frameState,  # Parent is the Frame
            text="Esperando Pieza",
            background="light yellow",  # *** CRITICAL: Ensure this matches the frame's background ***
            foreground="orange",
            font=(
                "Helvetica",
                32,
                "bold",
            ),  # *** Increased font size and bolded for visibility ***
            padx=10,  # Add some internal horizontal padding
            pady=10,  # Add some internal vertical padding
        )

        # 3. Center the Label
        # relx=0.5, rely=0.5 sets the center of the Label to the center of the Frame
        self.labelStateText.place(relx=0.5, rely=0.5, anchor="center")

    def createTableFrame(self):
        self.frameState = tk.Frame(
            self.master,
            width=IMAGE_SIZE[0],
            height=IMAGE_SIZE[1],
            background="white",  # Using white background for the table area
        )
        self.frameState.place(x=10, y=IMAGE_SIZE[1] + 60)
        style = ttk.Style(self.master)

        # Configure the style for the Treeview rows (body text)
        style.configure("mystyle.Treeview", font=("Helvetica", 20, "bold"))

        # Configure the style for the Treeview headings (header text)
        style.configure("mystyle.Treeview.Heading", font=("Helvetica", 24, "bold"))

        # We need to stop the frame from shrinking around the Treeview
        # Since we use .place for the frame in the master, we can use
        # .pack or .grid inside the frame and use propagation control.
        self.frameState.grid_propagate(False)

        columns = ("#1", "#2")
        self.tree = ttk.Treeview(
            self.frameState,
            columns=columns,
            show="headings",  # Only show the column headings, not the default tree column
        )

        # 3. Define Column Headings and Widths (Example)
        self.tree.heading("#1", text="Piece type")
        self.tree.heading("#2", text="Count")

        # Adjust column widths (can be tricky, but we'll try to scale them)
        frame_width = IMAGE_SIZE[0]  # 720
        self.tree.column("#1", width=frame_width // 2, anchor="w")
        self.tree.column("#2", width=frame_width // 2, anchor="center")

        # 4. Insert Example Data (Replace this with your actual data)

        # 5. Place the Treeview using .grid to fill the entire Frame area
        self.tree.grid(row=0, column=0, sticky="nsew")

        # Configure grid weight to ensure the Treeview expands to fill the Frame
        self.frameState.grid_columnconfigure(0, weight=1)
        self.frameState.grid_rowconfigure(0, weight=1)

    def createImageZeros(self):
        frame = np.zeros([IMAGE_SIZE[1], IMAGE_SIZE[0], 3], dtype=np.uint8)
        imagetk = self.convertToFrameTk(frame)
        return imagetk

    def initCamera(self):
        self.camera_1 = Classifier(self.src)
        self.camera_1.start()
        self.showvideo()
        print("Iniciando cámara...")

    def stopCamera(self):
        print("Parando cámara...")
        self.camera_1.stop()

    def showvideo(self):
        try:
            ret, frame = self.camera_1.read()
            if frame is not None:
                imageTk = self.convertToFrameTk(frame=cv2.resize(frame, IMAGE_SIZE))
                self.labelVideo_1.configure(image=imageTk)
                self.labelVideo_1.image = imageTk
                if self.camera_1.separate_frame():
                    self.eval_frame()

            self.labelVideo_1.after(1, self.showvideo)
        except Exception as e:
            print(str(e))

    def eval_frame(self):
        piece = self.camera_1.read_piece()
        self.logReport.debug("Pieza en frame")
        imageTkPiece = self.convertToFrameTk(
            frame=pad_frame(piece, IMAGE_SIZE[0], IMAGE_SIZE[1])
        )
        self.labelVideo_2.configure(image=imageTkPiece)
        self.labelVideo_2.image = imageTkPiece

        piece_type, condition, features_dict = self.camera_1.classify_piece()
        if condition == "Defectuosa" or piece_type == "Unknown":
            self.updateStateLabel("Pieza rota", "dark red", "red")
            self.rotas += 1
        else:
            self.updateStateLabel(f"{piece_type}", "green", "light green")
            if piece_type == "Zeta":
                self.zetas += 1
            if piece_type == "Tensor":
                self.tensores += 1
            if piece_type == "Anillo":
                self.anillos += 1
            if piece_type == "Arandela":
                self.arandelas += 1
        new_data = [
            ("Zetas", self.zetas),
            ("Tensores", self.tensores),
            ("Anillos", self.anillos),
            ("Arandelas", self.arandelas),
            ("Piezas rotas", self.rotas),
        ]
        self.updateTable(new_data)

    def updateTable(self, new_data):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for property_name, value in new_data:
            self.tree.insert("", tk.END, values=(property_name, value))

    def convertToFrameTk(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        imgArray = Image.fromarray(frame)
        imageTk = ImageTk.PhotoImage(image=imgArray)
        return imageTk

    def updateStateLabel(self, new_text, text_color, background_color="light yellow"):
        try:
            self.labelStateText.config(
                text=new_text, fg=text_color, bg=background_color
            )
            self.frameState.config(background=background_color)
        except AttributeError:
            # Handle case where the label might not be fully initialized yet
            print("Error: labelStateText is not yet defined.")


def pad_frame(frame, target_width, target_height):
    H_in, W_in = frame.shape

    if W_in > target_width or H_in > target_height:
        # For this request (adding padding), we simply return the original
        # or handle cropping if necessary, but assuming input is smaller/equal for padding.
        print(
            "Warning: Input frame is larger than target. Cropping might be necessary instead of padding."
        )
        return frame

    pad_w_total = target_width - W_in
    pad_h_total = target_height - H_in

    pad_left = pad_w_total // 2
    pad_top = pad_h_total // 2

    pad_right = pad_w_total - pad_left
    pad_bottom = pad_h_total - pad_top

    padded_frame = cv2.copyMakeBorder(
        frame,
        pad_top,
        pad_bottom,
        pad_left,
        pad_right,
        cv2.BORDER_CONSTANT,
        value=0,  # Since it's grayscale, the value is a single 0
    )

    return padded_frame


def main():
    root = tk.Tk()
    root.title("GUI CAMERA")
    appRunCamera = Application(
        master=root, src="./Vid_Piezas/Anillos/Anillos_Malos.mp4"
    )


if __name__ == "__main__":
    main()
