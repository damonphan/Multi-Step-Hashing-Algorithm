import hashlib
import time
import random
import math

# Set three different hash functions
def sha256(data):
    return hashlib.sha256(data.encode()).hexdigest()

def sha3(data):
    return hashlib.sha3_256(data.encode()).hexdigest()

# Simulate a similar version of swift

def swifft_mock(data):
    mixed = 0
    for i, c in enumerate(data.encode()):
        mixed += (c * (i + 1)) % 251
    return hashlib.sha3_256(str(mixed).encode()).hexdigest()


# Set dictionary of all hash functions
hash_functions = [sha256, sha3, swifft_mock]


quantum_exponents = {
    sha256: 0.5, # Grover's algorithm is faster by O(N^0.5) compared to Classical (O(N))
    sha3: 0.9, # O(N^0.9) versus (O(N)), very quantum resistent
    swifft_mock: 1.0 # O(N) versus O(N), extremely quantum resistent 
}

def hash_meets_difficulty(hex_hash, difficulty_bits):
    binary = bin(int(hex_hash, 16))[2:].zfill(256)
    return binary.startswith('0' * difficulty_bits)


def classical_sha256_mining(data, difficulty_bits):
    nonce = 0
    start = time.time()
    while True:
        h = sha256(data + str(nonce))
        if hash_meets_difficulty(h, difficulty_bits):
            return nonce, time.time() - start
        nonce += 1

# Grover's takes about square root guesses compared to classical miner
def quantum_sha256_estimate(classical_nonce):
    return int(classical_nonce ** 0.5)

def classical_multi_hash_mining(data, difficulty_bits):
    nonce = 0
    start = time.time()
    while True:
        d1 = data + str(nonce)
        d2 = data + str(nonce + 1)
        chosen = random.sample(hash_functions, 2)
        h1 = chosen[0](d1)
        h2 = chosen[1](d2)
        if hash_meets_difficulty(h1, difficulty_bits) and hash_meets_difficulty(h2, difficulty_bits):
            return nonce, time.time() - start, chosen
        nonce += 1

def quantum_multi_hash_estimate(classical_nonce, selected_funcs):
    avg_exp = sum([quantum_exponents[f] for f in selected_funcs]) / 2
    return int(classical_nonce ** avg_exp)

def run_simulation(difficulty):
    print(f"\nSimulation at Difficulty {difficulty}")

    # SHA-256 Only
    c_nonce_sha, c_time_sha = classical_sha256_mining("blockdata", difficulty)
    q_nonce_sha = quantum_sha256_estimate(c_nonce_sha)
    print("\nSHA-256 Only")
    print(f"Classical: nonce = {c_nonce_sha}, time = {c_time_sha:.2f}s")
    print(f"Quantum Estimate: {q_nonce_sha}, speedup = {c_nonce_sha / q_nonce_sha:.2f}x")

    # Multi-Hash (2-of-3)
    c_nonce_multi, c_time_multi, selected = classical_multi_hash_mining("blockdata", difficulty)
    q_nonce_multi = quantum_multi_hash_estimate(c_nonce_multi, selected)
    print("\nMulti-Hash (2-of-3)")
    print(f"Classical: nonce = {c_nonce_multi}, time = {c_time_multi:.2f}s")
    print(f"Hashes Used: {[f.__name__ for f in selected]}")
    print(f"Quantum Estimate: {q_nonce_multi}, speedup = {c_nonce_multi / q_nonce_multi:.2f}x")

# Should be adjusted from 1-10, anything higher is harder on computer
run_simulation(1)