"""Un turno aislado de Hermes por proceso para el chat público de ZÍA.

Entrada (stdin, JSON): {"system": str, "message": str, "history": [{"role", "content"}]}
Salida (stdout): una línea "ZIA_RESULT:{"text": ...}".

Sin herramientas, sin memoria, sin archivos de contexto ni identidad cargada del
perfil: el system prompt lo arma server.py (SOUL del perfil + conocimiento + reglas).
"""
import json
import os
import sys

MARK = 'ZIA_RESULT:'


def main():
    request = json.load(sys.stdin)
    if os.environ.get('ZIA_FAKE_MODEL') == '1':  # solo pruebas locales
        print(MARK + json.dumps({'text': f"(modo prueba) Recibí: {request['message']}"}, ensure_ascii=False))
        return

    sys.path.insert(0, os.environ.get('HERMES_RUNTIME', '/usr/local/lib/hermes-agent'))
    from run_agent import AIAgent

    agent = AIAgent(
        model=os.environ.get('ZIA_MODEL', 'openai/gpt-4.1-mini'),
        provider=os.environ.get('ZIA_PROVIDER', 'openrouter'),
        base_url=os.environ.get('ZIA_BASE_URL', 'https://openrouter.ai/api/v1'),
        api_key=os.environ.get('ZIA_API_KEY') or os.environ['OPENROUTER_API_KEY'],
        enabled_toolsets=[],
        max_iterations=2,
        max_tokens=900,
        quiet_mode=True,
        save_trajectories=False,
        skip_context_files=True,
        skip_memory=True,
        skip_background_review=True,
        load_soul_identity=False,
        run_budget_seconds=60,
        ephemeral_system_prompt=request['system'],
    )
    if agent.tools:
        agent.close()
        raise RuntimeError('El chat público no debe tener herramientas habilitadas')
    try:
        result = agent.run_conversation(request['message'], conversation_history=request.get('history') or [])
        print(MARK + json.dumps({'text': result['final_response']}, ensure_ascii=False))
    finally:
        agent.close()


if __name__ == '__main__':
    main()
