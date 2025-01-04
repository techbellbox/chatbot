CREATE TABLE VoterDetails (
    voter_id INT PRIMARY KEY AUTO_INCREMENT,  -- Auto-incremented primary key
    voter_name VARCHAR(255) COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,  -- Voter name with utf8mb4 collation
    mobile_number VARCHAR(20) COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,  -- Mobile number with utf8mb4 collation
    constituency VARCHAR(255) COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,  -- Constituency with utf8mb4 collation
    gender VARCHAR(50) COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,  -- Gender with utf8mb4 collation
    marital_status VARCHAR(50) COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,  -- Marital status with utf8mb4 collation
    education_qualification VARCHAR(255) COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,  -- Education qualification with utf8mb4 collation
    schemes TEXT COLLATE utf8mb4_0900_ai_ci DEFAULT NULL  -- Schemes column with utf8mb4 collation
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
