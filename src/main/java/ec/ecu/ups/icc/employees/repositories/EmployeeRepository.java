package ec.ecu.ups.icc.employees.repositories;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

import ec.ecu.ups.icc.employees.entities.Employee;

public interface EmployeeRepository extends JpaRepository<Employee, Long> {

    List<Employee> findByDepartmentIdAndActive(Long departmentId, String active);

    List<Employee> findByDepartmentCompanyIdAndSalaryGreaterThanEqualAndActive(Long companyId, Double salary,
            String active);
}
