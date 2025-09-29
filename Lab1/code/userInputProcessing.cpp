#include <iostream>
#include <limits>
#include <string>

using namespace std;

int operationVariant() {
  string line;
  int operation;
  cout << "Choose the operation:\n";
  cout << "1. Encryption\n";
  cout << "2. Decryption\n";
  cout << "Introduce your choice: ";
  getline(cin, line);
  operation = stoi(line);
  return operation;
}

int customKey() {
  int key;

  cout << "Introduce the key that you want to use during the operation: \n";
  cin >> key;

  cin.ignore(numeric_limits<streamsize>::max(), '\n');

  return key % 26;
}

string userMessage() {
  string message;
  cout << "Introduce the message to be processed:\n";
  getline(cin, message);
  return message;
}

string tryParseMessage(string raw) {
  string parsed = "";
  for (char symbol : raw) {
    if (symbol == ' ')
      continue;

    if (symbol >= 'a' && symbol <= 'z') {
      parsed += static_cast<char>(toupper(symbol));
    } else if (symbol >= 'A' && symbol <= 'Z') {
      parsed += symbol;
    } else {
      return ""; // return empty string = invalid input
    }
  }
  return parsed;
}

string getMessage() {
  while (true) {
    string raw = userMessage();
    string parsed = tryParseMessage(raw);
    if (!parsed.empty()) {
      return parsed;
    } else {
      cout << "Please introduce only the symbols of the English alphabet\n";
    }
  }
}

string getSalt() {
  string salt;
  while (true) {
    cout << "Introduce salting word (press Enter to skip): ";
    getline(cin, salt);

    if (salt.empty())
      return ""; // skip

    if (salt.length() < 7) {
      cout << "Introduce a salt with minimum 7 symbols\n";
      continue;
    }

    bool valid = true;
    for (char &symbol : salt) {
      if (isalpha(symbol)) {
        symbol = static_cast<char>(toupper(symbol));
      } else {
        cout << "Please introduce only the symbols of English alphabet\n";
        valid = false;
        break;
      }
    }

    if (valid)
      return salt;
  }
}
