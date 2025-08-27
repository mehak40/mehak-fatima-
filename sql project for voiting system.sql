CREATE DATABASE CANDIDATE;
USE CANDIDATE;

-- Table: Users (Voters & Admins)
CREATE TABLE Users (
    User_ID INT PRIMARY KEY,
    FullName VARCHAR(100),
    Email VARCHAR(100) UNIQUE,
    PasswordHash VARCHAR(255),
	Role ENUM('admin', 'voter') DEFAULT 'voter',
    HasVoted BOOLEAN DEFAULT FALSE
);

-- Table: Candidates
CREATE TABLE Candidates (
    Candidate_ID INT PRIMARY KEY,
    FullName VARCHAR(100),
    Party VARCHAR(50),
    Symbol VARCHAR(50)
);

-- Table: Elections
CREATE TABLE Elections (
    Election_ID INT PRIMARY KEY,
    ElectionName VARCHAR(100),
    StartDate DATE,
    EndDate DATE,
    IsActive BOOLEAN DEFAULT TRUE
);

-- Table: Votes
CREATE TABLE Votes (
    VoteID INT PRIMARY KEY AUTO_INCREMENT,
    UserID INT,
    CandidateID INT,
    ElectionID INT,
    VoteDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (User_ID) REFERENCES Users(User_ID),
    FOREIGN KEY (Candidate_ID) REFERENCES Candidates(Candidate_ID),
    FOREIGN KEY (Election_ID) REFERENCES Elections(Election_ID)
);