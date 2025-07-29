#!/usr/bin/env python3
"""
Script de inicialização da GitHub Data API e execução de testes
"""

import sys
import subprocess
import uvicorn
from app.config import settings


def run_tests():
    """Executa todos os testes do projeto"""
    print("🧪 Executando todos os testes...")
    print("=" * 50)
    
    try:
        # Executa pytest com todos os testes
        result = subprocess.run([
            sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"
        ], capture_output=True, text=True, cwd=".")
        
        print(result.stdout)
        
        if result.stderr:
            print("⚠️  Warnings/Errors:")
            print(result.stderr)
        
        if result.returncode == 0:
            print("✅ Todos os testes passaram com sucesso!")
            return True
        else:
            print("❌ Alguns testes falharam!")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao executar testes: {e}")
        return False


def run_api():
    """Executa a API do GitHub"""
    print("🚀 Iniciando GitHub Data API...")
    print(f"📍 URL: http://{settings.host}:{settings.port}")
    print(f"📚 Documentação: http://{settings.host}:{settings.port}/docs")
    print("=" * 50)
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info"
    )


def show_menu():
    """Exibe menu de opções"""
    print("🔹 GitHub Data API - Menu Principal")
    print("=" * 40)
    print("1. 🚀 Executar API")
    print("2. 🧪 Executar todos os testes")
    print("3. 🧪 Executar testes + 🚀 Executar API")
    print("4. 📊 Executar testes com cobertura")
    print("5. 🚪 Sair")
    print("=" * 40)


def run_tests_with_coverage():
    """Executa testes com relatório de cobertura"""
    print("📊 Executando testes com cobertura...")
    print("=" * 50)
    
    try:
        # Verifica se pytest-cov está instalado
        import importlib
        try:
            importlib.import_module("pytest_cov")
        except ImportError:
            print("❌ pytest-cov não está instalado!")
            print("💡 Instale com: pip install pytest-cov")
            print("💡 Ou execute: python run.py test")
            return False
        
        # Executa pytest com cobertura
        result = subprocess.run([
            sys.executable, "-m", "pytest", "tests/", "-v", 
            "--cov=app", "--cov-report=term-missing", "--cov-report=html"
        ], capture_output=True, text=True, cwd=".")
        
        print(result.stdout)
        
        if result.stderr:
            print("⚠️  Warnings/Errors:")
            print(result.stderr)
        
        if result.returncode == 0:
            print("✅ Testes com cobertura executados com sucesso!")
            print("📁 Relatório HTML gerado em: htmlcov/index.html")
            return True
        else:
            print("❌ Alguns testes falharam!")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao executar testes com cobertura: {e}")
        return False


def main():
    """Função principal"""
    if len(sys.argv) > 1:
        # Modo linha de comando
        command = sys.argv[1].lower()
        
        if command in ["test", "tests", "t"]:
            success = run_tests()
            sys.exit(0 if success else 1)
        elif command in ["api", "server", "s"]:
            run_api()
        elif command in ["coverage", "cov", "c"]:
            success = run_tests_with_coverage()
            sys.exit(0 if success else 1)
        elif command in ["all", "full"]:
            print("🧪 Executando testes primeiro...")
            success = run_tests()
            if success:
                print("\n🚀 Iniciando API...")
                run_api()
            else:
                print("❌ Testes falharam. API não será iniciada.")
                sys.exit(1)
        else:
            print(f"❌ Comando desconhecido: {command}")
            print("Comandos disponíveis: test, api, coverage, all")
            sys.exit(1)
    else:
        # Modo interativo
        while True:
            show_menu()
            
            try:
                choice = input("Escolha uma opção (1-5): ").strip()
                
                if choice == "1":
                    run_api()
                    break
                elif choice == "2":
                    run_tests()
                    break
                elif choice == "3":
                    print("🧪 Executando testes primeiro...")
                    success = run_tests()
                    if success:
                        print("\n🚀 Iniciando API...")
                        run_api()
                    else:
                        print("❌ Testes falharam. API não será iniciada.")
                    break
                elif choice == "4":
                    run_tests_with_coverage()
                    break
                elif choice == "5":
                    print("👋 Até logo!")
                    break
                else:
                    print("❌ Opção inválida. Tente novamente.")
                    
            except KeyboardInterrupt:
                print("\n👋 Até logo!")
                break
            except Exception as e:
                print(f"❌ Erro: {e}")


if __name__ == "__main__":
    main() 