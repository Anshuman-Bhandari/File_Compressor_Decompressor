import heapq
import os
import tkinter as tk
from tkinter import filedialog
from threading import Thread

class BinaryTree:
    def __init__(self, value, frequ):
        self.value = value
        self.frequ = frequ
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.frequ < other.frequ

    def __eq__(self, other):
        return self.frequ == other.frequ

class Huffmancode:
    
    def __init__(self, path):
        self.path = path
        self._heap = []
        self._code = {}
        self._reversecode = {}

    def _frequency_from_text(self, text):
        frequ_dict = {}
        for char in text:
            if char not in frequ_dict:
                frequ_dict[char] = 0
            frequ_dict[char] += 1
        return frequ_dict

    def _build_heap(self, frequency_dict):
        for key in frequency_dict:
            frequency = frequency_dict[key]
            binary_tree_node = BinaryTree(key, frequency)
            heapq.heappush(self._heap, binary_tree_node)

    def _build_binary_tree(self):
        while len(self._heap) > 1:
            binary_tree_node_1 = heapq.heappop(self._heap)
            binary_tree_node_2 = heapq.heappop(self._heap)
            sum_of_freq = binary_tree_node_1.frequ + binary_tree_node_2.frequ
            newnode = BinaryTree(None, sum_of_freq)
            newnode.left = binary_tree_node_1
            newnode.right = binary_tree_node_2
            heapq.heappush(self._heap, newnode)

    def _build_tree_code_helper(self, root, curr_bits):
        if root is None:
            return
        if root.value is not None:
            self._code[root.value] = curr_bits
            self._reversecode[curr_bits] = root.value
            return
            
        self._build_tree_code_helper(root.left, curr_bits + '0')
        self._build_tree_code_helper(root.right, curr_bits + '1')

    def _build_tree_code(self):
        root = heapq.heappop(self._heap)
        self._build_tree_code_helper(root, '')

    def _build_encoded_text(self, text):
        encoded_text = ''
        for char in text:
            encoded_text += self._code[char]

        return encoded_text

    def _build_padded_text(self, encoded_text):
        padding_value = 8 - len(encoded_text) % 8
        for i in range(padding_value):
            encoded_text += '0'

        padded_info = "{0:08b}".format(padding_value)
        padded_text = padded_info + encoded_text
        return padded_text

    def _build_byte_array(self, padded_text):
        array = []
        for i in range(0, len(padded_text), 8):
            byte = padded_text[i:i+8]
            array.append(int(byte, 2))

        return array
    
    def compression(self):
        print("Compression For Your File Starts......")
        filename, file_extension = os.path.splitext(self.path)
        output_path = filename + '.bin'
        with open(self.path, 'r+') as file, open(output_path, 'wb') as output:
            text = file.read()
            text = text.rstrip()
            frequency_dict = self._frequency_from_text(text)
            self._build_heap(frequency_dict)
            self._build_binary_tree()
            self._build_tree_code()
            encoded_text = self._build_encoded_text(text)
            padded_text = self._build_padded_text(encoded_text)
            bytes_array = self._build_byte_array(padded_text)
            final_bytes = bytes(bytes_array)
            output.write(final_bytes)
        print('Compressed successfully')
        return output_path

    def _remove_padding(self, text):
        padded_info = text[:8]
        padding_value = int(padded_info, 2)
        text = text[8:-padding_value]
        return text

    def _decoded_text(self, text):
        current_bits = ''
        decoded_text = ''
        for char in text:
            current_bits += char
            if current_bits in self._reversecode:
                decoded_text += self._reversecode[current_bits]
                current_bits = ''
        return decoded_text

    def decompress(self, input_path):
        filename, file_extension = os.path.splitext(input_path)
        output_path = 'SampIe' + '.txt'
        with open(input_path, 'rb') as file, open(output_path, 'w') as output:
            bit_string = ''
            byte = file.read(1)
            while byte:
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8, '0')
                bit_string += bits
                byte = file.read(1)

            text_after_removing_padding = self._remove_padding(bit_string)
            actual_text = self._decoded_text(text_after_removing_padding) 
            output.write(actual_text)
        return output_path


class HuffmanGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Huffman Compression Tool")
        self.root.geometry("400x320")

        self.file_path = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        # File selection
        self.label_file = tk.Label(self.root, text="Select File:")
        self.label_file.pack(pady=10)
        
        self.entry_file = tk.Entry(self.root, textvariable=self.file_path, width=30)
        self.entry_file.pack(pady=10)

        self.btn_browse = tk.Button(self.root, text="Browse", command=self.browse_file)
        self.btn_browse.pack(pady=10)

        # Compression and Decompression buttons
        self.btn_compress = tk.Button(self.root, text="Compress", command=self.compress_thread)
        self.btn_compress.pack(pady=10)

        self.btn_decompress = tk.Button(self.root, text="Decompress", command=self.decompress_thread)
        self.btn_decompress.pack(pady=10)

        # Loading screen
        self.loading_label = tk.Label(self.root, text="Processing...")
        self.loading_label.pack_forget()

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            self.file_path.set(file_path)

    def compress_thread(self):
        self.loading_label.pack()
        self.root.update()
        Thread(target=self.compress).start()

    def decompress_thread(self):
        self.loading_label.pack()
        self.root.update()
        Thread(target=self.decompress).start()

    def compress(self):
        try:
            huffman = Huffmancode(self.file_path.get())
            compressed_file = huffman.compression()
            self.show_message(f"File compressed successfully.\nOutput: {compressed_file}", "Compression")
        except Exception as e:
            self.show_message(f"Compression failed.\nError: {str(e)}", "Compression")

    def decompress(self):
        try:
            huffman = Huffmancode(self.file_path.get())
            decompressed_file = huffman.decompress(self.file_path.get())
            self.show_message(f"File decompressed successfully.\nOutput: {decompressed_file}", "Decompression")
        except Exception as e:
            self.show_message(f"Decompression failed.\nError: {str(e)}", "Decompression")

    def show_message(self, message, title):
        self.loading_label.pack_forget()
        tk.messagebox.showinfo(title, message)

if __name__ == "__main__":
    root = tk.Tk()
    app = HuffmanGUI(root)
    root.mainloop()


path = input("Enter the path of your File which you need to compress : ")
h = Huffmancode(path)
compressed_file = h.compression()
h.decompress(compressed_file)
