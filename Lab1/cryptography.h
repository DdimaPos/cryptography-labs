#ifndef CRYPTOGRAPHY_H
#define CRYPTOGRAPHY_H

#include <map>
#include <string>

std::string encrypt(int key, std::string message, std::string salt);
std::string decrypt(int key, std::string message, std::string salt);

#endif
