package ec.ecu.ups.icc.employees.controllers;

import ec.ecu.ups.icc.employees.dtos.*;
import ec.ecu.ups.icc.employees.services.EmployeeService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api")
public class EmployeeController {

    @Autowired
    private EmployeeService employeeService;

    @GetMapping("/departments/{id}/employees")
    public ResponseEntity<DepartmentWithEmployeesDto> getDeptEmployees(
            @PathVariable Long id,
            @RequestParam(defaultValue = "desc") String sort) {
        return ResponseEntity.ok(employeeService.getDepartmentEmployees(id, sort));
    }

    @GetMapping("/companies/{id}/departments")
    public ResponseEntity<CompanyDepartmentsDto> getCompanyDepts(@PathVariable Long id) {
        return ResponseEntity.ok(employeeService.getCompanyDepartments(id));
    }

    @GetMapping("/companies/{id}/high-salary-employees")
    public ResponseEntity<EmployeesResponseDto> getHighSalary(
            @PathVariable Long id,
            @RequestParam(defaultValue = "5000") Double minSalary) {
        return ResponseEntity.ok(employeeService.getHighSalaryEmployees(id, minSalary));
    }
}
