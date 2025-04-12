"""Example comparing synchronous and asynchronous API usage.

This example demonstrates how to use both the synchronous and asynchronous
APIs for structured, unstructured, and tool call responses.
"""

import asyncio
import time

from pydantic import BaseModel, Field

from aikernel import (
    LLMMessagePart,
    LLMSystemMessage,
    LLMUserMessage,
    get_router,
    llm_structured,
    llm_structured_sync,
    llm_unstructured,
    llm_unstructured_sync,
)


# Define a simple structured response model
class Summary(BaseModel):
    main_points: list[str] = Field(description="The main points of the text")
    tone: str = Field(description="The tone of the text (formal, informal, etc.)")
    word_count_estimate: int = Field(description="Estimated number of words in the source text")


# Define a simple tool
class CalcParams(BaseModel):
    operation: str = Field(description="The math operation to perform (add, subtract, multiply, divide)")
    a: float = Field(description="The first number")
    b: float = Field(description="The second number")


async def main():
    start_time = time.time()
    
    # Create a router with the model we want to use
    router = get_router(models=("gemini-2.0-flash",))
    
    # Create messages for our requests
    system_message = LLMSystemMessage(
        parts=[
            LLMMessagePart(
                content="You are a helpful assistant."
            )
        ]
    )
    user_message = LLMUserMessage(
        parts=[
            LLMMessagePart(
                content="Summarize the key features of Python programming language."
            )
        ]
    )
    messages = [system_message, user_message]
    
    # Note: Tool-related code removed as it's not used in this simplified example
    
    # Run a synchronous unstructured request
    print("Making synchronous unstructured request...")
    sync_unstructured_start = time.time()
    
    unstructured_response = llm_unstructured_sync(
        messages=messages,
        router=router,
    )
    
    sync_unstructured_time = time.time() - sync_unstructured_start
    print(f"Sync unstructured response received in {sync_unstructured_time:.2f} seconds")
    print(f"First 100 chars: {unstructured_response.text[:100]}...\n")
    
    # Run a synchronous structured request
    print("Making synchronous structured request...")
    sync_structured_start = time.time()
    
    structured_response = llm_structured_sync(
        messages=messages,
        router=router,
        response_model=Summary,
    )
    
    sync_structured_time = time.time() - sync_structured_start
    print(f"Sync structured response received in {sync_structured_time:.2f} seconds")
    print(f"Main points: {structured_response.structured_response.main_points[:2]}...\n")
    
    # Skip tool call for this example as it requires specific provider configuration
    sync_tool_time = 0
    
    # Now run the same requests asynchronously in parallel
    print("Making asynchronous requests in parallel...")
    async_start = time.time()
    
    # Gather just the unstructured and structured async requests
    unstructured_task, structured_task = await asyncio.gather(
        llm_unstructured(messages=messages, router=router),
        llm_structured(messages=messages, router=router, response_model=Summary)
    )
    
    async_time = time.time() - async_start
    print(f"All async responses received in {async_time:.2f} seconds")
    
    print(f"Async unstructured response first 100 chars: {unstructured_task.text[:100]}...")
    print(f"Async structured response main points: {structured_task.structured_response.main_points[:2]}...")
    
    # Compare total times
    total_sync_time = sync_unstructured_time + sync_structured_time + sync_tool_time
    print(f"\nTotal time for sequential sync requests: {total_sync_time:.2f} seconds")
    print(f"Total time for parallel async requests: {async_time:.2f} seconds")
    print(f"Time saved with async: {total_sync_time - async_time:.2f} seconds ({(1 - async_time / total_sync_time) * 100:.1f}%)")
    
    total_time = time.time() - start_time
    print(f"\nTotal example runtime: {total_time:.2f} seconds")


if __name__ == "__main__":
    asyncio.run(main())
