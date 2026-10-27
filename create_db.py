import sqlite3

def init_company_db():
    conn = sqlite3.connect("company.db")
    cur = conn.cursor()

    # Enable foreign keys in SQLite
    cur.execute("PRAGMA foreign_keys = ON;")

    # 1. Create Tables
    cur.executescript("""
    DROP TABLE IF EXISTS DEPENDENT;
    DROP TABLE IF EXISTS WORKS_ON;
    DROP TABLE IF EXISTS PROJECT;
    DROP TABLE IF EXISTS EMPLOYEE;
    DROP TABLE IF EXISTS DEPARTMENT;

    CREATE TABLE DEPARTMENT (
        Dnumber INTEGER PRIMARY KEY,
        Dname TEXT NOT NULL,
        Mgr_ssn TEXT
    );

    CREATE TABLE EMPLOYEE (
        SSN TEXT PRIMARY KEY,
        Fname TEXT NOT NULL,
        Lname TEXT NOT NULL,
        Salary REAL,
        Dno INTEGER,
        FOREIGN KEY (Dno) REFERENCES DEPARTMENT(Dnumber)
    );

    CREATE TABLE PROJECT (
        Pnumber INTEGER PRIMARY KEY,
        Pname TEXT NOT NULL,
        Plocation TEXT,
        Dnum INTEGER,
        FOREIGN KEY (Dnum) REFERENCES DEPARTMENT(Dnumber)
    );

    CREATE TABLE WORKS_ON (
        Essn TEXT,
        Pno INTEGER,
        Hours REAL,
        PRIMARY KEY (Essn, Pno),
        FOREIGN KEY (Essn) REFERENCES EMPLOYEE(SSN),
        FOREIGN KEY (Pno) REFERENCES PROJECT(Pnumber)
    );

    CREATE TABLE DEPENDENT (
        Essn TEXT,
        Dependent_name TEXT,
        Relationship TEXT,
        PRIMARY KEY (Essn, Dependent_name),
        FOREIGN KEY (Essn) REFERENCES EMPLOYEE(SSN)
    );
    """)

    # 2. Insert Departments (Mgr_ssn will be updated after inserting employees)
    departments = [
        (1, 'Headquarters', None),
        (4, 'Administration', None),
        (5, 'Research', None)
    ]
    cur.executemany("INSERT INTO DEPARTMENT (Dnumber, Dname, Mgr_ssn) VALUES (?, ?, ?);", departments)

    # 3. Insert Employees
    # Includes edge cases: NULL salary, low salary, high work hours, no project, no dependents
    employees = [
        ('123456789', 'John', 'Smith', 30000.0, 5),
        ('333445555', 'Franklin', 'Wong', 40000.0, 5),
        ('999887777', 'Alicia', 'Zelaya', 25000.0, 4),
        ('987654321', 'Jennifer', 'Wallace', 43000.0, 4),
        ('666884444', 'Ramesh', 'Narayan', 38000.0, 5),
        ('453453453', 'Joyce', 'English', 25000.0, 5),
        ('987987987', 'Ahmad', 'Jabbar', 25000.0, 4),
        ('888665555', 'James', 'Borg', 55000.0, 1),
        ('111223333', 'Hoang', 'Pham', None, 4),           # NULL salary edge case (Question p)
        ('222334444', 'Linh', 'Tran', 28000.0, 5),         # No project & no dependents (Question t)
        ('777889999', 'Minh', 'Doan', 60000.0, 5)          # High earner for comparison checks
    ]
    cur.executemany("INSERT INTO EMPLOYEE (SSN, Fname, Lname, Salary, Dno) VALUES (?, ?, ?, ?, ?);", employees)

    # Update Department Managers
    cur.execute("UPDATE DEPARTMENT SET Mgr_ssn = '888665555' WHERE Dnumber = 1;")
    cur.execute("UPDATE DEPARTMENT SET Mgr_ssn = '987654321' WHERE Dnumber = 4;")
    cur.execute("UPDATE DEPARTMENT SET Mgr_ssn = '333445555' WHERE Dnumber = 5;")

    # 4. Insert Projects
    # Includes Dept 5 projects, low hours (< 5 hours), and unstaffed project
    projects = [
        (1, 'ProductX', 'Bellaire', 5),
        (2, 'ProductY', 'Sugarland', 5),
        (3, 'ProductZ', 'Houston', 5),
        (10, 'Computerization', 'Stafford', 4),
        (20, 'Reorganization', 'Houston', 1),
        (30, 'Newbenefits', 'Stafford', 4),
        (99, 'AbandonedProject', 'Bellaire', 5)  # 0 hours / no employees (Question s)
    ]
    cur.executemany("INSERT INTO PROJECT (Pnumber, Pname, Plocation, Dnum) VALUES (?, ?, ?, ?);", projects)

    # 5. Insert Works_On
    # Includes high hours (>40h total for Question q), low hours (<5h total for Question s)
    works_on = [
        ('123456789', 1, 32.5),
        ('123456789', 2, 10.0),   # Total 42.5 hours (> 40h)
        ('333445555', 2, 10.0),
        ('333445555', 3, 10.0),
        ('333445555', 10, 10.0),
        ('333445555', 20, 10.0),
        ('999887777', 30, 3.0),   # Total on Project 30 is < 5 hours
        ('987654321', 30, 1.0),   # Project 30 total: 4.0 hours (Question s)
        ('987654321', 20, 15.0),
        ('666884444', 3, 40.0),
        ('453453453', 1, 20.0),
        ('453453453', 2, 20.0),
        ('987987987', 10, 35.0),
        ('888665555', 20, 0.0),
        ('333445555', 1, 5.0)     # Franklin Wong works on all Dept 5 projects (1, 2, 3) (Question j)
    ]
    cur.executemany("INSERT INTO WORKS_ON (Essn, Pno, Hours) VALUES (?, ?, ?);", works_on)

    # 6. Insert Dependents
    dependents = [
        ('333445555', 'Alice', 'Daughter'),
        ('333445555', 'Theodore', 'Son'),
        ('333445555', 'Joy', 'Spouse'),
        ('987654321', 'Abner', 'Spouse'),
        ('123456789', 'Michael', 'Son'),
        ('123456789', 'Alice', 'Daughter'),
        ('123456789', 'Elizabeth', 'Spouse')
    ]
    cur.executemany("INSERT INTO DEPENDENT (Essn, Dependent_name, Relationship) VALUES (?, ?, ?);", dependents)

    conn.commit()
    conn.close()
    print("Database 'company.db' successfully created.")

if __name__ == "__main__":
    init_company_db()