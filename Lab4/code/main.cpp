#include <algorithm>
#include <bitset>
#include <iomanip>
#include <iostream>
#include <random>
#include <sstream>
#include <string>

using namespace std;

// left shift schedule for DES (number of shifts for each round)
const int SHIFT_SCHEDULE[16] = {1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1};

bitset<28> leftCircularShift(bitset<28> bits, int shifts) {
  bitset<28> result;
  for (int i = 0; i < 28; i++) {
    result[i] = bits[(i + 28 - shifts) % 28];
  }
  return result;
}

// function to convert bitset to binary string with spaced. readability
template <size_t N> string formatBitset(bitset<N> bits) {
  string result = "";
  for (int i = N - 1; i >= 0; i--) {
    result += (bits[i] ? '1' : '0');
    if (i > 0 && i % 4 == 0) {
      result += " ";
    }
  }
  return result;
}

// function to convert bitset to hexadecimal string
template <size_t N> string toHex(bitset<N> bits) {
  unsigned long long value = bits.to_ullong();
  stringstream ss;
  ss << "0x" << uppercase << hex << setw((N + 3) / 4) << setfill('0') << value;
  return ss.str();
}

// function to display the shift schedule table
void displayShiftScheduleTable() {
  cout << "\n=== DES Left Shift Schedule Table ===" << endl;
  cout << "+--------+------------+" << endl;
  cout << "| Round  | Shifts     |" << endl;
  cout << "+--------+------------+" << endl;
  for (int i = 0; i < 16; i++) {
    cout << "|   " << setw(2) << (i + 1) << "   |     " << setw(2)
         << SHIFT_SCHEDULE[i] << "     |" << endl;
  }
  cout << "+--------+------------+" << endl;
}

int main() {
  cout << "==================================================" << endl;
  cout << "    DES Algorithm - Task 2.2 Implementation" << endl;
  cout << "    Determine Ci and Di for a given round i" << endl;
  cout << "==================================================" << endl;

  displayShiftScheduleTable();

  bitset<56> kPlus; // K+ (56 bits after PC-1)
  int choice;

  cout << "\nHow would you like to provide K+?" << endl;
  cout << "1. Enter manually (56 bits)" << endl;
  cout << "2. Generate randomly" << endl;
  cout << "Choice: ";
  cin >> choice;

  if (choice == 1) {
    string input;
    cout << "\nEnter K+ (56 bits, no spaces): ";
    cin >> input;

    // Remove any spaces
    input.erase(remove(input.begin(), input.end(), ' '), input.end());

    if (input.length() != 56) {
      cout << "Error: K+ must be exactly 56 bits!" << endl;
      return 1;
    }

    // Convert string to bitset (reverse order for bitset indexing)
    for (int i = 0; i < 56; i++) {
      kPlus[55 - i] = (input[i] == '1');
    }
  } else {
    // Generate random K+
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<> dis(0, 1);

    for (int i = 0; i < 56; i++) {
      kPlus[i] = dis(gen);
    }
    cout << "\nK+ generated randomly." << endl;
  }

  cout << "\n=== Initial K+ (56 bits) ===" << endl;
  cout << "Binary: " << formatBitset(kPlus) << endl;
  cout << "Hex:    " << toHex(kPlus) << endl;

  // split K+ into C0 (left 28 bits) and D0 (right 28 bits)
  bitset<28> C0, D0;

  // extract C0 (bits 55-28 in our representation)
  for (int i = 0; i < 28; i++) {
    C0[i] = kPlus[i + 28];
  }

  // extract D0 (bits 27-0 in our representation)
  for (int i = 0; i < 28; i++) {
    D0[i] = kPlus[i];
  }

  cout << "\n=== Initial Split ===" << endl;
  cout << "C0 (left 28 bits):  " << formatBitset(C0) << " (" << toHex(C0) << ")"
       << endl;
  cout << "D0 (right 28 bits): " << formatBitset(D0) << " (" << toHex(D0) << ")"
       << endl;

  int roundNumber;
  cout << "\nEnter round number i (1-16): ";
  cin >> roundNumber;

  if (roundNumber < 1 || roundNumber > 16) {
    cout << "Error: Round number must be between 1 and 16!" << endl;
    return 1;
  }

  // calculate Ci and Di by performing cumulative shifts
  bitset<28> C = C0;
  bitset<28> D = D0;

  cout << "\n=== Calculating Ci and Di (showing all intermediate steps) ==="
       << endl;

  int totalShifts = 0;
  for (int i = 0; i < roundNumber; i++) {
    int shifts = SHIFT_SCHEDULE[i];
    totalShifts += shifts;

    C = leftCircularShift(C, shifts);
    D = leftCircularShift(D, shifts);

    cout << "\nRound " << (i + 1) << " (shift " << shifts << " position"
         << (shifts > 1 ? "s" : "") << "):" << endl;
    cout << "  C" << (i + 1) << ": " << formatBitset(C) << " (" << toHex(C)
         << ")" << endl;
    cout << "  D" << (i + 1) << ": " << formatBitset(D) << " (" << toHex(D)
         << ")" << endl;
  }

  cout << "\n==================================================" << endl;
  cout << "                 FINAL RESULT" << endl;
  cout << "==================================================" << endl;
  cout << "For round i = " << roundNumber << ":" << endl;
  cout << "\nC" << roundNumber << " (28 bits):" << endl;
  cout << "  Binary: " << formatBitset(C) << endl;
  cout << "  Hex:    " << toHex(C) << endl;

  cout << "\nD" << roundNumber << " (28 bits):" << endl;
  cout << "  Binary: " << formatBitset(D) << endl;
  cout << "  Hex:    " << toHex(D) << endl;

  cout << "\nTotal left shifts applied: " << totalShifts << endl;
  cout << "==================================================" << endl;

  return 0;
}
