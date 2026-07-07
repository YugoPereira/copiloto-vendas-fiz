from core.agente import AgenteFyz

if __name__ == "__main__":
    try:
        agente = AgenteFyz()
        agente.iniciar()
    except KeyboardInterrupt:
        print("\n\nSistema interrompido pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro fatal no sistema: {e}")