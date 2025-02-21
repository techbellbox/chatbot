CREATE TABLE IF NOT EXISTS Employee_Details (
    EMPLOYEE_ID INT PRIMARY KEY,
    FIRST_NAME VARCHAR(255),
    LAST_NAME VARCHAR(255),
    EMAIL VARCHAR(255),
    PHONE_NUMBER VARCHAR(255),
    HIRE_DATE VARCHAR(255),
    JOB_ID VARCHAR(255),
    SALARY INT,
    COMMISSION_PCT VARCHAR(255),
    MANAGER_ID VARCHAR(255),
    DEPARTMENT_ID INT
);