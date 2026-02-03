"""
Test Endpoint 4: PATCH /api/employees/{employeeId}/transfer
Validación completa del endpoint con todos los casos posibles
Puntaje total: 3.0 puntos
"""

import requests
from typing import Dict, Any

BASE_URL = "http://localhost:8080"
ENDPOINT = f"{BASE_URL}/api/employees"


class TestEndpoint4Transfer:
    """Tests para el Endpoint 4: Transferir empleado a otro departamento"""
    
    # Configuración de puntajes
    TOTAL_POINTS = 3.0
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
    
    def validate_transfer_response_dto_structure(self, data: Dict[str, Any]) -> tuple[bool, str]:
        """Valida la estructura completa del EmployeeTransferResponseDto"""
        errors = []
        
        # Validar campos principales
        required_fields = ['employeeId', 'employeeName', 'oldDepartment', 'newDepartment', 'message']
        for field in required_fields:
            if field not in data:
                errors.append(f"Campo requerido '{field}' no encontrado")
        
        # Validar tipos de datos
        if 'employeeId' in data and not isinstance(data['employeeId'], int):
            errors.append(f"Campo 'employeeId' debe ser int, recibido: {type(data['employeeId']).__name__}")
        
        if 'employeeName' in data and not isinstance(data['employeeName'], str):
            errors.append(f"Campo 'employeeName' debe ser str, recibido: {type(data['employeeName']).__name__}")
        
        if 'message' in data and not isinstance(data['message'], str):
            errors.append(f"Campo 'message' debe ser str, recibido: {type(data['message']).__name__}")
        
        # Validar estructura de oldDepartment (DepartmentSimpleDto)
        if 'oldDepartment' in data:
            dept = data['oldDepartment']
            if not isinstance(dept, dict):
                errors.append(f"Campo 'oldDepartment' debe ser objeto, recibido: {type(dept).__name__}")
            else:
                dept_fields = ['id', 'name']
                for field in dept_fields:
                    if field not in dept:
                        errors.append(f"oldDepartment.{field} no encontrado")
                
                if 'id' in dept and not isinstance(dept['id'], int):
                    errors.append("oldDepartment.id debe ser int")
                if 'name' in dept and not isinstance(dept['name'], str):
                    errors.append("oldDepartment.name debe ser str")
        
        # Validar estructura de newDepartment (DepartmentSimpleDto)
        if 'newDepartment' in data:
            dept = data['newDepartment']
            if not isinstance(dept, dict):
                errors.append(f"Campo 'newDepartment' debe ser objeto, recibido: {type(dept).__name__}")
            else:
                dept_fields = ['id', 'name']
                for field in dept_fields:
                    if field not in dept:
                        errors.append(f"newDepartment.{field} no encontrado")
                
                if 'id' in dept and not isinstance(dept['id'], int):
                    errors.append("newDepartment.id debe ser int")
                if 'name' in dept and not isinstance(dept['name'], str):
                    errors.append("newDepartment.name debe ser str")
        
        return len(errors) == 0, "; ".join(errors) if errors else "Estructura válida"
    
    def test_01_successful_transfer(self):
        """
        Caso 1: Transferencia exitosa
        Validar: 200 OK, estructura DTO correcta, transferencia realizada
        Puntaje: 0.375 puntos
        """
        employee_id = 1  # John Doe - Engineering
        transfer_data = {"newDepartmentId": 2}  # Marketing
        
        response = requests.patch(
            f"{ENDPOINT}/{employee_id}/transfer",
            json=transfer_data,
            headers={'Content-Type': 'application/json'}
        )
        
        try:
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            
            data = response.json()
            
            # Validar estructura del DTO
            is_valid, message = self.validate_transfer_response_dto_structure(data)
            assert is_valid, f"Estructura DTO inválida: {message}"
            
            # Validar valores específicos
            assert data['employeeId'] == 1, f"Expected employeeId=1, got {data['employeeId']}"
            assert data['employeeName'] == "John Doe", f"Expected name='John Doe', got {data['employeeName']}"
            
            # Validar departamento antiguo
            assert data['oldDepartment']['id'] == 1, "Old department id debe ser 1 (Engineering)"
            assert data['oldDepartment']['name'] == "Engineering", "Old department debe ser Engineering"
            
            # Validar departamento nuevo
            assert data['newDepartment']['id'] == 2, "New department id debe ser 2 (Marketing)"
            assert data['newDepartment']['name'] == "Marketing", "New department debe ser Marketing"
            
            # Validar mensaje
            assert 'transferred successfully' in data['message'].lower(), \
                f"Message debe indicar 'transferred successfully', recibido: {data['message']}"
            
            print("✓ Test 1 PASSED: Transferencia exitosa funciona correctamente")
            self.test_results.append(True)
        except AssertionError as e:
            print(f"✗ Test 1 FAILED: {str(e)}")
            self.test_results.append(False)
            raise
    
    def test_02_employee_already_in_department(self):
        """
        Caso 2: Empleado ya está en ese departamento
        Validar: 409 CONFLICT, mensaje de error apropiado
        Puntaje: 0.375 puntos
        """
        employee_id = 1  # John Doe - ahora está en Marketing (dept 2)
        transfer_data = {"newDepartmentId": 2}  # Ya está en Marketing
        
        response = requests.patch(
            f"{ENDPOINT}/{employee_id}/transfer",
            json=transfer_data,
            headers={'Content-Type': 'application/json'}
        )
        
        try:
            assert response.status_code == 409, f"Expected 409 CONFLICT, got {response.status_code}"
            
            data = response.json()
            assert 'message' in data, "Response debe contener campo 'message'"
            assert 'already' in data['message'].lower(), \
                f"Mensaje debe indicar 'already', recibido: {data['message']}"
            
            print("✓ Test 2 PASSED: Empleado ya en departamento retorna 409")
            self.test_results.append(True)
        except AssertionError as e:
            print(f"✗ Test 2 FAILED: {str(e)}")
            self.test_results.append(False)
            raise
    
    def test_03_transfer_back_to_original(self):
        """
        Caso 3: Devolver empleado a departamento original
        Validar: 200 OK, transferencia realizada correctamente
        Puntaje: 0.375 puntos
        """
        employee_id = 1  # John Doe - actualmente en Marketing (dept 2)
        transfer_data = {"newDepartmentId": 1}  # Devolver a Engineering
        
        response = requests.patch(
            f"{ENDPOINT}/{employee_id}/transfer",
            json=transfer_data,
            headers={'Content-Type': 'application/json'}
        )
        
        try:
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            
            data = response.json()
            
            # Validar estructura
            is_valid, message = self.validate_transfer_response_dto_structure(data)
            assert is_valid, f"Estructura DTO inválida: {message}"
            
            # Validar transferencia
            assert data['oldDepartment']['id'] == 2, "Old department debe ser Marketing"
            assert data['newDepartment']['id'] == 1, "New department debe ser Engineering"
            
            print("✓ Test 3 PASSED: Devolución a departamento original funciona")
            self.test_results.append(True)
        except AssertionError as e:
            print(f"✗ Test 3 FAILED: {str(e)}")
            self.test_results.append(False)
            raise
    
    def test_04_employee_not_found(self):
        """
        Caso 4: Empleado no existe
        Validar: 404 NOT FOUND, mensaje de error
        Puntaje: 0.375 puntos
        """
        employee_id = 999  # No existe
        transfer_data = {"newDepartmentId": 2}
        
        response = requests.patch(
            f"{ENDPOINT}/{employee_id}/transfer",
            json=transfer_data,
            headers={'Content-Type': 'application/json'}
        )
        
        try:
            assert response.status_code == 404, f"Expected 404, got {response.status_code}"
            
            data = response.json()
            assert 'message' in data, "Response debe contener campo 'message'"
            assert 'not found' in data['message'].lower() or 'inactive' in data['message'].lower(), \
                f"Mensaje debe indicar 'not found' o 'inactive', recibido: {data['message']}"
            
            print("✓ Test 4 PASSED: Empleado no encontrado retorna 404")
            self.test_results.append(True)
        except AssertionError as e:
            print(f"✗ Test 4 FAILED: {str(e)}")
            self.test_results.append(False)
            raise
    
    def test_05_employee_inactive(self):
        """
        Caso 5: Empleado está inactivo
        Validar: 404 NOT FOUND
        Puntaje: 0.375 puntos
        """
        employee_id = 33  # Empleado inactivo
        transfer_data = {"newDepartmentId": 2}
        
        response = requests.patch(
            f"{ENDPOINT}/{employee_id}/transfer",
            json=transfer_data,
            headers={'Content-Type': 'application/json'}
        )
        
        try:
            assert response.status_code == 404, f"Expected 404 for inactive employee, got {response.status_code}"
            
            data = response.json()
            assert 'message' in data, "Response debe contener campo 'message'"
            
            print("✓ Test 5 PASSED: Empleado inactivo retorna 404")
            self.test_results.append(True)
        except AssertionError as e:
            print(f"✗ Test 5 FAILED: {str(e)}")
            self.test_results.append(False)
            raise
    
    def test_06_target_department_not_found(self):
        """
        Caso 6: Departamento destino no existe
        Validar: 404 NOT FOUND, mensaje apropiado
        Puntaje: 0.375 puntos
        """
        employee_id = 2  # Jane Smith
        transfer_data = {"newDepartmentId": 999}  # Departamento no existe
        
        response = requests.patch(
            f"{ENDPOINT}/{employee_id}/transfer",
            json=transfer_data,
            headers={'Content-Type': 'application/json'}
        )
        
        try:
            assert response.status_code == 404, f"Expected 404, got {response.status_code}"
            
            data = response.json()
            assert 'message' in data, "Response debe contener campo 'message'"
            assert 'department' in data['message'].lower(), \
                f"Mensaje debe mencionar 'department', recibido: {data['message']}"
            
            print("✓ Test 6 PASSED: Departamento destino no encontrado retorna 404")
            self.test_results.append(True)
        except AssertionError as e:
            print(f"✗ Test 6 FAILED: {str(e)}")
            self.test_results.append(False)
            raise
    
    def test_07_target_department_inactive(self):
        """
        Caso 7: Departamento destino está inactivo
        Validar: 404 NOT FOUND
        Puntaje: 0.375 puntos
        """
        employee_id = 2  # Jane Smith
        transfer_data = {"newDepartmentId": 5}  # Sales - departamento inactivo
        
        response = requests.patch(
            f"{ENDPOINT}/{employee_id}/transfer",
            json=transfer_data,
            headers={'Content-Type': 'application/json'}
        )
        
        try:
            assert response.status_code == 404, \
                f"Expected 404 for inactive target department, got {response.status_code}"
            
            data = response.json()
            assert 'message' in data, "Response debe contener campo 'message'"
            
            print("✓ Test 7 PASSED: Departamento destino inactivo retorna 404")
            self.test_results.append(True)
        except AssertionError as e:
            print(f"✗ Test 7 FAILED: {str(e)}")
            self.test_results.append(False)
            raise
    
    def test_08_multiple_transfers_same_employee(self):
        """
        Caso 8: Múltiples transferencias del mismo empleado
        Validar: Secuencia de transferencias funciona correctamente
        Puntaje: 0.375 puntos
        """
        employee_id = 3  # Alice Johnson - Engineering
        
        try:
            # Primera transferencia: Engineering -> Marketing (1 -> 2)
            response1 = requests.patch(
                f"{ENDPOINT}/{employee_id}/transfer",
                json={"newDepartmentId": 2},
                headers={'Content-Type': 'application/json'}
            )
            assert response1.status_code == 200, f"Primera transferencia falló: {response1.status_code}"
            data1 = response1.json()
            assert data1['oldDepartment']['id'] == 1 and data1['newDepartment']['id'] == 2
            
            # Segunda transferencia: Marketing -> HR (2 -> 3)
            response2 = requests.patch(
                f"{ENDPOINT}/{employee_id}/transfer",
                json={"newDepartmentId": 3},
                headers={'Content-Type': 'application/json'}
            )
            assert response2.status_code == 200, f"Segunda transferencia falló: {response2.status_code}"
            data2 = response2.json()
            assert data2['oldDepartment']['id'] == 2 and data2['newDepartment']['id'] == 3
            
            # Tercera transferencia: HR -> Engineering (3 -> 1) - devolver a original
            response3 = requests.patch(
                f"{ENDPOINT}/{employee_id}/transfer",
                json={"newDepartmentId": 1},
                headers={'Content-Type': 'application/json'}
            )
            assert response3.status_code == 200, f"Tercera transferencia falló: {response3.status_code}"
            data3 = response3.json()
            assert data3['oldDepartment']['id'] == 3 and data3['newDepartment']['id'] == 1
            
            print("✓ Test 8 PASSED: Múltiples transferencias secuenciales funcionan")
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
        print("EJECUTANDO TESTS - ENDPOINT 4: PATCH /api/employees/{id}/transfer")
        print("=" * 80)
        print()
    
    test_class = TestEndpoint4Transfer()
    
    # Ejecutar todos los tests
    tests = [
        test_class.test_01_successful_transfer,
        test_class.test_02_employee_already_in_department,
        test_class.test_03_transfer_back_to_original,
        test_class.test_04_employee_not_found,
        test_class.test_05_employee_inactive,
        test_class.test_06_target_department_not_found,
        test_class.test_07_target_department_inactive,
        test_class.test_08_multiple_transfers_same_employee,
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
    # Puede ejecutarse con: python test_endpoint_4_transfer.py
    try:
        score, total_points, passed, total = run_all_tests(show_output=True)
        exit(0 if score == TestEndpoint4Transfer.TOTAL_POINTS else 1)
    except Exception as e:
        print(f"\nERROR CRÍTICO: {str(e)}")
        exit(1)
