#include <map>
#include <set>
#include <string>

using namespace std;

const array<char, 26> alphabet = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
                                  'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                                  'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'};

map<char, int> buildEncryptionMap(string salt) {
  map<char, int> caesarMap;
  set<char> used;

  int index = 0;
  for (char c : salt) {
    caesarMap[c] = index++;
    used.insert(c);
  }

  for (char c : alphabet) {
    if (!used.count(c)) {
      caesarMap[c] = index++;
      used.insert(c);
    }
  }

  return caesarMap;
}

map<int, char> buildDecryptionMap(map<char, int> inputMap) {
  map<int, char> decrMap;

  for (auto &[key, value] : inputMap) {
    decrMap[value] = key;
  }

  return decrMap;
}

string encrypt(int key, string message, string salt) {
  string encryptedString = "";
  map<char, int> caesarMap = buildEncryptionMap(salt);
  map<int, char> decryptionMap = buildDecryptionMap(caesarMap);

  for (int i = 0; i < message.length(); i++) {
    int messageCharIndex = caesarMap[message[i]];
    int newIndex = (messageCharIndex + key) % 26;
    encryptedString += decryptionMap[newIndex];
  }

  return encryptedString;
}

string decrypt(int key, string message, string salt) {
  string decryptedString = "";
  map<char, int> caesarMap = buildEncryptionMap(salt);
  map<int, char> decryptionMap = buildDecryptionMap(caesarMap);

  for (int i = 0; i < message.length(); i++) {
    int messageCharIndex = caesarMap[message[i]];
    int newIndex = (messageCharIndex - key + 26) % 26;
    decryptedString += decryptionMap[newIndex];
  }

  return decryptedString;
}
