This C++ code implements a basic cryptographic file utility using the Huffman coding algorithm for compression. Here's a description of the main components and functionality of the code:

Huffman Coding:
HuffmanNode Structure:

Represents a node in the Huffman Tree.
Contains character data, frequency, and pointers to left and right children.
CompareNodes Structure:

Functor used for the priority queue to compare Huffman nodes based on their frequencies.
buildHuffmanTree Function:

Constructs a Huffman Tree based on the frequency of characters in the input data.
generateHuffmanCodes Function:

Recursively generates Huffman codes for each character in the tree.
encodeData Function:

Uses the generated Huffman codes to encode the input data.
decodeData Function:

Decodes the encoded data using the Huffman Tree.
Main Functionality:
User Input:

Prompts the user to enter the data to be encrypted.
Frequency Calculation:

Counts the frequency of each character in the input data.
Huffman Tree Construction:

Builds a Huffman Tree based on the calculated frequencies.
Huffman Code Generation:

Generates Huffman codes for each character in the tree.
Data Encoding:

Encodes the original data using the generated Huffman codes.
Output Information:

Prints the size of the original and encoded data.
File Output - Encryption:

Writes the encoded data to a binary file named "encrypted_data.bin."
Data Decoding:

Decodes the encrypted data using the Huffman Tree.
File Output - Decryption:

Writes the decoded data to a text file named "decrypted_data.txt."
Notes:
The code assumes binary encoding, and the encoded data is written to a binary file.
The program reports the sizes of the original and encoded data in bytes.
The decoding process is performed and saved in a separate text file.
Usage:
Compile and run the program.
Enter the data to be encrypted when prompted.
Check the console output for original and encoded data sizes.
The encrypted data is saved in "encrypted_data.bin."
The decrypted data is saved in "decrypted_data.txt."
Note: Ensure that you have the necessary file write permissions for the program to create the output files.
