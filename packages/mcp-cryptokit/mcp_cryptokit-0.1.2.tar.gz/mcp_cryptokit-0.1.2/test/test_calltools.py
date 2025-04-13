import asyncio, os, json, ast,sys
from mcp_client import MCPClient

sm4_key = """
    {"status_code": 200, "request_id": "1044d256-65ea-9921-93ee-f276c40ab25a", "code": "", "message": "", "output": {"text": null, "finish_reason": null, "choices": [{"finish_reason": "tool_calls", "message": {"role": "assistant", "content": "首先，我们需要生成一个SM4加密算法所需的密钥。然后，我们将使用这个密钥来加密你的数据：'我是明文'。\\n\\n第一步：生成SM4密钥", "tool_calls": [{"function": {"name": "generate_key", "arguments": "{'key_type': 'SM4'}"}, "index": 0, "id": "call_f938e2319ff546b28bf264", "type": "function"}]}}]}, "usage": {"input_tokens": 1726, "output_tokens": 57, "prompt_tokens_details": {"cached_tokens": 0}, "total_tokens": 1783}}
                """
sm4_encrypt = """
{"status_code": 200, "request_id": "1f4fbd5a-9329-912d-9814-56a845f60b56", "code": "", "message": "", "output": {"text": null, "finish_reason": null, "choices": [{"finish_reason": "stop", "message": {"role": "assistant", "content": "使用SM4密钥加密后的数据为：NyMOAHvi71nrHyPAzujAH11FAU/P1wvpIZ+RNXaNQEutk7Os1f7GQ8e3oS7Eb1sh\\n\\n这就是你的加密后的信息。请注意，为了安全起见，你应该妥善保管生成的密钥ID（19）。"}}]}, "usage": {"input_tokens": 1913, "output_tokens": 80, "prompt_tokens_details": {"cached_tokens": 1024}, "total_tokens": 1993}}
        """
aes_query ="""
{"status_code": 200, "request_id": "8a76cf5f-d382-921c-ab95-9fc297f71264", "code": "", "message": "", "output": {"text": null, "finish_reason": null, "choices": [{"finish_reason": "tool_calls", "message": {"role": "assistant", "content": "为了使用AES算法加密数据，我们需要一个AES密钥ID。如果没有提供密钥ID，我们将首先查询现有的AES密钥。如果不存在任何AES密钥，我们将生成一个新的AES密钥。", "tool_calls": [{"function": {"name": "query_keys", "arguments": "{\\"key_type\\": \\"AES\\"}"}, "index": 0, "id": "call_cd754e023e3f4f438c1a4d", "type": "function"}]}}]}, "usage": {"input_tokens": 2041, "output_tokens": 60, "prompt_tokens_details": {"cached_tokens": 0}, "total_tokens": 2101}}
    """
aes_create ="""
{"status_code": 200, "request_id": "b6350732-119f-9d13-b921-f4c7abd42fd5", "code": "", "message": "", "output": {"text": null, "finish_reason": null, "choices": [{"finish_reason": "tool_calls", "message": {"role": "assistant", "content": "看来系统中还没有AES密钥。让我们生成一个新的AES密钥以便进行加密。", "tool_calls": [{"function": {"name": "generate_key", "arguments": "{\\"key_type\\": \\"AES\\"}"}, "index": 0, "id": "call_dfdbfc885deb498f867cca", "type": "function"}]}}]}, "usage": {"input_tokens": 2109, "output_tokens": 40, "prompt_tokens_details": {"cached_tokens": 0}, "total_tokens": 2149}}
    """
async def test_call_tools():
    json_response = json.loads(aes_create)
    client = MCPClient()
    await client.connect_to_server("server.py")
    response = await client.process_query("", json_response)
    print(response)
    await client.cleanup()

if __name__ == "__main__":
    import sys
    asyncio.run(test_call_tools())