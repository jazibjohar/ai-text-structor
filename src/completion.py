from ai_engine import AIEngine
import asyncio


def run_completion(model, content, engine_object):
    engine = AIEngine(engine_object, model)
    
    async def execute_with_timing():
        start_time = asyncio.get_event_loop().time()
        result = await engine.execute(content)
        end_time = asyncio.get_event_loop().time()
        print(f"Execution time: {end_time - start_time:.2f} seconds")
        return result
    
    return asyncio.run(execute_with_timing())
