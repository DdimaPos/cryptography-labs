#include "cryptography.h"
#include "userInputProcessing.h"
#include <iostream>
#include <string>

using namespace std;

enum OPERATION_TYPES { Encryption, Decryption };

int main() {
  OPERATION_TYPES operation = operationVariant() == 1 ? Encryption : Decryption;

  int key = customKey();
  string message = getMessage();
  string finalMessage = "";
  string salt = getSalt();

  switch (operation) {
  case Encryption:
    finalMessage = encrypt(key, message, salt);
    break;
  case Decryption:
    finalMessage = decrypt(key, message, salt);
    break;
  default:
    break;
  }

  cout << "Your message is: " << finalMessage << endl;

  return 0;
}
