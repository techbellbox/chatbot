CREATE TABLE VoterDetails (
    VoterName VARCHAR(100) NOT NULL,
    MobileNumber VARCHAR(15) UNIQUE NOT NULL,
    Constituency VARCHAR(100) NOT NULL,
    Gender ENUM('Male', 'Female', 'Other') NOT NULL,
    MaritalStatus ENUM('Single', 'Married', 'Widowed', 'Divorced') NOT NULL,
    EducationQualification VARCHAR(50) NOT NULL,
    Schemes TEXT
);
