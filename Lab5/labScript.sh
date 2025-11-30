#!/bin/bash

# phase 0: setup DB
echo "--- Setting up Environment ---"
rm -rf demoCA newcerts *.pem *.key *.crt *.csr *.txt *.sig *.crl # cleanup
mkdir -p demoCA/newcerts
touch demoCA/index.txt
echo 1000 > demoCA/serial
echo 1000 > demoCA/crlnumber

# phase 1: create CA 
echo "--- Generating CA Key and Certificate ---"
openssl genrsa -out ca.key 4096
openssl req -new -x509 -key ca.key -out ca.crt -days 3650 -subj "/CN=RootCA"

# phase 2: create Johnny 
echo "--- Generating User Key and CSR ---"
openssl genrsa -out john.key 2048
openssl req -new -key john.key -out john.csr -subj "/CN=John"

# phase 3: issue certificate (365 days)
echo "--- Signing User Certificate ---"
openssl ca -config my_config.cnf -in john.csr -out john.crt -batch

# phase 4: sign and verify
echo "--- Testing Signature ---"
echo "I agree to the terms." > doc.txt
# sign
openssl dgst -sha256 -sign john.key -out doc.sig doc.txt
# extract public key
openssl x509 -in john.crt -pubkey -noout > john_pub.pem

openssl dgst -sha256 -verify john_pub.pem -signature doc.sig doc.txt

#phase 5: Revocation 
echo "--- Revoking Certificate ---"
openssl ca -config my_config.cnf -revoke john.crt
openssl ca -config my_config.cnf -gencrl -out revocation_list.crl

echo "--- Checking Revocation Status ---"
openssl verify -crl_check -CAfile ca.crt -CRLfile revocation_list.crl john.crt > /dev/null 2>&1

if [ $? -ne 0 ]; then
    echo "SUCCESS: The certificate is correctly identified as REVOKED."
else
    echo "FAILURE: The certificate is still valid (it should be revoked)."
fi
