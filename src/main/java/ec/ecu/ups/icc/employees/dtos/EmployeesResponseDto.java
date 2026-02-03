package ec.ecu.ups.icc.employees.dtos;

import java.math.BigDecimal;
import java.util.List;

public class EmployeesResponseDto {
    private String companyName;
    private Double minSalary;
    private Integer count;
    private List<EmployeeWithDeptDto> employees;

    public String getCompanyName() {
        return companyName;
    }

    public void setCompanyName(String companyName) {
        this.companyName = companyName;
    }

    public Double getMinSalary() {
        return minSalary;
    }

    public void setMinSalary(Double minSalary) {
        this.minSalary = minSalary;
    }

    public Integer getCount() {
        return count;
    }

    public void setCount(Integer count) {
        this.count = count;
    }

    public List<EmployeeWithDeptDto> getEmployees() {
        return employees;
    }

    public void setEmployees(List<EmployeeWithDeptDto> employees) {
        this.employees = employees;
    }

    public static class EmployeeWithDeptDto {
        private Long id;
        private String firstName;
        private String lastName;
        private String email;
        private BigDecimal salary;
        private DeptDto department;

        public Long getId() {
            return id;
        }

        public void setId(Long id) {
            this.id = id;
        }

        public String getFirstName() {
            return firstName;
        }

        public void setFirstName(String firstName) {
            this.firstName = firstName;
        }

        public String getLastName() {
            return lastName;
        }

        public void setLastName(String lastName) {
            this.lastName = lastName;
        }

        public String getEmail() {
            return email;
        }

        public void setEmail(String email) {
            this.email = email;
        }

        public BigDecimal getSalary() {
            return salary;
        }

        public void setSalary(BigDecimal salary) {
            this.salary = salary;
        }

        public DeptDto getDepartment() {
            return department;
        }

        public void setDepartment(DeptDto department) {
            this.department = department;
        }
    }

    public static class DeptDto {
        private Long id;
        private String name;

        public Long getId() {
            return id;
        }

        public void setId(Long id) {
            this.id = id;
        }

        public String getName() {
            return name;
        }

        public void setName(String name) {
            this.name = name;
        }
    }
}