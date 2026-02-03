"""
Test Full Flow: Validación completa de todos los endpoints del sistema
Ejecuta un flujo de pruebas que cubre todos los 6 endpoints de la API
Integra y ejecuta todos los módulos de tests individuales
"""

import sys
import os

# Agregar el directorio de tests al path para importar los módulos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importar módulos de tests individuales
try:
    from test_endpoint_1_departments import run_all_tests as run_endpoint_1_tests
except ImportError:
    print("⚠ WARNING: test_endpoint_1_departments.py no encontrado")
    run_endpoint_1_tests = None

try:
    from test_endpoint_2_companies import run_all_tests as run_endpoint_2_tests
except ImportError:
    print("⚠ WARNING: test_endpoint_2_companies.py no encontrado")
    run_endpoint_2_tests = None

try:
    from test_endpoint_3_high_salary import run_all_tests as run_endpoint_3_tests
except ImportError:
    print("⚠ WARNING: test_endpoint_3_high_salary.py no encontrado")
    run_endpoint_3_tests = None

try:
    from test_endpoint_4_transfer import run_all_tests as run_endpoint_4_tests
except ImportError:
    print("⚠ WARNING: test_endpoint_4_transfer.py no encontrado")
    run_endpoint_4_tests = None


class TestFullFlow:
    """Clase para ejecutar el flujo completo de pruebas de la API"""
    
    def __init__(self):
        self.endpoint_scores = []
        self.total_score = 0.0
        self.max_score = 0.0
        
    def log_endpoint_result(self, endpoint_name: str, score: float, max_score: float, 
                           passed: int, total: int, status: str = ""):
        """Registra el resultado de un endpoint completo"""
        self.endpoint_scores.append({
            'endpoint': endpoint_name,
            'score': score,
            'max_score': max_score,
            'passed': passed,
            'total': total,
            'status': status
        })
        self.total_score += score
        self.max_score += max_score
        
        percentage = (score / max_score * 100) if max_score > 0 else 0
        status_icon = "✓" if score == max_score else "⚠" if score > 0 else "✗"
        
        print(f"\n{status_icon} {endpoint_name}")
        print(f"   Puntaje: {score:.2f} / {max_score:.2f} ({percentage:.1f}%)")
        print(f"   Tests: {passed}/{total} aprobados")
        if status:
            print(f"   Estado: {status}")
    
    def test_endpoint_1_department_with_employees(self):
        """ENDPOINT 1: GET /api/departments/{id}/employees - 2.0 puntos"""
        print("\n" + "=" * 80)
        print("ENDPOINT 1: Obtener departamento con sus empleados")
        print("Ejecutando módulo: test_endpoint_1_departments.py")
        print("=" * 80)
        
        try:
            if run_endpoint_1_tests:
                # Ejecutar tests del módulo (sin mostrar output detallado)
                score, max_score, passed, total = run_endpoint_1_tests(show_output=False)
                
                # Registrar resultado
                status = "Completado exitosamente" if score == max_score else "Completado con errores"
                self.log_endpoint_result("ENDPOINT 1", score, max_score, passed, total, status)
            else:
                
                # Fallback a tests integrados (mantener compatibilidad)
                
                print("⚠ Módulo test_endpoint_1_companies.py no disponible")
                self.log_endpoint_result("ENDPOINT 1", 0.0, 2, 0, 0, "Módulo no disponible")
        except Exception as e:
            print(f"✗ ERROR al ejecutar ENDPOINT 1: {str(e)}")
            self.log_endpoint_result("ENDPOINT 1", 0.0, 2.0, 0, 0, f"Error: {str(e)}")
    

    def test_endpoint_2_company_departments(self):
        """ENDPOINT 2: GET /api/companies/{id}/departments - 2.0 puntos"""
        print("\n" + "=" * 80)
        print("ENDPOINT 2: Obtener departamentos de una empresa")
        print("Ejecutando módulo: test_endpoint_2_companies.py")
        print("=" * 80)
        
        try:
            if run_endpoint_2_tests:
                # Ejecutar tests del módulo (sin mostrar output detallado)
                score, max_score, passed, total = run_endpoint_2_tests(show_output=False)
                
                # Registrar resultado
                status = "Completado exitosamente" if score == max_score else "Completado con errores"
                self.log_endpoint_result("ENDPOINT 2", score, max_score, passed, total, status)
            else:
                print("⚠ Módulo test_endpoint_2_companies.py no disponible")
                self.log_endpoint_result("ENDPOINT 2", 0.0, 2.0, 0, 0, "Módulo no disponible")
        except Exception as e:
            print(f"✗ ERROR al ejecutar ENDPOINT 2: {str(e)}")
            self.log_endpoint_result("ENDPOINT 2", 0.0, 2.0, 0, 0, f"Error: {str(e)}")
    
    def test_endpoint_3_high_salary_employees(self):
        """ENDPOINT 3: GET /api/companies/{id}/high-salary-employees - 2.0 puntos"""
        print("\n" + "=" * 80)
        print("ENDPOINT 3: Obtener empleados con salario alto")
        print("Ejecutando módulo: test_endpoint_3_high_salary.py")
        print("=" * 80)
        
        try:
            if run_endpoint_3_tests:
                # Ejecutar tests del módulo (sin mostrar output detallado)
                score, max_score, passed, total = run_endpoint_3_tests(show_output=False)
                
                # Registrar resultado
                status = "Completado exitosamente" if score == max_score else "Completado con errores"
                self.log_endpoint_result("ENDPOINT 3", score, max_score, passed, total, status)
            else:
                print("⚠ Módulo test_endpoint_3_high_salary.py no disponible")
                self.log_endpoint_result("ENDPOINT 3", 0.0, 2.0, 0, 0, "Módulo no disponible")
        except Exception as e:
            print(f"✗ ERROR al ejecutar ENDPOINT 3: {str(e)}")
            self.log_endpoint_result("ENDPOINT 3", 0.0, 2.0, 0, 0, f"Error: {str(e)}")
    

    def test_endpoint_4_transfer_employee(self):
        """ENDPOINT 4: PATCH /api/employees/{employeeId}/transfer - 3.0 puntos"""
        print("\n" + "=" * 80)
        print("ENDPOINT 4: Transferir empleado a otro departamento")
        print("Ejecutando módulo: test_endpoint_4_transfer.py")
        print("=" * 80)
        
        try:
            if run_endpoint_4_tests:
                # Ejecutar tests del módulo (sin mostrar output detallado)
                score, max_score, passed, total = run_endpoint_4_tests(show_output=False)
                
                # Registrar resultado
                status = "Completado exitosamente" if score == max_score else "Completado con errores"
                self.log_endpoint_result("ENDPOINT 4", score, max_score, passed, total, status)
            else:
                print("⚠ Módulo test_endpoint_4_transfer.py no disponible")
                self.log_endpoint_result("ENDPOINT 4", 0.0, 3.0, 0, 0, "Módulo no disponible")
        except Exception as e:
            print(f"✗ ERROR al ejecutar ENDPOINT 4: {str(e)}")
            self.log_endpoint_result("ENDPOINT 4", 0.0, 3.0, 0, 0, f"Error: {str(e)}")
    
    
    def print_summary(self):
        """Imprime un resumen final de todos los tests"""
        print("\n" + "=" * 80)
        print("RESUMEN FINAL DE TESTS - TODOS LOS ENDPOINTS")
        print("=" * 80)
        
        # Resumen por endpoint
        print("\nRESULTADOS POR ENDPOINT:")
        print("-" * 80)
        
        for ep in self.endpoint_scores:
            endpoint = ep['endpoint']
            score = ep['score']
            max_score = ep['max_score']
            passed = ep['passed']
            total = ep['total']
            status = ep['status']
            
            percentage = (score / max_score * 100) if max_score > 0 else 0
            status_icon = "✓" if score == max_score else "⚠" if score > 0 else "✗"
            
            print(f"\n{status_icon} {endpoint}")
            print(f"   Puntaje: {score:.2f} / {max_score:.2f} ({percentage:.1f}%)")
            print(f"   Tests: {passed}/{total} aprobados")
            if status:
                print(f"   Estado: {status}")
        
        # Totales globales
        print("\n" + "=" * 80)
        print("TOTALES GLOBALES:")
        print("=" * 80)
        
        total_passed = sum(ep['passed'] for ep in self.endpoint_scores)
        total_tests = sum(ep['total'] for ep in self.endpoint_scores)
        global_percentage = (self.total_score / self.max_score * 100) if self.max_score > 0 else 0
        
        print(f"\nPuntaje Total: {self.total_score:.2f} / {self.max_score:.2f} ({global_percentage:.1f}%)")
        print(f"Tests Totales: {total_passed}/{total_tests} aprobados")
        
        # Mensaje de éxito
        if self.total_score == self.max_score:
            print("\n🎉 ¡PERFECTO! TODOS LOS TESTS PASARON 🎉")
        elif global_percentage >= 80:
            print("\n✓ ¡Excelente! La mayoría de los tests pasaron")
        elif global_percentage >= 60:
            print("\n⚠ Buen progreso, algunos tests requieren atención")
        elif global_percentage >= 40:
            print("\n⚠ Varios tests fallaron, revisar implementación")
        else:
            print("\n✗ Muchos tests fallaron, revisar código")
        
        # Mostrar endpoints pendientes
        pending = [ep for ep in self.endpoint_scores if ep['status'] == "Módulo pendiente"]
        if pending:
            print("\n" + "-" * 80)
            print("MÓDULOS PENDIENTES DE IMPLEMENTACIÓN:")
            print("-" * 80)
            for ep in pending:
                print(f"  • {ep['endpoint']} - {ep['max_score']:.1f} puntos disponibles")
        
        print("\n" + "=" * 80)
        
        return self.total_score == self.max_score


def run_full_flow():
    """Ejecuta el flujo completo de tests"""
    print("\n" + "=" * 80)
    print("INICIANDO FLUJO COMPLETO DE PRUEBAS")
    print("Sistema de Gestión de Departamentos y Empleados")
    print("=" * 80)
    
    tester = TestFullFlow()
    
    # Ejecutar todos los endpoints en orden
    tester.test_endpoint_1_department_with_employees()
    tester.test_endpoint_2_company_departments()
    tester.test_endpoint_3_high_salary_employees()
    tester.test_endpoint_4_transfer_employee()
    
    # Mostrar resumen
    all_passed = tester.print_summary()
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    try:
        exit_code = run_full_flow()
        exit(exit_code)
    except Exception as e:
        print(f"\nERROR CRÍTICO: {str(e)}")
        import traceback
        traceback.print_exc()
        exit(1)
