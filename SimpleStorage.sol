// SPDX-License-Identifier: MIT


pragma solidity 0.8.9;

contract SimpleStorage {

    uint256 public favouriteNumber;
    bool favouriteBool;
    bool favouriteBool2;

    struct People{
        uint256 favouriteNumber;
        string name;
    }

    People[] public people;

    mapping(string => uint256) public nameToFavouriteNumber;

    People public person = People({favouriteNumber : 3, name: "oluwatobiloba"});

     function store(uint256 _favouriteNumber) public returns(uint256) {
        favouriteNumber = _favouriteNumber;
        return _favouriteNumber;
    }

    function addPerson(string memory _name, uint256 _favouriteNumber) public {
        people.push(People(_favouriteNumber, _name));
        nameToFavouriteNumber[_name] = _favouriteNumber;
    }

    function retrieve() public view returns(uint256) {
        return favouriteNumber;
    }
}