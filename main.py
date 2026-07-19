"""Main entry point for the Mini Minion demo."""

import asyncio
import os
import sys
from dotenv import load_dotenv

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from minion.sandbox import init_sandbox, destroy_sandbox
from minion.workflow import build_minion_workflow

load_dotenv()



async def run_minion(task: str, repo_path: str = "./sample_repo"):
    """Run the Mini Minion end-to-end."""
    print("=" * 70)
    print(f"🤖 MINI MINION ACTIVATED")
    print(f"📋 Task: {task}")
    print(f"📂 Repo: {repo_path}")
    print("=" * 70)

    # 1. Start sandbox
    init_sandbox(repo_path=repo_path)

    try:
        # 2. Build workflow
        workflow = build_minion_workflow()

        # 3. Setup ADK session
        session_service = InMemorySessionService()
        app_name = "mini_minion"
        user_id = "demo_user"
        session_id = "session_001"
        
        await session_service.create_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id,
        )

        runner = Runner(
            agent=workflow,
            app_name=app_name,
            session_service=session_service,
        )

        # 4. Run the agent
        user_message = types.Content(
            role="user",
            parts=[types.Part(text=task)],
        )

        print("\n🔄 Minion working...\n")
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=user_message,
        ):
            # Print progress
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if hasattr(part, "text") and part.text:
                        print(f"[{event.author}]: {part.text[:500]}")
                    if hasattr(part, "function_call") and part.function_call:
                        fc = part.function_call
                        print(f"🔧 [{event.author}] calling {fc.name}({dict(fc.args)})")

        print("\n" + "=" * 70)
        print("✅ MINION FINISHED")
        print("=" * 70)

    finally:
        # 5. Cleanup
        destroy_sandbox()


if __name__ == "__main__":
    # Demo task: fix failing tests
    default_task = (
        "The tests in tests/test_calculator.py are failing. "
        "Investigate the bugs in src/calculator.py and fix them so all tests pass. "
        "Also add a ValueError raise for division by zero."
    )
    
    task = sys.argv[1] if len(sys.argv) > 1 else default_task
    asyncio.run(run_minion(task))