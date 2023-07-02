
const Web3 = require('web3');

const web3 = new Web3('https://rpc-mumbai.matic.today');
const contractAddress = '{{ contract_data["0x818F7FF1375C59dCB3A8B47E21128d2EF1d45Bcc"] }}';
const contractABI = JSON.parse('{{ contract_data["[{"inputs": [{"internalType": "uint256","name": "_id","type": "uint256"},{"internalType": "string","name": "_name","type": "string"},{"internalType": "string","name": "_party","type": "string"},{"internalType": "string","name": "_imageUri","type": "string"}],"name": "addCandidate","outputs": [],"stateMutability": "nonpayable","type": "function"},{"inputs": [{"internalType": "uint256","name": "_id","type": "uint256"},{"internalType": "string","name": "_name","type": "string"},{"internalType": "uint256","name": "_cnic","type": "uint256"},{"internalType": "uint256","name": "_qr","type": "uint256"}],"name": "addVoter","outputs": [],"stateMutability": "nonpayable","type": "function"},{"inputs": [],"name": "startElection","outputs": [],"stateMutability": "nonpayable","type": "function"},{"inputs": [],"name": "stopElection","outputs": [],"stateMutability": "nonpayable","type": "function"},{"inputs": [],"stateMutability": "nonpayable","type": "constructor"},{"inputs": [{"internalType": "uint256","name": "_candidateId","type": "uint256"},{"internalType": "uint256","name": "_voterId","type": "uint256"}],"name": "vote","outputs": [],"stateMutability": "nonpayable","type": "function"},{"inputs": [],"name": "candidateCount","outputs": [{"internalType": "uint256","name": "","type": "uint256"}],"stateMutability": "view","type": "function"},{"inputs": [],"name": "electionStarted","outputs": [{"internalType": "bool","name": "","type": "bool"}],"stateMutability": "view","type": "function"},{"inputs": [{"internalType": "uint256","name": "_id","type": "uint256"}],"name": "getCandidateDetailsByID","outputs": [{"internalType": "uint256","name": "","type": "uint256"},{"internalType": "string","name": "","type": "string"},{"internalType": "string","name": "","type": "string"},{"internalType": "string","name": "","type": "string"},{"internalType": "uint256","name": "","type": "uint256"}],"stateMutability": "view","type": "function"},{"inputs": [],"name": "getResult","outputs": [{"components": [{"internalType": "uint256","name": "id","type": "uint256"},{"internalType": "string","name": "name","type": "string"},{"internalType": "string","name": "party","type": "string"},{"internalType": "string","name": "imageUri","type": "string"},{"internalType": "uint256","name": "votes","type": "uint256"}],"internalType": "struct Voting.Candidate[]","name": "","type": "tuple[]"}],"stateMutability": "view","type": "function"},{"inputs": [],"name": "owner","outputs": [{"internalType": "address","name": "","type": "address"}],"stateMutability": "view","type": "function"},{"inputs": [],"name": "totalVotes","outputs": [{"internalType": "uint256","name": "","type": "uint256"}],"stateMutability": "view","type": "function"},{"inputs": [],"name": "voterCount","outputs": [{"internalType": "uint256","name": "","type": "uint256"}],"stateMutability": "view","type": "function"}]"] | tojson }}');

const contract = new web3.eth.Contract(contractABI, contractAddress);

// Function to start the election
async function startElection() {
    // Check if MetaMask is installed
    if (typeof window.ethereum !== 'undefined') {
        // Request access to the user's accounts
        await window.ethereum.enable();

        // Get the selected account
        const accounts = await window.ethereum.request({ method: 'eth_accounts' });
        const selectedAccount = accounts[0];

        // Confirm the transaction
        const result = await contract.methods.startElection().send({ from: selectedAccount });

        // Handle the transaction confirmation
        if (result.status) {
            alert('Election started successfully!');
        } else {
            alert('Error occurred while starting the election!');
        }
    } else {
        alert('MetaMask is not installed!');
    }
}

// Attach the startElection function to the "Start Election" button
const startElectionButton = document.getElementById('start-election-button');
startElectionButton.addEventListener('click', startElection);

