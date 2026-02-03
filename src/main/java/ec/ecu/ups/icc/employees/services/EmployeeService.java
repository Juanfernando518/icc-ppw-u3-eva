package ec.ecu.ups.icc.employees.services;

import java.math.BigDecimal;
import java.util.Comparator;
import java.util.List;
import java.util.stream.Collectors;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import ec.ecu.ups.icc.employees.dtos.*;
import ec.ecu.ups.icc.employees.entities.*;
import ec.ecu.ups.icc.employees.repositories.*;

@Service
public class EmployeeService {
    @Autowired
    private CompanyRepository companyRepository;
    @Autowired
    private DepartmentRepository departmentRepository;
    @Autowired
    private EmployeeRepository employeeRepository;

    public DepartmentWithEmployeesDto getDepartmentEmployees(Long deptId, String sort) {
        Department dept = departmentRepository.findByIdAndActive(deptId, "S")
                .orElseThrow(() -> new RuntimeException("Department not found"));

        DepartmentWithEmployeesDto dto = new DepartmentWithEmployeesDto();
        dto.setId(dept.getId());
        dto.setName(dept.getName());
        dto.setBudget(dept.getBudget());

        List<Employee> activeEmployees = dept.getEmployees().stream()
                .filter(e -> e.getActive() != null && String.valueOf(e.getActive()).equalsIgnoreCase("S"))
                .collect(Collectors.toList());

        if (sort != null && sort.equalsIgnoreCase("asc")) {
            activeEmployees.sort(Comparator.comparing(Employee::getSalary));
        } else {
            activeEmployees.sort(Comparator.comparing(Employee::getSalary).reversed());
        }

        dto.setEmployees(activeEmployees.stream().map(e -> {
            DepartmentWithEmployeesDto.EmployeeDto ed = new DepartmentWithEmployeesDto.EmployeeDto();
            ed.setId(e.getId());
            ed.setFirstName(e.getFirstName());
            ed.setSalary(e.getSalary());
            return ed;
        }).collect(Collectors.toList()));

        dto.setEmployeeCount(activeEmployees.size());
        dto.setTotalSalaries(
                activeEmployees.stream().map(Employee::getSalary).reduce(BigDecimal.ZERO, BigDecimal::add));
        return dto;
    }

    public CompanyDepartmentsDto getCompanyDepartments(Long companyId) {
        Company company = companyRepository.findByIdAndActive(companyId, "S")
                .orElseThrow(() -> new RuntimeException("Company not found"));

        List<Department> activeDepts = departmentRepository.findByCompanyIdAndActive(companyId, "S");

        CompanyDepartmentsDto dto = new CompanyDepartmentsDto();
        dto.setCompanyId(company.getId());
        dto.setCompanyName(company.getName());
        dto.setDepartments(activeDepts.stream().map(d -> {
            CompanyDepartmentsDto.DeptSummaryDto ds = new CompanyDepartmentsDto.DeptSummaryDto();
            ds.setId(d.getId());
            ds.setName(d.getName());
            ds.setBudget(d.getBudget());
            return ds;
        }).collect(Collectors.toList()));
        return dto;
    }

    public EmployeesResponseDto getHighSalaryEmployees(Long companyId, Double minSalary) {
        companyRepository.findByIdAndActive(companyId, "S")
                .orElseThrow(() -> new RuntimeException("Company not found"));

        List<Employee> highSalaryEmps = employeeRepository
                .findByDepartmentCompanyIdAndSalaryGreaterThanEqualAndActive(companyId, minSalary, "S");

        EmployeesResponseDto dto = new EmployeesResponseDto();
        dto.setCount(highSalaryEmps.size());
        return dto;
    }
}