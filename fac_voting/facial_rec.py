import os
import face_recognition
from web3 import Web3
import cv2
# Ethereum smart contract setup
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
contract_address = '0xe8937e73b65a1D03070C82BFE98FdE442bF65a41'  # Replace with your contract's address
contract_abi = [
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_name",
				"type": "string"
			}
		],
		"name": "addCandidate",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "checkElectionPeriod",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "resetAllVotersStatus",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string[]",
				"name": "_candidates",
				"type": "string[]"
			},
			{
				"internalType": "uint256",
				"name": "_votingDuration",
				"type": "uint256"
			}
		],
		"name": "startElection",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_voter",
				"type": "address"
			}
		],
		"name": "verifyVoter",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_id",
				"type": "uint256"
			}
		],
		"name": "voteTo",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "candidates",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "id",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "name",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "numbersofVotes",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "electionStarted",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "electionTimer",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "listofVoters",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "owner",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "retrieveVotes",
		"outputs": [
			{
				"components": [
					{
						"internalType": "uint256",
						"name": "id",
						"type": "uint256"
					},
					{
						"internalType": "string",
						"name": "name",
						"type": "string"
					},
					{
						"internalType": "uint256",
						"name": "numbersofVotes",
						"type": "uint256"a
					}
				],
				"internalType": "struct Voting.Candidate[]",
				"name": "",
				"type": "tuple[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "verifiedVoters",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "voters",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_voter",
				"type": "address"
			}
		],
		"name": "voterStatus",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "votingEnd",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "votingStart",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]# Replace with your contract's ABI
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Known face encodings (In a real scenario, this would be more dynamic and robust)
known_faces = {
    
}

# Function to find a match in the unknown folder
def find_match(unknown_folder, known_faces):
    for filename in os.listdir(unknown_folder):
        if filename.endswith(('png', 'jpg', 'jpeg', 'gif')):
            unknown_image = face_recognition.load_image_file(os.path.join(unknown_folder, filename))
            unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
            
            for name, known_encoding in known_faces.items():
                results = face_recognition.compare_faces([known_encoding], unknown_encoding)
                if True in results:
                    return name
    return None

# Load known faces dynamically from the 'known' folder
def load_known_faces(known_folder):
    known_faces = {}
    for filename in os.listdir(known_folder):
        if filename.endswith(('png', 'jpg', 'jpeg', 'gif')):
            name = os.path.splitext(filename)[0]  # Use filename (excluding extension) as the name
            known_image = face_recognition.load_image_file(os.path.join(known_folder, filename))
            known_encoding = face_recognition.face_encodings(known_image)[0]
            known_faces[name] = known_encoding
    return known_faces
def capture_image(camera_index=0, save_path='unknown/captured_image.jpg'):
    # Open the camera
    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # Capture a single frame
    ret, frame = cap.read()

    # Save the captured image to the 'unknown' folder
    if ret:
        cv2.imwrite(save_path, frame)
        print(f"Image captured and saved to {save_path}")
    else:
        print("Error: Could not capture image.")

    # Release the camera
    cap.release()

if __name__ == "__main__":
    # Assuming 'known' folder is inside the 'fac_voting' directory
    # Capture an image and save it to the 'unknown' folder
    capture_image(camera_index=0, save_path='unknown/captured_image.jpg')

    # Load known faces dynamically from the 'known' folder
    known_folder = 'known'
    known_faces = load_known_faces(known_folder)

    # Replace with the path to your 'unknown' folder
    unknown_folder = 'unknown'

    # Facial recognition and updating verification status
    matched_face = find_match(unknown_folder, known_faces)
    if matched_face:
        # Call the smart contract function to verify the voter

        voter_address = '0xB7B34F2F6f808221d9e2f355ABF22d3Eb3aD4AB7'  # Replace with the Ethereum address of the voter
        txn = contract.functions.verifyVoter(voter_address).buildTransaction({
            'from': voter_address,  # The transaction is now sent from the second account
            'nonce': w3.eth.getTransactionCount(voter_address),  # Fetching the nonce for the second account
            'gas': 2000000  # Gas limit
        })

        # Sign and send the transaction
        private_key = '0x4aff28b8a4d5a2386c10c717f38699ac8d9ff7e291f4a5ca658b6f8d7d5b2a5f'  # Replace with the private key for the account
        signed_txn = w3.eth.account.signTransaction(txn, private_key)
        txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

        print(f"Verification transaction sent. Transaction hash: {txn_hash.hex()}")

    else:
        print("No match found.")