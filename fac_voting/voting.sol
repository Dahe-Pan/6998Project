//SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
contract Voting{
    struct Candidate{
        uint256 id;
        string name;
        uint256 numbersofVotes;
    }

    Candidate[] public candidates;
    address public owner;
    mapping(address => bool) public voters;
    address[] public listofVoters;
    uint256 public votingStart;
    uint256 public votingEnd;
    bool public electionStarted;
    mapping(address => bool) public verifiedVoters;

    modifier onlyOwner(){
        require(msg.sender == owner, 'only owner can call this function');
        _;
    }
    modifier electionOngoing(){
        require(electionStarted, 'no election is ongoing');
        _;
    }
    constructor(){
        owner = msg.sender;
    }
    function startElection(string[] memory _candidates, uint256 _votingDuration) public onlyOwner{
        require(electionStarted == false, 'election already started');
        delete candidates;
        // resetAllVotersStatus();
        for(uint256 i = 0; i < _candidates.length; i++){
            candidates.push(Candidate({id:i, name:_candidates[i], numbersofVotes:0}));
        }
        electionStarted = true;
        votingStart = block.timestamp;
        votingEnd = block.timestamp + (_votingDuration * 1 minutes);
    }
    function addCandidate(string memory _name) public onlyOwner electionOngoing{
        require(checkElectionPeriod(), 'election period has ended');
        candidates.push(Candidate({id:candidates.length, name:_name, numbersofVotes:0}));
    }
    function voterStatus(address _voter) public view electionOngoing returns(bool){
        if(voters[_voter] == true){
            return true;
        }
        return false;
    }
    function voteTo(uint256 _id) public electionOngoing{
        require(checkElectionPeriod(), 'election period has ended');
        require(!voterStatus(msg.sender), 'you have already voted');
        require(verifiedVoters[msg.sender], 'Voter not verified');
        candidates[_id].numbersofVotes ++;
        voters[msg.sender] = true;
        listofVoters.push(msg.sender);
    }
    function retrieveVotes() public view returns(Candidate[] memory){
        return candidates;
    }
    function electionTimer()   public view electionOngoing returns(uint256){
        if(block.timestamp >= votingEnd){
            return 0;
        }
        return (votingEnd - block.timestamp);
    }
    function checkElectionPeriod() public returns(bool){
        if(electionTimer() > 0){
            return true;
        }
        electionStarted = false;
        return false;
    }
    function resetAllVotersStatus() public onlyOwner{
        for(uint256 i = 0; i < listofVoters.length; i++){
            voters[listofVoters[i]] = false;
        }
        delete listofVoters;
    }
    function verifyVoter(address _voter) public {
    // You should add security checks here, like onlyOwner or a similar modifier
        verifiedVoters[_voter] = true;
    }
}