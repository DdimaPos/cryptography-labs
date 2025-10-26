#include <algorithm>
#include <iostream>
#include <string>
#include <unordered_map>
#include <vector>

using namespace std;

const vector<string> ALFABET = {"A", "Ă", "Â", "B", "C", "D", "E", "F",
                                "G", "H", "I", "Î", "J", "K", "L", "M",
                                "N", "O", "P", "Q", "R", "S", "Ș", "T",
                                "Ț", "U", "V", "W", "X", "Y", "Z"};
const int ALPHABET_SIZE = ALFABET.size();

unordered_map<string, int> createCharToNum() {
  unordered_map<string, int> m;
  // createa a map of chars from 0 to 30
  for (int i = 0; i < ALPHABET_SIZE; i++)
    m[ALFABET[i]] = i;
  return m;
}

string replaceAll(string text, const string &from, const string &to) {
  size_t start = 0;
  while ((start = text.find(from, start)) != string::npos) {
    text.replace(start, from.length(), to);
    start += to.length();
  }
  return text;
}

string normalizeText(const string &input) {
  string text = input;
  text = replaceAll(text, "ă", "Ă");
  text = replaceAll(text, "â", "Â");
  text = replaceAll(text, "î", "Î");
  text = replaceAll(text, "ș", "Ș");
  text = replaceAll(text, "ş", "Ș");
  text = replaceAll(text, "ț", "Ț");
  text = replaceAll(text, "ţ", "Ț");

  // remove spaces and capitalize
  text.erase(remove(text.begin(), text.end(), ' '), text.end());
  for (auto &c : text)
    c = toupper(static_cast<unsigned char>(c));
  return text;
}

// romanian characters can be 2 or 3 bites long, so I had to split the strint
// properly in graphemes. An analogy could be that 😩 emoji is actually 5 bytes
// long in C++ even if you see only 1

vector<string> splitUTF8(const string &text) {
  // to show the utf issues
  // cout << "ĂÂÎȘȚ".
  // cout << "😩".
  vector<string> chars;
  for (size_t i = 0; i < text.size();) {
    unsigned char c = text[i];
    int len = 1;
    // pattern detection:
    // 110xxxxx(2byte char),
    if ((c & 0b11100000) == 0b11000000)
      len = 2;
    // 111xxxxx(3byte char)
    else if ((c & 0b11110000) == 0b11100000)
      len = 3;
    chars.push_back(text.substr(i, len));
    i += len;
  }
  return chars;
}

bool validateText(const vector<string> &chars,
                  const unordered_map<string, int> &map) {
  for (auto &ch : chars) {
    if (!map.count(ch))
      return false;
  }
  return true;
}

string vigenere(const vector<string> &msg, const vector<string> &key,
                const unordered_map<string, int> &map, bool encrypt) {
  string result;
  for (size_t i = 0; i < msg.size(); i++) {
    int p = map.at(msg[i]);
    int k = map.at(key[i % key.size()]);
    int c = encrypt ? (p + k) % ALPHABET_SIZE
                    : (p - k + ALPHABET_SIZE) % ALPHABET_SIZE;
    result += ALFABET[c];
  }
  return result;
}

int main() {
  auto map = createCharToNum();

  cout << "Alege operatia (1 - Criptare, 2 - Decriptare): ";
  int opt;
  cin >> opt;
  cin.ignore();

  cout << "Introdu cheia (minim 7 caractere): ";
  string key;
  getline(cin, key);
  key = normalizeText(key);
  auto keyChars = splitUTF8(key);

  if (keyChars.size() < 7) {
    cerr << "Eroare: cheia trebuie sa aiba cel putin 7 caractere.\n";
    return 1;
  }
  if (!validateText(keyChars, map)) {
    cerr << "Eroare: cheia contine caractere invalide.\n";
    return 1;
  }

  cout << "Introdu mesajul: ";
  string msg;
  getline(cin, msg);
  msg = normalizeText(msg);
  auto msgChars = splitUTF8(msg);
  if (!validateText(msgChars, map)) {
    cerr << "Eroare: mesajul contine caractere invalide.\n";
    return 1;
  }

  bool encrypt = (opt == 1);
  string result = vigenere(msgChars, keyChars, map, encrypt);

  if (encrypt)
    cout << "Criptograma: " << result << "\n";
  else
    cout << "Mesaj decriptat: " << result << "\n";

  return 0;
}
