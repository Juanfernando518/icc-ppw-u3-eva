package ec.ecu.ups.icc.employees.repositories;

import java.util.List;
import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;

import ec.ecu.ups.icc.employees.entities.Department;

public interface DepartmentRepository extends JpaRepository<Department, Long> {
    Optional<Department> findByIdAndActive(Long id, String active);

    List<Department> findByCompanyIdAndActive(Long companyId, String active);
}
