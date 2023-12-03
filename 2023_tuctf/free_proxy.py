# author: @shipcod3

import socket
import rsa
import os
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s1.settimeout(1)
s2.settimeout(1)
s1.connect(("chals.tuctf.com",30000))
s2.connect(("chals.tuctf.com",30001))

bob_pubkey = None
alice_pubkey = None
shared_key = None

mitm_keys = rsa.newkeys(1024)


def run():
    handshake()
    key_exchange()
    msg_loop()

def handshake():
    global bob_pubkey
    global alice_pubkey

    # Receive pubkey from Bob
    h1 = s1.recv(4096)
    print("BOB PUBKEY: ", h1)
    bob_pubkey = rsa.PublicKey.load_pkcs1(b64decode(h1))

    # Inject pubkey to Alice
    s2.sendall(b64encode(mitm_keys[0].save_pkcs1()))

    # Receive Alice Pubkey
    h2 = s2.recv(4096)
    print("ALICE PUBKEY: ", h2)
    alice_pubkey = rsa.PublicKey.load_pkcs1(b64decode(h2))

    # Inject pubkey to Bob
    s1.sendall(b64encode(mitm_keys[0].save_pkcs1()))

def key_exchange():
    global shared_key

    # Receive Bobs proposed AES key
    k1 = s1.recv(4096)
    
    # Decrypt shared_key with the injected pub/priv key pair
    shared_key = rsa.decrypt(b64decode(k1), mitm_keys[1])
    print(shared_key)
    # Encrypt and send shared_key with alice's pub key
    s2.sendall(b64encode(rsa.encrypt(shared_key, alice_pubkey)))

    # Receive decrypt and forward test OK msg
    resp = decrypt(b64decode(s2.recv(4096))).decode('utf8')
    print(resp)
    s1.sendall(b64encode(encrypt(resp)))

# Use intercepted keyexchange to decrypt message contents
def msg_loop():
    while True:
        try:
            m1 = decrypt(b64decode(s1.recv(4096))).decode('utf8')
            print("BOB: ", m1)
            s2.sendall(b64encode(encrypt(m1)))
            m2 = decrypt(b64decode(s2.recv(4096))).decode('utf8')
            print("ALICE: ", m2)
            s1.sendall(b64encode(encrypt(m2)))
        except socket.timeout:
            print("Done.")
            break

def encrypt(data:str):
    iv = os.urandom(AES.block_size)
    cipher = AES.new(shared_key, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))

def decrypt(data:bytes):
    cipher = AES.new(shared_key, AES.MODE_CBC, data[:AES.block_size])
    return unpad(cipher.decrypt(data[AES.block_size:]), AES.block_size)

run()