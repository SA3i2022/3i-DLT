#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
import os
import onnxruntime as rt
import SBAccess
import SBSupport
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QLineEdit, QFormLayout, QLabel, QWidget,QSplitter,QHBoxLayout, QFileDialog,QComboBox
from PySide6.QtGui import QPixmap, QImage
import numpy as np


# In[ ]:


image_array = None
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        main_splitter = QSplitter()

        # Main layout
        left_widget = QWidget()
        left_layout = QVBoxLayout()

        # Fetch Image Button and Inputs
        open_file_button = QPushButton("Open Model")
        open_file_button.clicked.connect(self.open_file)
        open_file_button.setStyleSheet("border: 2px solid black; padding: 5px;")

        fetch_image_button = QPushButton("Fetch Image")
        fetch_image_button.clicked.connect(self.fetch_image)

        self.input1 = QLineEdit()
        self.input1.setPlaceholderText("Image to Fetch")

        self.input2 = QLineEdit()
        self.input2.setPlaceholderText("Channel to Fetch")

        form_layout = QFormLayout()
        form_layout.addRow(QLabel("Image Index:"), self.input1)
        form_layout.addRow(QLabel("Channel:"), self.input2)

        self.file_name_label = QLabel()

        self.model_info = QLabel()
        self.model_output = QLabel()
        self.model_info.setWordWrap(True)
        self.model_output.setWordWrap(True)

        # Add a dropdown for data type selection
        self.data_type_combo = QComboBox()
        self.data_type_combo.addItems(["uint16", "float32", "double"])

        apply_model_button = QPushButton("Apply Model")
        apply_model_button.clicked.connect(self.apply_image)
        apply_model_button.setStyleSheet("border: 2px solid black; padding: 5px;")

        # Add inputs and button to the layout
        left_layout.addLayout(form_layout)
        left_layout.addWidget(fetch_image_button)
        left_layout.addWidget(open_file_button)
        left_layout.addWidget(self.file_name_label)
        left_layout.addWidget(self.model_info)
        left_layout.addWidget(self.model_output)
        left_layout.addWidget(self.data_type_combo)  # Place the dropdown above the apply model button
        left_layout.addWidget(apply_model_button)
        left_layout.addStretch()

        left_widget.setLayout(left_layout)

        # Image display labels
        self.image_label = QLabel()
        self.image_label.setMinimumSize(400, 400)
        self.image_label.setStyleSheet("border: 1px solid black;")

        self.output_label = QLabel()
        self.output_label.setMinimumSize(400, 400)
        self.output_label.setStyleSheet("border: 1px solid black;")

        image_splitter = QSplitter()
        image_splitter.addWidget(self.image_label)
        image_splitter.addWidget(self.output_label)

        main_splitter.addWidget(left_widget)
        main_splitter.addWidget(image_splitter)

        # Set the central widget of the Window.
        container = QWidget()
        main_layout = QHBoxLayout()
        main_layout.addWidget(main_splitter)
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Initialize instance variables
        self.m = None
        self.output_names = None
        self.input_name = None
        self.input_shape = None
    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open ONNX File", "", "Model (*.onnx)")
        if file_name:
            model_name = os.path.splitext(os.path.basename(file_name))[0]
            self.m = rt.InferenceSession(file_name)
            # Print the model inputs to verify their names, shapes, and types
            for i in self.m.get_inputs():
                self.model_info.setText(f"Input name: {i.name}, shape: {i.shape}, type: {i.type}")# Extract the base name without extension
                self.input_shape = i.shape
            output_names = [output.name for output in self.m.get_outputs()]
            output_info = "Model Outputs:\n" + ", ".join(output_names)
            self.model_output.setText(output_info)
            self.file_name_label.setText(model_name)
            self.input_name = self.m.get_inputs()[0].name
        
    def fetch_image(self):
        global image_array
        try:
            num1 = int(self.input1.text())
            num2 = int(self.input2.text())
            image_array = SBSupport.get_array(num1, num2)
            image_array=np.squeeze(image_array)
            self.display_image(image_array)
        except ValueError:
            print("Please enter valid numbers")


    def preprocess_image(self):
        global image_array
        data_type = self.data_type_combo.currentText()
        if data_type =='uint16':
            image_array = image_array / np.max(image_array)
            image_array = np.expand_dims(image_array, axis=0)
            image_array = np.array(image_array, dtype=np.uint16)
        elif data_type =='float32':
            image_array = image_array / np.max(image_array)
            image_array = np.expand_dims(image_array, axis=0)
            image_array = np.array(image_array, dtype=np.float32)
        elif data_type =='double':
            image_array = image_array / np.max(image_array)
            image_array = np.expand_dims(image_array, axis=0)
            image_array = np.array(image_array, dtype=np.double)
        image_array=np.reshape(image_array,self.input_shape)
        return image_array
    
    def apply_image(self):
        global image_array
        if self.m is not None:
            processed_image = self.preprocess_image()
            onnx_pred = self.m.run(self.output_names, {self.input_name: processed_image})
            print("Model prediction:", onnx_pred)
            lab=onnx_pred[0][0]
            print(np.shape(lab))
            self.display_labels(lab)
        else:
            print("Model or image not available")
        
    def display_image(self, image_array):
        height, width = image_array.shape
        image_array = (image_array / np.max(image_array))*255
        image_array=image_array.astype(np.uint8)
        q_image = QImage(image_array.data, width, height, width, QImage.Format_Grayscale8)
        pixmap = QPixmap.fromImage(q_image)
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)

    def display_labels(self,label):
        label=np.squeeze(label)
        label = (label / np.max(label) * 255).astype(np.uint8)
        print(label)
        height, width = label.shape
        bytes_per_line = width
        q_image = QImage(label.data, width, height, bytes_per_line, QImage.Format_Grayscale8)
        pixmap = QPixmap.fromImage(q_image)
        self.output_label.setPixmap(pixmap)
        self.output_label.setScaledContents(True)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()

