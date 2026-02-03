package ec.ecu.ups.icc.employees.services;

import java.math.BigDecimal;
import java.util.Comparator;
import java.util.List;
import java.util.stream.Collectors;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;
import org.springframework.http.HttpStatus;

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
        // Devuelve 404 si no existe o no está activo
        Department dept = departmentRepository.findByIdAndActive(deptId, "S")
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Department not found"));

        DepartmentWithEmployeesDto dto = new DepartmentWithEmployeesDto();
        dto.setId(dept.getId());
        dto.setName(dept.getName());
        dto.setBudget(dept.getBudget());

        // Llenamos la información de la Company (Arregla el error de NoneType)
        if (dept.getCompany() != null) {
            DepartmentWithEmployeesDto.CompanyDto cDto = new DepartmentWithEmployeesDto.CompanyDto();
            cDto.setId(dept.getCompany().getId());
            cDto.setName(dept.getCompany().getName());
            cDto.setCountry(dept.getCompany().getCountry());
            dto.setCompany(cDto);
        }

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
            ed.setLastName(e.getLastName());
            ed.setEmail(e.getEmail());
            ed.setSalary(e.getSalary());
            return ed;
        }).collect(Collectors.toList()));

        dto.setEmployeeCount(activeEmployees.size());
        dto.setTotalSalaries(activeEmployees.stream()
                .map(Employee::getSalary)
                .reduce(BigDecimal.ZERO, BigDecimal::add));

        return dto;
    }

    public CompanyDepartmentsDto getCompanyDepartments(Long companyId) {
        // Buscamos la empresa (Ya devuelve 404 si no existe gracias al arreglo
        // anterior)
        Company company = companyRepository.findByIdAndActive(companyId, "S")
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Company not found"));

        // Obtenemos departamentos activos
        List<Department> activeDepts = departmentRepository.findByCompanyIdAndActive(companyId, "S");

        CompanyDepartmentsDto dto = new CompanyDepartmentsDto();
        dto.setCompanyId(company.getId());
        dto.setCompanyName(company.getName());

        // ARREGLO: Campos que el test reclama como NoneType
        dto.setCountry(company.getCountry());
        dto.setDepartmentCount(activeDepts.size());

        // ARREGLO: Calcular el presupuesto total de la empresa
        BigDecimal totalBudget = activeDepts.stream()
                .map(Department::getBudget)
                .filter(java.util.Objects::nonNull)
                .reduce(BigDecimal.ZERO, BigDecimal::add);
        dto.setTotalBudget(totalBudget);

        // Mapear los departamentos con su conteo de empleados
        dto.setDepartments(activeDepts.stream().map(d -> {
            CompanyDepartmentsDto.DeptSummaryDto ds = new CompanyDepartmentsDto.DeptSummaryDto();
            ds.setId(d.getId());
            ds.setName(d.getName());
            ds.setBudget(d.getBudget());

            // ARREGLO: El test pide el conteo de empleados por departamento
            long empCount = d.getEmployees().stream()
                    .filter(e -> e.getActive() != null && String.valueOf(e.getActive()).equalsIgnoreCase("S"))
                    .count();
            ds.setEmployeeCount((int) empCount);

            return ds;
        }).collect(Collectors.toList()));

        return dto;
    }

    public EmployeesResponseDto getHighSalaryEmployees(Long companyId, Double minSalary) {
        // 1. Validar empresa
        Company company = companyRepository.findByIdAndActive(companyId, "S")
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Company not found"));

        // 2. Buscar empleados
        List<Employee> highSalaryEmps = employeeRepository
                .findByDepartmentCompanyIdAndSalaryGreaterThanEqualAndActive(companyId, minSalary, "S");

        // 3. Llenar DTO
        EmployeesResponseDto dto = new EmployeesResponseDto();
        dto.setCompanyName(company.getName());
        dto.setMinSalary(minSalary); // Cambiado a Double para que coincida con tu DTO
        dto.setCount(highSalaryEmps.size());

        // 4. Mapear la lista usando EmployeeWithDeptDto (que es la que tienes en tu
        // archivo)
        dto.setEmployees(highSalaryEmps.stream().map(e -> {
            EmployeesResponseDto.EmployeeWithDeptDto ed = new EmployeesResponseDto.EmployeeWithDeptDto();
            ed.setId(e.getId());
            ed.setFirstName(e.getFirstName());
            ed.setLastName(e.getLastName());
            ed.setSalary(e.getSalary());
            ed.setEmail(e.getEmail());

            // Mapear el departamento interno
            EmployeesResponseDto.DeptDto dDto = new EmployeesResponseDto.DeptDto();
            dDto.setId(e.getDepartment().getId());
            dDto.setName(e.getDepartment().getName());
            ed.setDepartment(dDto);

            return ed;
        }).collect(Collectors.toList()));

        return dto;
    }
}