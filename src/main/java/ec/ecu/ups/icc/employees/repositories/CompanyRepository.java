package ec.ecu.ups.icc.employees.repositories;

import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;

import ec.ecu.ups.icc.employees.entities.Company;

public interface CompanyRepository extends JpaRepository<Company, Long> {

    Optional<Company> findByIdAndActive(Long id, String active);
}
