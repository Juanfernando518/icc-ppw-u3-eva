package ec.ecu.ups.icc.employees.dtos;

import java.math.BigDecimal;
import java.util.List;

public class CompanyDepartmentsDto {
    private Long companyId;
    private String companyName;
    private String country;
    private Integer departmentCount;
    private List<DeptSummaryDto> departments;
    private BigDecimal totalBudget;

    public Long getCompanyId() {
        return companyId;
    }

    public void setCompanyId(Long companyId) {
        this.companyId = companyId;
    }

    public String getCompanyName() {
        return companyName;
    }

    public void setCompanyName(String companyName) {
        this.companyName = companyName;
    }

    public String getCountry() {
        return country;
    }

    public void setCountry(String country) {
        this.country = country;
    }

    public Integer getDepartmentCount() {
        return departmentCount;
    }

    public void setDepartmentCount(Integer departmentCount) {
        this.departmentCount = departmentCount;
    }

    public List<DeptSummaryDto> getDepartments() {
        return departments;
    }

    public void setDepartments(List<DeptSummaryDto> departments) {
        this.departments = departments;
    }

    public BigDecimal getTotalBudget() {
        return totalBudget;
    }

    public void setTotalBudget(BigDecimal totalBudget) {
        this.totalBudget = totalBudget;
    }

    public static class DeptSummaryDto {
        private Long id;
        private String name;
        private BigDecimal budget;
        private Integer employeeCount;

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

        public BigDecimal getBudget() {
            return budget;
        }

        public void setBudget(BigDecimal budget) {
            this.budget = budget;
        }

        public Integer getEmployeeCount() {
            return employeeCount;
        }

        public void setEmployeeCount(Integer employeeCount) {
            this.employeeCount = employeeCount;
        }
    }
}