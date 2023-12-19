import os
import face_recognition
from web3 import Web3

# Ethereum smart contract setup
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
contract_address = '0xYourContractAddress'  # Replace with your contract's address
contract_abi = 'YourContractABI'            # Replace with your contract's ABI
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Known face encodings (In a real scenario, this would be more dynamic and robust)
known_faces = {
    "Alice": face_recognition.load_image_file("path_to_alice_image.jpg"),
    # Add more known faces here
}

# Function to find a match in the unknown folder
def find_match(unknown_folder):
    for filename in os.listdir(unknown_folder):
        if filename.endswith(('png', 'jpg', 'jpeg', 'gif')):
            unknown_image = face_recognition.load_image_file(os.path.join(unknown_folder, filename))
            unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

            for name, known_encoding in known_faces.items():
                results = face_recognition.compare_faces([known_encoding], unknown_encoding)
                if True in results:
                    return name
    return None

# Replace with the path to your 'unknown' folder
unknown_folder = 'path_to_unknown_folder'

# Facial recognition and updating verification status
matched_face = find_match(unknown_folder)
if matched_face:
    print(f"Match found: {matched_face}")
    
    # Call the smart contract function to verify the voter
    voter_address = '0xVoterEthereumAddress'  # Replace with the Ethereum address of the voter
    txn = contract.functions.verifyVoter(voter_address).buildTransaction({
        'from': w3.eth.accounts[0],  # Using the first account from Ganache
        'nonce': w3.eth.getTransactionCount(w3.eth.accounts[0]),
        'gas': 2000000  # Set appropriate gas limit
    })

    # Sign and send the transaction
    private_key = '0xYourPrivateKey'  # Replace with the private key for the account
    signed_txn = w3.eth.account.signTransaction(txn, private_key)
    txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

    print(f"Verification transaction sent. Transaction hash: {txn_hash.hex()}")

    # Example: Voting for candidate with ID 1 after successful verification
    candidate_id = 1
    vote_txn = contract.functions.voteTo(candidate_id).buildTransaction({
        'from': voter_address,
        'nonce': w3.eth.getTransactionCount(voter_address),
        'gas': 2000000  # Set appropriate gas limit
    })

    # Sign and send the vote transaction
    signed_vote_txn = w3.eth.account.signTransaction(vote_txn, private_key)
    vote_txn_hash = w3.eth.sendRawTransaction(signed_vote_txn.rawTransaction)

    print(f"Vote transaction sent. Transaction hash: {vote_txn_hash.hex()}")
else:
    print("No match found.")

# Note: This script is a simplified example and may need modifications based on your specific requirements.
