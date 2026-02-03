"""
Test Endpoint 2: GET /api/companies/{id}/departments
Validación completa del endpoint con todos los casos posibles
Puntaje total: 1.5 puntos
"""

import requests
from typing import Dict, Any

BASE_URL = "http://localhost:8080"
ENDPOINT = f"{BASE_URL}/api/companies"


class TestEndpoint2Companies:
    """Tests para el Endpoint 2: Obtener departamentos de una empresa"""
    
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
    
    def validate_company_departments_dto_structure(self, data: Dict[str, Any]) -> tuple[bool, str]:
        """Valida la estructura completa del CompanyDepartmentsDto"""
        errors = []
        
        # Validar campos principales
        required_fields = ['companyId', 'companyName', 'country', 'departmentCount', 'departments', 'totalBudget']
        for field in required_fields:
            if field not in data:
                errors.append(f"Campo requerido '{field}' no encontrado")
        
        # Validar tipos de datos
        if 'companyId' in data and not isinstance(data['companyId'], int):
            errors.append(f"Campo 'companyId' debe ser int, recibido: {type(data['companyId']).__name__}")
        
        if 'companyName' in data and not isinstance(data['companyName'], str):
            errors.append(f"Campo 'companyName' debe ser str, recibido: {type(data['companyName']).__name__}")
        
        if 'country' in data and not isinstance(data['country'], str):
            errors.append(f"Campo 'country' debe ser str, recibido: {type(data['country']).__name__}")
        
        if 'departmentCount' in data and not isinstance(data['departmentCount'], int):
            errors.append(f"Campo 'departmentCount' debe ser int, recibido: {type(data['departmentCount']).__name__}")
        
        if 'totalBudget' in data and not isinstance(data['totalBudget'], (int, float)):
            errors.append(f"Campo 'totalBudget' debe ser number, recibido: {type(data['totalBudget']).__name__}")
        
        # Validar estructura de departments (List<DepartmentWithCountDto>)
        if 'departments' in data:
            departments = data['departments']
            if not isinstance(departments, list):
                errors.append(f"Campo 'departments' debe ser array, recibido: {type(departments).__name__}")
            else:
                for idx, dept in enumerate(departments):
                    if not isinstance(dept, dict):
                        errors.append(f"Department[{idx}] debe ser objeto")
                        continue
                    
                    dept_fields = ['id', 'name', 'budget', 'employeeCount']
                    for field in dept_fields:
                        if field not in dept:
                            errors.append(f"Department[{idx}].{field} no encontrado")
                    
                    if 'id' in dept and not isinstance(dept['id'], int):
                        errors.append(f"Department[{idx}].id debe ser int")
                    if 'name' in dept and not isinstance(dept['name'], str):
                        errors.append(f"Department[{idx}].name debe ser str")
                    if 'budget' in dept and not isinstance(dept['budget'], (int, float)):
                        errors.append(f"Department[{idx}].budget debe ser number")
                    if 'employeeCount' in dept and not isinstance(dept['employeeCount'], int):
                        errors.append(f"Department[{idx}].employeeCount debe ser int")
        
        return len(errors) == 0, "; ".join(errors) if errors else "Estructura válida"
    
    def test_01_company_with_departments(self):
        """
        Caso 1: Empresa existe con departamentos activos
        Validar: 200 OK, estructura DTO correcta, solo departamentos activos
        Puntaje: 0.25 puntos
        """
        company_id = 1  # TechCorp
        response = requests.get(f"{ENDPOINT}/{company_id}/departments")
        
        try:
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            
            data = response.json()
            
            # Validar estructura del DTO
            is_valid, message = self.validate_company_departments_dto_structure(data)
            assert is_valid, f"Estructura DTO inválida: {message}"
            
            # Validar valores específicos de TechCorp
            assert data['companyId'] == 1, f"Expected companyId=1, got {data['companyId']}"
            assert data['companyName'] == "TechCorp", f"Expected companyName='TechCorp', got {data['companyName']}"
            assert data['country'] == "USA", f"Expected country='USA', got {data['country']}"
            
            # TechCorp tiene 4 departamentos activos (Engineering, Marketing, HR, Finance)
            # Sales (id=5) está inactivo, no debe incluirse
            assert data['departmentCount'] == 4, f"Expected 4 departments, got {data['departmentCount']}"
            assert len(data['departments']) == 4, f"Expected 4 departments in list, got {len(data['departments'])}"
            
            # Validar IDs de departamentos (deben ser 1, 2, 3, 4)
            dept_ids = [dept['id'] for dept in data['departments']]
            expected_ids = [1, 2, 3, 4]
            assert set(dept_ids) == set(expected_ids), f"Expected dept IDs {expected_ids}, got {dept_ids}"
            
            # Validar totalBudget (250000 + 150000 + 100000 + 180000 = 680000)
            expected_total_budget = 680000.0
            assert data['totalBudget'] == expected_total_budget, \
                f"Expected totalBudget={expected_total_budget}, got {data['totalBudget']}"
            
            print("✓ Test 1 PASSED: Empresa con departamentos activos retorna correctamente")
            self.test_results.append(True)
        except AssertionError as e:
            print(f"✗ Test 1 FAILED: {str(e)}")
            self.test_results.append(False)
            raise
    
    def test_02_validate_department_employee_counts(self):
        """
        Caso 2: Validar conteo de empleados por departamento
        Validar: employeeCount solo incluye empleados activos
        Puntaje: 0.25 puntos
        """
        company_id = 1  # TechCorp
        response = requests.get(f"{ENDPOINT}/{company_id}/departments")
        
        try:
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            
            data = response.json()
            
            # Validar employeeCount específicos de cada departamento
            # Engineering (1): 5 empleados activos
            # Marketing (2): 3 empleados activos
            # Human Resources (3): 2 empleados activos
            # Finance (4): 3 empleados activos
            
            expected_counts = {
                1: 5,  # Engineering
                2: 3,  # Marketing
                3: 2,  # Human Resources
                4: 3   # Finance
            }
            
            for dept in data['departments']:
                dept_id = dept['id']
                if dept_id in expected_counts:
                    expected_count = expected_counts[dept_id]
                    assert dept['employeeCount'] == expected_count, \
                        f"Department {dept['name']} (ID {dept_id}) expected {expected_count} employees, got {dept['employeeCount']}"
            
            print("✓ Test 2 PASSED: Conteo de empleados por departamento es correcto")
            self.test_results.append(True)
        except AssertionError as e:
            print(f"✗ Test 2 FAILED: {str(e)}")
            self.test_results.append(False)
            raise
    
    def test_03_company_not_found(self):
        """
        Caso 3: Empresa no existe
        Validar: 404 NOT FOUND, mensaje de error
        Puntaje: 0.25 puntos
        """
        company_id = 999  # No existe
        response = requests.get(f"{ENDPOINT}/{company_id}/departments")
        
        try:
            assert response.status_code == 404, f"Expected 404, got {response.status_code}"
            
            data = response.json()
            assert 'message' in data, "Response debe contener campo 'message'"
            assert 'not found' in data['message'].lower() or 'inactive' in data['message'].lower(), \
                f"Mensaje debe indicar 'not found' o 'inactive', recibido: {data['message']}"
            
            print("✓ Test 3 PASSED: Empresa no encontrada retorna 404")
            self.test_results.append(True)
        except AssertionError as e:
            print(f"✗ Test 3 FAILED: {str(e)}")
            self.test_results.append(False)
            raise
    
    def test_04_company_inactive(self):
        """
        Caso 4: Empresa está inactiva
        Validar: 404 NOT FOUND
        Puntaje: 0.25 puntos
        """
        company_id = 3  # GlobalSystems - empresa inactiva
        response = requests.get(f"{ENDPOINT}/{company_id}/departments")
        
        try:
            assert response.status_code == 404, f"Expected 404 for inactive company, got {response.status_code}"
            
            data = response.json()
            assert 'message' in data, "Response debe contener campo 'message'"
            
            print("✓ Test 4 PASSED: Empresa inactiva retorna 404")
            self.test_results.append(True)
        except AssertionError as e:
            print(f"✗ Test 4 FAILED: {str(e)}")
            self.test_results.append(False)
            raise
    
    def test_05_validate_total_budget_calculation(self):
        """
        Caso 5: Validar cálculo correcto de totalBudget
        Validar: La suma manual de budgets coincide con totalBudget
        Puntaje: 0.25 puntos
        """
        company_id = 2  # InnovateLabs
        response = requests.get(f"{ENDPOINT}/{company_id}/departments")
        
        try:
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            
            data = response.json()
            
            # Calcular suma manual de budgets
            manual_sum = sum(dept['budget'] for dept in data['departments'])
            
            assert data['totalBudget'] == manual_sum, \
                f"TotalBudget {data['totalBudget']} no coincide con suma manual {manual_sum}"
            
            # Validar departmentCount
            assert data['departmentCount'] == len(data['departments']), \
                f"DepartmentCount {data['departmentCount']} no coincide con tamaño de lista {len(data['departments'])}"
            
            print("✓ Test 5 PASSED: Cálculo de totalBudget es correcto")
            self.test_results.append(True)
        except AssertionError as e:
            print(f"✗ Test 5 FAILED: {str(e)}")
            self.test_results.append(False)
            raise
    
    def test_06_multiple_companies(self):
        """
        Caso 6: Validar múltiples empresas diferentes
        Validar: Cada empresa retorna sus propios departamentos
        Puntaje: 0.25 puntos
        """
        test_companies = [
            {'id': 1, 'name': 'TechCorp', 'country': 'USA', 'min_depts': 4},
            {'id': 2, 'name': 'InnovateLabs', 'country': 'Canada', 'min_depts': 3},
            {'id': 4, 'name': 'DataMinds', 'country': 'Germany', 'min_depts': 2},
        ]
        
        try:
            for company in test_companies:
                response = requests.get(f"{ENDPOINT}/{company['id']}/departments")
                assert response.status_code == 200, f"Company {company['id']} failed with {response.status_code}"
                
                data = response.json()
                assert data['companyId'] == company['id'], f"Expected company id {company['id']}"
                assert data['companyName'] == company['name'], f"Expected company name {company['name']}"
                assert data['country'] == company['country'], f"Expected country {company['country']}"
                assert data['departmentCount'] >= company['min_depts'], \
                    f"Expected at least {company['min_depts']} departments"
            
            print("✓ Test 6 PASSED: Múltiples empresas retornan datos correctos")
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
        print("EJECUTANDO TESTS - ENDPOINT 2: GET /api/companies/{id}/departments")
        print("=" * 80)
        print()
    
    test_class = TestEndpoint2Companies()
    
    # Ejecutar todos los tests
    tests = [
        test_class.test_01_company_with_departments,
        test_class.test_02_validate_department_employee_counts,
        test_class.test_03_company_not_found,
        test_class.test_04_company_inactive,
        test_class.test_05_validate_total_budget_calculation,
        test_class.test_06_multiple_companies,
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
    # Puede ejecutarse con: python test_endpoint_2_companies.py
    try:
        score, total_points, passed, total = run_all_tests(show_output=True)
        exit(0 if score == TestEndpoint2Companies.TOTAL_POINTS else 1)
    except Exception as e:
        print(f"\nERROR CRÍTICO: {str(e)}")
        exit(1)
