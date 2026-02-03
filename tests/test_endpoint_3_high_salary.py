"""
Test Endpoint 3: GET /api/companies/{id}/high-salary-employees
Validación completa del endpoint con todos los casos posibles
Puntaje total: 1.5 puntos
"""

import requests
from typing import Dict, Any

BASE_URL = "http://localhost:8080"
ENDPOINT = f"{BASE_URL}/api/companies"


class TestEndpoint3HighSalary:
    """Tests para el Endpoint 3: Obtener empleados con salario alto"""
    
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
    
    def validate_employees_response_dto_structure(self, data: Dict[str, Any]) -> tuple[bool, str]:
        """Valida la estructura completa del EmployeesResponseDto"""
        errors = []
        
        # Validar campos principales
        required_fields = ['companyName', 'minSalary', 'count', 'employees']
        for field in required_fields:
            if field not in data:
                errors.append(f"Campo requerido '{field}' no encontrado")
        
        # Validar tipos de datos
        if 'companyName' in data and not isinstance(data['companyName'], str):
            errors.append(f"Campo 'companyName' debe ser str, recibido: {type(data['companyName']).__name__}")
        
        if 'minSalary' in data and not isinstance(data['minSalary'], (int, float)):
            errors.append(f"Campo 'minSalary' debe ser number, recibido: {type(data['minSalary']).__name__}")
        
        if 'count' in data and not isinstance(data['count'], int):
            errors.append(f"Campo 'count' debe ser int, recibido: {type(data['count']).__name__}")
        
        # Validar estructura de employees (List<EmployeeWithDepartmentDto>)
        if 'employees' in data:
            employees = data['employees']
            if not isinstance(employees, list):
                errors.append(f"Campo 'employees' debe ser array, recibido: {type(employees).__name__}")
            else:
                for idx, emp in enumerate(employees):
                    if not isinstance(emp, dict):
                        errors.append(f"Employee[{idx}] debe ser objeto")
                        continue
                    
                    emp_fields = ['id', 'firstName', 'lastName', 'email', 'salary', 'department']
                    for field in emp_fields:
                        if field not in emp:
                            errors.append(f"Employee[{idx}].{field} no encontrado")
                    
                    if 'id' in emp and not isinstance(emp['id'], int):
                        errors.append(f"Employee[{idx}].id debe ser int")
                    if 'salary' in emp and not isinstance(emp['salary'], (int, float)):
                        errors.append(f"Employee[{idx}].salary debe ser number")
                    
                    # Validar estructura de department (DepartmentSimpleDto)
                    if 'department' in emp:
                        dept = emp['department']
                        if not isinstance(dept, dict):
                            errors.append(f"Employee[{idx}].department debe ser objeto")
                        else:
                            dept_fields = ['id', 'name']
                            for field in dept_fields:
                                if field not in dept:
                                    errors.append(f"Employee[{idx}].department.{field} no encontrado")
        
        return len(errors) == 0, "; ".join(errors) if errors else "Estructura válida"
    
    def test_01_default_min_salary_5000(self):
        """
        Caso 1: Salario mínimo por defecto (5000)
        Validar: 200 OK, estructura DTO correcta, minSalary=5000, empleados filtrados
        Puntaje: 0.25 puntos
        """
        company_id = 1  # TechCorp
        response = requests.get(f"{ENDPOINT}/{company_id}/high-salary-employees")
        
        try:
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            
            data = response.json()
            
            # Validar estructura del DTO
            is_valid, message = self.validate_employees_response_dto_structure(data)
            assert is_valid, f"Estructura DTO inválida: {message}"
            
            # Validar valores específicos
            assert data['companyName'] == "TechCorp", f"Expected companyName='TechCorp', got {data['companyName']}"
            assert data['minSalary'] == 5000.0, f"Expected minSalary=5000.0, got {data['minSalary']}"
            
            # Todos los empleados deben tener salario >= 5000
            for emp in data['employees']:
                assert emp['salary'] >= 5000.0, \
                    f"Empleado {emp['firstName']} {emp['lastName']} tiene salario {emp['salary']} < 5000"
            
            # Validar count coincide con tamaño de lista
            assert data['count'] == len(data['employees']), \
                f"Count {data['count']} no coincide con tamaño de lista {len(data['employees'])}"
            
            # TechCorp tiene varios empleados con salario >= 5000
            # Engineering: John (5500), Jane (6200), Alice (7500), Robert (6500), Emily (5800)
            # Marketing: Sarah (4800) NO, Mike (5200) SI, David (5600) SI
            # HR: Jennifer (5000) SI, Christopher (4500) NO
            # Finance: Jessica (6800), Matthew (6500), Ashley (5800)
            # Total esperado: al menos 11 empleados
            assert data['count'] >= 11, f"Expected at least 11 employees, got {data['count']}"
            
            print("✓ Test 1 PASSED: Salario mínimo por defecto funciona correctamente")
            self.test_results.append(True)
        except AssertionError as e:
            print(f"✗ Test 1 FAILED: {str(e)}")
            self.test_results.append(False)
            raise
    
    def test_02_custom_min_salary(self):
        """
        Caso 2: Salario mínimo personalizado (6000)
        Validar: 200 OK, minSalary=6000, solo empleados con salary >= 6000
        Puntaje: 0.25 puntos
        """
        company_id = 1  # TechCorp
        min_salary = 6000.0
        response = requests.get(f"{ENDPOINT}/{company_id}/high-salary-employees?minSalary={min_salary}")
        
        try:
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            
            data = response.json()
            
            # Validar estructura
            is_valid, message = self.validate_employees_response_dto_structure(data)
            assert is_valid, f"Estructura DTO inválida: {message}"
            
            # Validar minSalary
            assert data['minSalary'] == min_salary, f"Expected minSalary={min_salary}, got {data['minSalary']}"
            
            # Todos los empleados deben tener salario >= 6000
            for emp in data['employees']:
                assert emp['salary'] >= min_salary, \
                    f"Empleado {emp['firstName']} {emp['lastName']} tiene salario {emp['salary']} < {min_salary}"
            
            # TechCorp con salary >= 6000: Jane (6200), Alice (7500), Robert (6500), Emily (5800) NO
            # Jessica (6800), Matthew (6500)
            # Total esperado: al menos 5 empleados
            assert data['count'] >= 5, f"Expected at least 5 employees with salary >= {min_salary}, got {data['count']}"
            
            print("✓ Test 2 PASSED: Salario mínimo personalizado funciona correctamente")
            self.test_results.append(True)
        except AssertionError as e:
            print(f"✗ Test 2 FAILED: {str(e)}")
            self.test_results.append(False)
            raise
    
    def test_03_descending_order_by_salary(self):
        """
        Caso 3: Validar orden descendente por salario
        Validar: Empleados ordenados de mayor a menor salario
        Puntaje: 0.25 puntos
        """
        company_id = 1  # TechCorp
        response = requests.get(f"{ENDPOINT}/{company_id}/high-salary-employees?minSalary=5000")
        
        try:
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            
            data = response.json()
            
            # Extraer salarios
            salaries = [emp['salary'] for emp in data['employees']]
            
            # Validar orden descendente
            assert salaries == sorted(salaries, reverse=True), \
                f"Empleados no están ordenados descendentemente por salario: {salaries}"
            
            # Validar que el primero tiene el salario más alto
            if len(salaries) > 0:
                assert salaries[0] == max(salaries), \
                    f"Primer empleado no tiene el salario más alto: {salaries[0]} vs {max(salaries)}"
            
            print("✓ Test 3 PASSED: Orden descendente por salario es correcto")
            self.test_results.append(True)
        except AssertionError as e:
            print(f"✗ Test 3 FAILED: {str(e)}")
            self.test_results.append(False)
            raise
    
    def test_04_no_employees_match_criteria(self):
        """
        Caso 4: Sin empleados que cumplan el criterio (salario muy alto)
        Validar: 200 OK, employees=[], count=0
        Puntaje: 0.25 puntos
        """
        company_id = 1  # TechCorp
        min_salary = 100000.0  # Muy alto, nadie cumple
        response = requests.get(f"{ENDPOINT}/{company_id}/high-salary-employees?minSalary={min_salary}")
        
        try:
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            
            data = response.json()
            
            # Validar estructura
            is_valid, message = self.validate_employees_response_dto_structure(data)
            assert is_valid, f"Estructura DTO inválida: {message}"
            
            # Validar que no hay empleados
            assert data['count'] == 0, f"Expected count=0, got {data['count']}"
            assert len(data['employees']) == 0, f"Expected empty list, got {len(data['employees'])} employees"
            assert data['employees'] == [], "La lista de empleados debe estar vacía"
            
            print("✓ Test 4 PASSED: Sin empleados que cumplan retorna lista vacía")
            self.test_results.append(True)
        except AssertionError as e:
            print(f"✗ Test 4 FAILED: {str(e)}")
            self.test_results.append(False)
            raise
    
    def test_05_company_not_found(self):
        """
        Caso 5: Empresa no existe
        Validar: 404 NOT FOUND, mensaje de error
        Puntaje: 0.25 puntos
        """
        company_id = 999  # No existe
        response = requests.get(f"{ENDPOINT}/{company_id}/high-salary-employees")
        
        try:
            assert response.status_code == 404, f"Expected 404, got {response.status_code}"
            
            data = response.json()
            assert 'message' in data, "Response debe contener campo 'message'"
            assert 'not found' in data['message'].lower() or 'inactive' in data['message'].lower(), \
                f"Mensaje debe indicar 'not found' o 'inactive', recibido: {data['message']}"
            
            print("✓ Test 5 PASSED: Empresa no encontrada retorna 404")
            self.test_results.append(True)
        except AssertionError as e:
            print(f"✗ Test 5 FAILED: {str(e)}")
            self.test_results.append(False)
            raise
    
    def test_06_company_inactive(self):
        """
        Caso 6: Empresa está inactiva
        Validar: 404 NOT FOUND
        Puntaje: 0.25 puntos
        """
        company_id = 3  # GlobalSystems - empresa inactiva
        response = requests.get(f"{ENDPOINT}/{company_id}/high-salary-employees")
        
        try:
            assert response.status_code == 404, f"Expected 404 for inactive company, got {response.status_code}"
            
            data = response.json()
            assert 'message' in data, "Response debe contener campo 'message'"
            
            print("✓ Test 6 PASSED: Empresa inactiva retorna 404")
            self.test_results.append(True)
        except AssertionError as e:
            print(f"✗ Test 6 FAILED: {str(e)}")
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
        print("EJECUTANDO TESTS - ENDPOINT 3: GET /api/companies/{id}/high-salary-employees")
        print("=" * 80)
        print()
    
    test_class = TestEndpoint3HighSalary()
    
    # Ejecutar todos los tests
    tests = [
        test_class.test_01_default_min_salary_5000,
        test_class.test_02_custom_min_salary,
        test_class.test_03_descending_order_by_salary,
        test_class.test_04_no_employees_match_criteria,
        test_class.test_05_company_not_found,
        test_class.test_06_company_inactive,
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
    # Puede ejecutarse con: python test_endpoint_3_high_salary.py
    try:
        score, total_points, passed, total = run_all_tests(show_output=True)
        exit(0 if score == TestEndpoint3HighSalary.TOTAL_POINTS else 1)
    except Exception as e:
        print(f"\nERROR CRÍTICO: {str(e)}")
        exit(1)
