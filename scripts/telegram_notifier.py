"""
Bot de Telegram para notificaciones del Pipeline CI/CD
Envía notificaciones en todas las fases del pipeline según los requisitos del proyecto.
"""

import os
import sys
import json
import requests
from typing import Dict, Optional, List
from datetime import datetime


class TelegramNotifier:
    """Cliente de notificaciones Telegram para el pipeline CI/CD"""
    
    def __init__(self, bot_token: str = None, chat_id: str = None):
        """
        Inicializa el notificador de Telegram
        
        Args:
            bot_token: Token del bot de Telegram (o usa TELEGRAM_BOT_TOKEN env var)
            chat_id: ID del chat/canal (o usa TELEGRAM_CHAT_ID env var)
        """
        self.bot_token = bot_token or os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = chat_id or os.getenv('TELEGRAM_CHAT_ID')
        
        if not self.bot_token or not self.chat_id:
            print("⚠️ TELEGRAM_BOT_TOKEN o TELEGRAM_CHAT_ID no configurados")
            self.enabled = False
        else:
            self.enabled = True
            self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
    
    def send_message(self, message: str, parse_mode: str = "HTML") -> bool:
        """
        Envía un mensaje a Telegram
        
        Args:
            message: Texto del mensaje (soporta HTML)
            parse_mode: Formato del mensaje (HTML o Markdown)
            
        Returns:
            True si se envió exitosamente, False en caso contrario
        """
        if not self.enabled:
            print("❌ Telegram no configurado. Mensaje no enviado:")
            print(message)
            return False
        
        try:
            url = f"{self.base_url}/sendMessage"
            payload = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": parse_mode,
                "disable_web_page_preview": False
            }
            
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            
            print("✅ Notificación Telegram enviada exitosamente")
            return True
            
        except Exception as e:
            print(f"❌ Error enviando notificación Telegram: {e}")
            return False
    
    # ========== NOTIFICACIONES DEL PIPELINE ==========
    
    def notify_security_scan_start(self, repo: str, branch: str, 
                                   pr_number: Optional[int] = None,
                                   files_count: int = 0) -> bool:
        """
        Notifica el inicio de la revisión de seguridad (Etapa 1)
        
        Args:
            repo: Nombre del repositorio
            branch: Rama siendo analizada
            pr_number: Número de PR (si aplica)
            files_count: Cantidad de archivos a escanear
        """
        emoji = "🔍"
        title = f"{emoji} <b>Iniciando Revisión de Seguridad</b>"
        
        message = f"""{title}

📦 <b>Repositorio:</b> {repo}
🌿 <b>Rama:</b> {branch}
"""
        
        if pr_number:
            message += f"🔀 <b>Pull Request:</b> #{pr_number}\n"
        
        message += f"""📄 <b>Archivos a escanear:</b> {files_count}
⏰ <b>Hora:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🤖 El modelo de Machine Learning está analizando el código...
"""
        
        return self.send_message(message)
    
    def notify_vulnerability_detected(self, repo: str, branch: str,
                                     pr_number: Optional[int],
                                     vulnerability_details: Dict) -> bool:
        """
        Notifica cuando se detecta código VULNERABLE (Etapa 1 - Rechazo)
        
        Args:
            repo: Nombre del repositorio
            branch: Rama
            pr_number: Número de PR
            vulnerability_details: Diccionario con detalles de vulnerabilidades
        """
        emoji = "🚨"
        title = f"{emoji} <b>VULNERABILIDAD DETECTADA - PR RECHAZADO</b>"
        
        high_risk = vulnerability_details.get('high_risk_count', 0)
        medium_risk = vulnerability_details.get('medium_risk_count', 0)
        total_files = vulnerability_details.get('total_files', 0)
        
        message = f"""{title}

❌ <b>Estado:</b> PR BLOQUEADO / MERGE RECHAZADO
📦 <b>Repositorio:</b> {repo}
🌿 <b>Rama:</b> {branch}
"""
        
        if pr_number:
            message += f"🔀 <b>Pull Request:</b> #{pr_number}\n"
        
        message += f"""
📊 <b>Resultados del escaneo:</b>
   • Total archivos: {total_files}
   • 🔴 Alto riesgo: {high_risk}
   • 🟠 Riesgo medio: {medium_risk}

⚠️ <b>Acción requerida:</b>
1. Revisar las vulnerabilidades detectadas
2. Corregir el código vulnerable
3. Realizar un nuevo commit para re-escanear

🏷️ Etiqueta aplicada: "fixing-required"
📋 Issue automática creada con detalles
"""
        
        # Agregar detalles de vulnerabilidades específicas
        if 'vulnerabilities' in vulnerability_details:
            message += "\n<b>Vulnerabilidades detectadas:</b>\n"
            for vuln in vulnerability_details['vulnerabilities'][:5]:  # Primeras 5
                file = vuln.get('file', 'Unknown')
                prob = vuln.get('probability', 0) * 100
                vuln_type = vuln.get('vulnerability_type', 'Unknown')
                message += f"   • {file}: {vuln_type} ({prob:.1f}% probabilidad)\n"
        
        return self.send_message(message)
    
    def notify_code_secure(self, repo: str, branch: str,
                          pr_number: Optional[int],
                          scan_details: Dict) -> bool:
        """
        Notifica cuando el código es clasificado como SEGURO (Etapa 1 - Aprobado)
        
        Args:
            repo: Nombre del repositorio
            branch: Rama
            pr_number: Número de PR
            scan_details: Detalles del escaneo
        """
        emoji = "✅"
        title = f"{emoji} <b>Código SEGURO - Continuando Pipeline</b>"
        
        total_files = scan_details.get('total_files', 0)
        
        message = f"""{title}

✅ <b>Estado:</b> APROBADO POR MODELO ML
📦 <b>Repositorio:</b> {repo}
🌿 <b>Rama:</b> {branch}
"""
        
        if pr_number:
            message += f"🔀 <b>Pull Request:</b> #{pr_number}\n"
        
        message += f"""
📊 <b>Resultados:</b>
   • Total archivos analizados: {total_files}
   • 🟢 Todos los archivos son seguros

➡️ <b>Siguiente etapa:</b> Merge a rama 'test' y ejecución de pruebas
"""
        
        return self.send_message(message)
    
    def notify_merge_to_test(self, repo: str, branch: str, pr_number: Optional[int]) -> bool:
        """
        Notifica el merge automático a rama test (Etapa 2)
        """
        emoji = "🔀"
        title = f"{emoji} <b>Merge Automático a Test Realizado</b>"
        
        message = f"""{title}

✅ <b>Acción:</b> Merge completado exitosamente
📦 <b>Repositorio:</b> {repo}
🌿 <b>Desde:</b> {branch} → <b>test</b>
"""
        
        if pr_number:
            message += f"🔀 <b>Pull Request:</b> #{pr_number}\n"
        
        message += f"""
⏰ <b>Hora:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🧪 Iniciando ejecución de pruebas unitarias e integración...
"""
        
        return self.send_message(message)
    
    def notify_tests_result(self, repo: str, passed: bool, 
                           tests_details: Optional[Dict] = None) -> bool:
        """
        Notifica el resultado de las pruebas (Etapa 2)
        
        Args:
            repo: Nombre del repositorio
            passed: True si todas las pruebas pasaron
            tests_details: Detalles de las pruebas ejecutadas
        """
        if passed:
            emoji = "✅"
            title = f"{emoji} <b>Pruebas EXITOSAS</b>"
            status = "TODAS LAS PRUEBAS PASARON"
            next_step = "➡️ <b>Siguiente etapa:</b> Merge a 'main' y despliegue a producción"
        else:
            emoji = "❌"
            title = f"{emoji} <b>Pruebas FALLIDAS</b>"
            status = "ALGUNAS PRUEBAS FALLARON"
            next_step = "⚠️ <b>Pipeline BLOQUEADO hasta corregir las pruebas</b>\n🏷️ Etiqueta aplicada: \"tests-failed\""
        
        message = f"""{title}

{status}
📦 <b>Repositorio:</b> {repo}
⏰ <b>Hora:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        if tests_details:
            total = tests_details.get('total', 0)
            passed_count = tests_details.get('passed', 0)
            failed_count = tests_details.get('failed', 0)
            
            message += f"""
📊 <b>Resultados:</b>
   • Total pruebas: {total}
   • ✅ Pasaron: {passed_count}
   • ❌ Fallaron: {failed_count}
"""
        
        message += f"\n{next_step}"
        
        return self.send_message(message)
    
    def notify_deployment_start(self, repo: str, environment: str = "production") -> bool:
        """
        Notifica el inicio del despliegue (Etapa 3)
        """
        emoji = "🚀"
        title = f"{emoji} <b>Iniciando Despliegue a Producción</b>"
        
        message = f"""{title}

✅ <b>Acción:</b> Merge a 'main' completado
📦 <b>Repositorio:</b> {repo}
🌿 <b>Rama:</b> main (producción)
🎯 <b>Entorno:</b> {environment}

📦 Construyendo imagen Docker...
🚀 Desplegando aplicación...
"""
        
        return self.send_message(message)
    
    def notify_deployment_success(self, repo: str, environment: str,
                                  deployment_url: Optional[str] = None) -> bool:
        """
        Notifica el despliegue exitoso (Etapa 3 - Final)
        """
        emoji = "🎉"
        title = f"{emoji} <b>DESPLIEGUE EXITOSO</b>"
        
        message = f"""{title}

✅ <b>Estado:</b> APLICACIÓN EN PRODUCCIÓN
📦 <b>Repositorio:</b> {repo}
🎯 <b>Entorno:</b> {environment}
⏰ <b>Hora:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🚀 <b>Pipeline completado exitosamente:</b>
   ✅ Revisión de seguridad ML
   ✅ Merge a test
   ✅ Pruebas unitarias
   ✅ Merge a main
   ✅ Despliegue a producción
"""
        
        if deployment_url:
            message += f"\n🌐 <b>URL:</b> {deployment_url}"
        
        message += "\n\n🎊 ¡Felicidades! El código está en producción."
        
        return self.send_message(message)
    
    def notify_deployment_failed(self, repo: str, environment: str,
                                error_message: Optional[str] = None) -> bool:
        """
        Notifica un fallo en el despliegue (Etapa 3 - Error)
        """
        emoji = "❌"
        title = f"{emoji} <b>DESPLIEGUE FALLIDO</b>"
        
        message = f"""{title}

❌ <b>Estado:</b> ERROR EN DESPLIEGUE
📦 <b>Repositorio:</b> {repo}
🎯 <b>Entorno:</b> {environment}
⏰ <b>Hora:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        if error_message:
            message += f"\n⚠️ <b>Error:</b> {error_message[:200]}"
        
        message += "\n\n🔧 <b>Acción requerida:</b> Revisar logs del pipeline"
        
        return self.send_message(message)


def main():
    """Función principal para testing del notificador"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Enviar notificaciones Telegram')
    parser.add_argument('--type', required=True, 
                       choices=['scan_start', 'vulnerable', 'secure', 'merge_test',
                               'tests_passed', 'tests_failed', 'deploy_start',
                               'deploy_success', 'deploy_failed'],
                       help='Tipo de notificación')
    parser.add_argument('--repo', default='test-repo', help='Nombre del repositorio')
    parser.add_argument('--branch', default='dev', help='Nombre de la rama')
    parser.add_argument('--pr', type=int, help='Número de PR')
    parser.add_argument('--url', help='URL de despliegue')
    parser.add_argument('--data', help='JSON con datos adicionales')
    
    args = parser.parse_args()
    
    notifier = TelegramNotifier()
    
    if not notifier.enabled:
        print("❌ Configura TELEGRAM_BOT_TOKEN y TELEGRAM_CHAT_ID")
        sys.exit(1)
    
    # Procesar tipo de notificación
    success = False
    
    if args.type == 'scan_start':
        success = notifier.notify_security_scan_start(args.repo, args.branch, args.pr, 5)
    
    elif args.type == 'vulnerable':
        details = {
            'high_risk_count': 2,
            'medium_risk_count': 1,
            'total_files': 3,
            'vulnerabilities': [
                {'file': 'app.py', 'probability': 0.95, 'vulnerability_type': 'SQL Injection'}
            ]
        }
        success = notifier.notify_vulnerability_detected(args.repo, args.branch, args.pr, details)
    
    elif args.type == 'secure':
        details = {'total_files': 3}
        success = notifier.notify_code_secure(args.repo, args.branch, args.pr, details)
    
    elif args.type == 'merge_test':
        success = notifier.notify_merge_to_test(args.repo, args.branch, args.pr)
    
    elif args.type == 'tests_passed':
        details = {'total': 10, 'passed': 10, 'failed': 0}
        success = notifier.notify_tests_result(args.repo, True, details)
    
    elif args.type == 'tests_failed':
        details = {'total': 10, 'passed': 8, 'failed': 2}
        success = notifier.notify_tests_result(args.repo, False, details)
    
    elif args.type == 'deploy_start':
        success = notifier.notify_deployment_start(args.repo)
    
    elif args.type == 'deploy_success':
        success = notifier.notify_deployment_success(args.repo, 'production', args.url)
    
    elif args.type == 'deploy_failed':
        success = notifier.notify_deployment_failed(args.repo, 'production', 'Build failed')
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
