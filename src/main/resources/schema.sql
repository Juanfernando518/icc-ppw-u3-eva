-- Schema para Evaluación Técnica 3: Relaciones OneToMany y ManyToOne
-- Sistema de Gestión de Recursos Humanos

-- Tabla: companies (independiente)
CREATE TABLE companies (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    country VARCHAR(50) NOT NULL,
    active CHAR(1) DEFAULT 'S' NOT NULL CHECK (active IN ('S', 'N'))
);

-- Tabla: departments (ManyToOne con companies)
CREATE TABLE departments (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    budget DECIMAL(12, 2) NOT NULL,
    company_id BIGINT NOT NULL,
    active CHAR(1) DEFAULT 'S' NOT NULL CHECK (active IN ('S', 'N')),
    CONSTRAINT fk_departments_company FOREIGN KEY (company_id) REFERENCES companies(id)
);

-- Tabla: employees (ManyToOne con departments)
CREATE TABLE employees (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    salary DECIMAL(10, 2) NOT NULL,
    department_id BIGINT NOT NULL,
    active CHAR(1) DEFAULT 'S' NOT NULL CHECK (active IN ('S', 'N')),
    CONSTRAINT fk_employees_department FOREIGN KEY (department_id) REFERENCES departments(id)
);

-- Índices para mejorar performance en consultas
CREATE INDEX idx_departments_company ON departments(company_id);
CREATE INDEX idx_departments_active ON departments(active);
CREATE INDEX idx_employees_department ON employees(department_id);
CREATE INDEX idx_employees_active ON employees(active);
CREATE INDEX idx_employees_email ON employees(email);
