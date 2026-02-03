"""
Test Endpoint 1: GET /api/departments/{id}/employees
Validación completa del endpoint con todos los casos posibles
Puntaje total: 2.0 puntos
"""

import requests
# import pytest
from typing import Dict, Any

BASE_URL = "http://localhost:8080"
ENDPOINT = f"{BASE_URL}/api/departments"


class TestEndpoint1Departments:
    """Tests para el Endpoint 1: Obtener departamento con sus empleados"""
    
    # Configuración de puntajes
    TOTAL_POINTS = 2.0
    test_results = []
    
    @classmethod
    def calculate_score(cls):
        """Calcula el puntaje final basado en tests pasados"""
        passed = sum(1 for result in cls.test_results if result)
        total = len(cls.test_results)
        if total == 0:
            return 0.0
        score = (passed / total) * cls.TOTAL_POINTS
        return round(score, 2)
    
    def validate_department_dto_structure(self, data: Dict[str, Any]) -> tuple[bool, str]:
        """Valida la estructura completa del DepartmentWithEmployeesDto"""
        errors = []
        
        # Validar campos principales
        required_fields = ['id', 'name', 'budget', 'company', 'employees', 'employeeCount', 'totalSalaries']
        for field in required_fields:
            if field not in data:
                errors.append(f"Campo requerido '{field}' no encontrado")
        
        # Validar tipos de datos
        if 'id' in data and not isinstance(data['id'], int):
            errors.append(f"Campo 'id' debe ser int, recibido: {type(data['id']).__name__}")
        
        if 'name' in data and not isinstance(data['name'], str):
            errors.append(f"Campo 'name' debe ser str, recibido: {type(data['name']).__name__}")
        
        if 'budget' in data and not isinstance(data['budget'], (int, float)):
            errors.append(f"Campo 'budget' debe ser number, recibido: {type(data['budget']).__name__}")
        
        if 'employeeCount' in data and not isinstance(data['employeeCount'], int):
            errors.append(f"Campo 'employeeCount' debe ser int, recibido: {type(data['employeeCount']).__name__}")
        
        if 'totalSalaries' in data and not isinstance(data['totalSalaries'], (int, float)):
            errors.append(f"Campo 'totalSalaries' debe ser number, recibido: {type(data['totalSalaries']).__name__}")
        
        # Validar estructura de company (CompanyDto)
        if 'company' in data:
            company = data['company']
            if not isinstance(company, dict):
                errors.append(f"Campo 'company' debe ser objeto, recibido: {type(company).__name__}")
            else:
                company_fields = ['id', 'name', 'country']
                for field in company_fields:
                    if field not in company:
                        errors.append(f"Campo 'company.{field}' no encontrado")
                
                if 'id' in company and not isinstance(company['id'], int):
                    errors.append(f"Campo 'company.id' debe ser int")
                if 'name' in company and not isinstance(company['name'], str):
                    errors.append(f"Campo 'company.name' debe ser str")
                if 'country' in company and not isinstance(company['country'], str):
                    errors.append(f"Campo 'company.country' debe ser str")
        
        # Validar estructura de employees (List<EmployeeSimpleDto>)
        if 'employees' in data:
            employees = data['employees']
            if not isinstance(employees, list):
                errors.append(f"Campo 'employees' debe ser array, recibido: {type(employees).__name__}")
            else:
                for idx, emp in enumerate(employees):
                    if not isinstance(emp, dict):
                        errors.append(f"Empleado[{idx}] debe ser objeto")
                        continue
                    
                    emp_fields = ['id', 'firstName', 'lastName', 'email', 'salary']
                    for field in emp_fields:
                        if field not in emp:
                            errors.append(f"Empleado[{idx}].{field} no encontrado")
                    
                    if 'id' in emp and not isinstance(emp['id'], int):
                        errors.append(f"Empleado[{idx}].id debe ser int")
                    if 'salary' in emp and not isinstance(emp['salary'], (int, float)):
                        errors.append(f"Empleado[{idx}].salary debe ser number")
        
        return len(errors) == 0, "; ".join(errors) if errors else "Estructura válida"
    
    def test_01_department_exists_default_order_desc(self):
        """
        Caso 1: Departamento existe, orden por defecto (desc)
        Validar: 200 OK, estructura DTO correcta, orden descendente por salario
        Puntaje: 0.25 puntos
        """
        department_id = 1  # Engineering - TechCorp
        response = requests.get(f"{ENDPOINT}/{department_id}/employees")
        
        try:
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            
            data = response.json()
            
            # Validar estructura del DTO
            is_valid, message = self.validate_department_dto_structure(data)
            assert is_valid, f"Estructura DTO inválida: {message}"
            
            # Validar valores específicos del departamento 1
            assert data['id'] == 1, f"Expected id=1, got {data['id']}"
            assert data['name'] == "Engineering", f"Expected name='Engineering', got {data['name']}"
            assert data['budget'] == 250000.0, f"Expected budget=250000.0, got {data['budget']}"
            
            # Validar company
            assert data['company']['id'] == 1, "Company id debe ser 1"
            assert data['company']['name'] == "TechCorp", "Company name debe ser TechCorp"
            assert data['company']['country'] == "USA", "Company country debe ser USA"
            
            # Validar empleados activos (5 empleados: IDs 1, 2, 3, 4, 5)
            assert data['employeeCount'] == 5, f"Expected 5 employees, got {data['employeeCount']}"
            assert len(data['employees']) == 5, f"Expected 5 employees in list, got {len(data['employees'])}"
            
            # Validar orden descendente por salario (default)
            salaries = [emp['salary'] for emp in data['employees']]
            assert salaries == sorted(salaries, reverse=True), f"Empleados no están ordenados descendentemente: {salaries}"
            
            # Validar suma de salarios (5500 + 6200 + 7500 + 5800 + 6500 = 31500)
            expected_total = 31500.0
            assert data['totalSalaries'] == expected_total, f"Expected totalSalaries={expected_total}, got {data['totalSalaries']}"
            
            # Validar que los salarios esperados están presentes
            expected_salaries = [7500.0, 6500.0, 6200.0, 5800.0, 5500.0]
            assert salaries == expected_salaries, f"Salarios esperados {expected_salaries}, obtenidos {salaries}"
            
            print("✓ Test 1 PASSED: Departamento existe con orden descendente por defecto")
            self.test_results.append(True)
        except AssertionError as e:
            print(f"✗ Test 1 FAILED: {str(e)}")
            self.test_results.append(False)
            raise
    
    def test_02_department_exists_order_asc(self):
        """
        Caso 2: Departamento existe, orden ascendente explícito
        Validar: 200 OK, orden ascendente por salario
        Puntaje: 0.25 puntos
        """
        department_id = 1
        response = requests.get(f"{ENDPOINT}/{department_id}/employees?sort=asc")
        
        try:
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            
            data = response.json()
            
            # Validar estructura
            is_valid, message = self.validate_department_dto_structure(data)
            assert is_valid, f"Estructura DTO inválida: {message}"
            
            # Validar orden ascendente
            salaries = [emp['salary'] for emp in data['employees']]
            assert salaries == sorted(salaries), f"Empleados no están ordenados ascendentemente: {salaries}"
            
            # Validar salarios esperados en orden ascendente
            expected_salaries = [5500.0, 5800.0, 6200.0, 6500.0, 7500.0]
            assert salaries == expected_salaries, f"Salarios esperados {expected_salaries}, obtenidos {salaries}"
            
            print("✓ Test 2 PASSED: Orden ascendente funciona correctamente")
            self.test_results.append(True)
        except AssertionError as e:
            print(f"✗ Test 2 FAILED: {str(e)}")
            self.test_results.append(False)
            raise
    
    def test_03_department_not_found(self):
        """
        Caso 3: Departamento no existe
        Validar: 404 NOT FOUND, mensaje de error
        Puntaje: 0.25 puntos
        """
        department_id = 999  # No existe
        response = requests.get(f"{ENDPOINT}/{department_id}/employees")
        
        try:
            assert response.status_code == 404, f"Expected 404, got {response.status_code}"
            
            data = response.json()
            assert 'message' in data, "Response debe contener campo 'message'"
            assert 'not found' in data['message'].lower() or 'inactive' in data['message'].lower(), \
                f"Mensaje debe indicar 'not found' o 'inactive', recibido: {data['message']}"
            
            print("✓ Test 3 PASSED: Departamento no encontrado retorna 404")
            self.test_results.append(True)
        except AssertionError as e:
            print(f"✗ Test 3 FAILED: {str(e)}")
            self.test_results.append(False)
            raise
    
    def test_04_department_inactive(self):
        """
        Caso 4: Departamento está inactivo
        Validar: 404 NOT FOUND
        Puntaje: 0.25 puntos
        """
        department_id = 5  # Sales - departamento inactivo
        response = requests.get(f"{ENDPOINT}/{department_id}/employees")
        
        try:
            assert response.status_code == 404, f"Expected 404 for inactive department, got {response.status_code}"
            
            data = response.json()
            assert 'message' in data, "Response debe contener campo 'message'"
            
            print("✓ Test 4 PASSED: Departamento inactivo retorna 404")
            self.test_results.append(True)
        except AssertionError as e:
            print(f"✗ Test 4 FAILED: {str(e)}")
            self.test_results.append(False)
            raise
    
    def test_05_department_without_employees(self):
        """
        Caso 5: Departamento activo sin empleados activos
        Validar: 200 OK, employees=[], employeeCount=0, totalSalaries=0.0
        Puntaje: 0.25 puntos
        """
        department_id = 9  # Operations - GlobalSystems - departamento sin empleados activos
        response = requests.get(f"{ENDPOINT}/{department_id}/employees")
        
        try:
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            
            data = response.json()
            
            # Validar estructura del DTO
            is_valid, message = self.validate_department_dto_structure(data)
            assert is_valid, f"Estructura DTO inválida: {message}"
            
            # Validar valores específicos del departamento 9
            assert data['id'] == 9, f"Expected id=9, got {data['id']}"
            assert data['name'] == "Operations", f"Expected name='Operations', got {data['name']}"
            assert data['budget'] == 150000.0, f"Expected budget=150000.0, got {data['budget']}"
            
            # Validar company
            assert data['company']['id'] == 3, "Company id debe ser 3"
            assert data['company']['name'] == "GlobalSystems", "Company name debe ser GlobalSystems"
            assert data['company']['country'] == "UK", "Company country debe ser UK"
            
            # Validar que NO tiene empleados activos
            assert data['employeeCount'] == 0, f"Expected 0 employees, got {data['employeeCount']}"
            assert len(data['employees']) == 0, f"Expected empty employee list, got {len(data['employees'])}"
            assert data['employees'] == [], "La lista de empleados debe estar vacía"
            
            # Validar suma de salarios debe ser 0
            assert data['totalSalaries'] == 0.0, f"Expected totalSalaries=0.0, got {data['totalSalaries']}"
            
            print("✓ Test 5 PASSED: Departamento sin empleados activos retorna correctamente")
            self.test_results.append(True)
        except AssertionError as e:
            print(f"✗ Test 5 FAILED: {str(e)}")
            self.test_results.append(False)
            raise
    
    def test_06_validate_employee_fields(self):
        """
        Caso 6: Validar todos los campos de empleados
        Validar: Cada empleado tiene firstName, lastName, email, salary correctos
        Puntaje: 0.25 puntos
        """
        department_id = 1
        response = requests.get(f"{ENDPOINT}/{department_id}/employees")
        
        try:
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            
            data = response.json()
            employees = data['employees']
            
            # Validar que cada empleado tiene todos los campos
            for idx, emp in enumerate(employees):
                assert 'id' in emp and emp['id'] > 0, f"Employee[{idx}] debe tener id válido"
                assert 'firstName' in emp and len(emp['firstName']) > 0, f"Employee[{idx}] debe tener firstName"
                assert 'lastName' in emp and len(emp['lastName']) > 0, f"Employee[{idx}] debe tener lastName"
                assert 'email' in emp and '@' in emp['email'], f"Employee[{idx}] debe tener email válido"
                assert 'salary' in emp and emp['salary'] > 0, f"Employee[{idx}] debe tener salary > 0"
            
            # Validar empleados específicos esperados del departamento Engineering
            employee_ids = [emp['id'] for emp in employees]
            expected_ids = [1, 2, 3, 4, 5]  # IDs de empleados activos en Engineering
            assert set(employee_ids) == set(expected_ids), f"Expected employee IDs {expected_ids}, got {employee_ids}"
            
            print("✓ Test 6 PASSED: Todos los campos de empleados son válidos")
            self.test_results.append(True)
        except AssertionError as e:
            print(f"✗ Test 6 FAILED: {str(e)}")
            self.test_results.append(False)
            raise
    
    def test_07_validate_total_salaries_calculation(self):
        """
        Caso 7: Validar cálculo correcto de totalSalaries
        Validar: La suma manual de salarios coincide con totalSalaries
        Puntaje: 0.25 puntos
        """
        department_id = 2  # Marketing - 3 empleados
        response = requests.get(f"{ENDPOINT}/{department_id}/employees")
        
        try:
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            
            data = response.json()
            
            # Calcular suma manual
            manual_sum = sum(emp['salary'] for emp in data['employees'])
            
            assert data['totalSalaries'] == manual_sum, \
                f"TotalSalaries {data['totalSalaries']} no coincide con suma manual {manual_sum}"
            
            # Validar employeeCount
            assert data['employeeCount'] == len(data['employees']), \
                f"EmployeeCount {data['employeeCount']} no coincide con tamaño de lista {len(data['employees'])}"
            
            print("✓ Test 7 PASSED: Cálculo de totalSalaries es correcto")
            self.test_results.append(True)
        except AssertionError as e:
            print(f"✗ Test 7 FAILED: {str(e)}")
            self.test_results.append(False)
            raise
    
    def test_08_different_departments(self):
        """
        Caso 8: Validar múltiples departamentos diferentes
        Validar: Cada departamento retorna sus propios datos correctamente
        Puntaje: 0.25 puntos
        """
        test_departments = [
            {'id': 1, 'name': 'Engineering', 'company': 'TechCorp', 'min_employees': 5},
            {'id': 2, 'name': 'Marketing', 'company': 'TechCorp', 'min_employees': 3},
            {'id': 6, 'name': 'Research', 'company': 'InnovateLabs', 'min_employees': 3},
        ]
        
        try:
            for dept in test_departments:
                response = requests.get(f"{ENDPOINT}/{dept['id']}/employees")
                assert response.status_code == 200, f"Dept {dept['id']} failed with {response.status_code}"
                
                data = response.json()
                assert data['id'] == dept['id'], f"Expected dept id {dept['id']}"
                assert data['name'] == dept['name'], f"Expected dept name {dept['name']}"
                assert data['company']['name'] == dept['company'], f"Expected company {dept['company']}"
                assert data['employeeCount'] >= dept['min_employees'], \
                    f"Expected at least {dept['min_employees']} employees"
            
            print("✓ Test 8 PASSED: Múltiples departamentos retornan datos correctos")
            self.test_results.append(True)
        except AssertionError as e:
            print(f"✗ Test 8 FAILED: {str(e)}")
            self.test_results.append(False)
            raise


def run_all_tests(show_output=True):
    """
    Ejecuta todos los tests y muestra el resumen de puntaje
    
    Args:
        show_output: Si es True, imprime el resumen completo. Si es False, solo retorna el puntaje.
    
    Returns:
        tuple: (score, total_points, passed, total_tests)
    """
    if show_output:
        print("=" * 80)
        print("EJECUTANDO TESTS - ENDPOINT 1: GET /api/departments/{id}/employees")
        print("=" * 80)
        print()
    
    test_class = TestEndpoint1Departments()
    
    # Ejecutar todos los tests
    tests = [
        test_class.test_01_department_exists_default_order_desc,
        test_class.test_02_department_exists_order_asc,
        test_class.test_03_department_not_found,
        test_class.test_04_department_inactive,
        test_class.test_05_department_without_employees,
        test_class.test_06_validate_employee_fields,
        test_class.test_07_validate_total_salaries_calculation,
        test_class.test_08_different_departments,
    ]
    
    for idx, test in enumerate(tests, 1):
        if show_output:
            print(f"\n--- Test {idx}/{len(tests)}: {test.__doc__.strip().split('Caso')[1].split('Validar')[0].strip()} ---")
        try:
            test()
        except Exception as e:
            if show_output:
                print(f"ERROR: {str(e)}")
    
    # Calcular y mostrar puntaje final
    passed = sum(1 for result in test_class.test_results if result)
    total = len(test_class.test_results)
    score = test_class.calculate_score()
    
    if show_output:
        print("\n" + "=" * 80)
        print("RESUMEN DE RESULTADOS")
        print("=" * 80)
        
        print(f"Tests ejecutados: {total}")
        print(f"Tests aprobados: {passed}")
        print(f"Tests fallidos: {total - passed}")
        print(f"\nPUNTAJE FINAL: {score} / {test_class.TOTAL_POINTS} puntos")
        print("=" * 80)
    
    return score, test_class.TOTAL_POINTS, passed, total


if __name__ == "__main__":
    # Puede ejecutarse con: python test_endpoint_1_departments.py
    # o con pytest: pytest test_endpoint_1_departments.py -v
    try:
        score, total_points, passed, total = run_all_tests(show_output=True)
        exit(0 if score == TestEndpoint1Departments.TOTAL_POINTS else 1)
    except Exception as e:
        print(f"\nERROR CRÍTICO: {str(e)}")
        exit(1)
