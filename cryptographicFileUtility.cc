//Cryptographic File utility
#include <iostream>
#include <fstream>
#include <string>
#include <unordered_map>
#include <queue>

using namespace std;

// Define a structure for a Huffman Tree node
struct HuffmanNode
	{
	char data;
	unsigned frequency;
	HuffmanNode* left;
	HuffmanNode* right;

	HuffmanNode(char data, unsigned frequency) : data(data), frequency(frequency), left(nullptr), right(nullptr) {}
	};

// Compare function for priority queue to build Huffman Tree
struct CompareNodes
	{
	bool operator()(HuffmanNode* left, HuffmanNode* right)
		{
		return left->frequency > right->frequency;
		}
	};

// Build the Huffman Tree
HuffmanNode* buildHuffmanTree(const unordered_map<char, unsigned>& frequencies)
	{
	priority_queue<HuffmanNode*, vector<HuffmanNode*>, CompareNodes> pq;

	for (const auto& pair : frequencies)
		{
		pq.push(new HuffmanNode(pair.first, pair.second));
		}

	while (pq.size() > 1)
		{
		HuffmanNode* left = pq.top();
		pq.pop();

		HuffmanNode* right = pq.top();
		pq.pop();

		HuffmanNode* internalNode = new HuffmanNode('\0', left->frequency + right->frequency);
		internalNode->left = left;
		internalNode->right = right;

		pq.push(internalNode);
		}

	return pq.top();
	}

// Generate Huffman codes
void generateHuffmanCodes(HuffmanNode* root, const string& code, unordered_map<char, string>& huffmanCodes)
	{
	if (root->left == nullptr && root->right == nullptr)
		{
		huffmanCodes[root->data] = code;
		return;
		}

	generateHuffmanCodes(root->left, code + '0', huffmanCodes);
	generateHuffmanCodes(root->right, code + '1', huffmanCodes);
	}

// Encode the data using Huffman codes
string encodeData(const string& data, const unordered_map<char, string>& huffmanCodes)
	{
	string encodedData;
	for (char c : data)
		{
		encodedData += huffmanCodes.at(c);
		}
	return encodedData;
	}

// Decode the data using Huffman codes
string decodeData(HuffmanNode* root, const string& encodedData)
	{
	string decodedData;
	HuffmanNode* current = root;

	for (char bit : encodedData)
		{
		if (bit == '0')
			{
			current = current->left;
			}
		else
			{
			current = current->right;
			}

		if (current->left == nullptr && current->right == nullptr)
			{
			decodedData += current->data;
			current = root;
			}
		}

	return decodedData;
	}

int main()
	{
	// Input data from the user
	cout << "Enter the data to be encrypted: ";
	string originalData;
	getline(cin, originalData);

	// Count the frequency of each character in the data
	unordered_map<char, unsigned> frequencies;
	for (char c : originalData)
		{
		frequencies[c]++;
		}

	// Build the Huffman Tree
	HuffmanNode* huffmanRoot = buildHuffmanTree(frequencies);

	// Generate Huffman codes
	unordered_map<char, string> huffmanCodes;
	generateHuffmanCodes(huffmanRoot, "", huffmanCodes);

	// Encode the original data
	string encodedData = encodeData(originalData, huffmanCodes);

	// Output the original and encoded data sizes
	cout << "Original Data Size: " << originalData.size() << " bytes\n";
	cout << "Encoded Data Size: " << encodedData.size() / 8 << " bytes\n";

	// Open a file for writing the encrypted data in binary mode
	ofstream encryptedFile("encrypted_data.bin", ios::binary);
	if (!encryptedFile.is_open())
		{
		cerr << "Unable to open the encrypted file." << endl;
		return 1; // Exit with an error code
		}

	// Write the encoded data to the file
	encryptedFile.write(encodedData.c_str(), encodedData.size() / 8);

	// Close the encrypted file
	encryptedFile.close();

	// Decode the encrypted data
	string decodedData = decodeData(huffmanRoot, encodedData);

	// Output the decoded data
	cout << "Encrption of Data completed "<< endl;

	// Open a file for writing the decrypted data
	ofstream decryptedFile("decrypted_data.txt");
	if (!decryptedFile.is_open())
		{
		cerr << "Unable to open the decrypted file." << endl;
		return 1; // Exit with an error code
		}

	// Write the decrypted data to the file
	decryptedFile << decodedData;

	// Close the decrypted file
	decryptedFile.close();

	return 0; // Exit successfully
	}
