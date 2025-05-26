from llama_cpp import Llama

from sentence_transformers import SentenceTransformer



model_path = "models/model-Q2_K.gguf"
llm = Llama(model_path=model_path, n_gpu_layers=40, n_ctx=512, n_batch=512)

async def async_main():
    async with llm.begin() as conn:
        await conn.run_sync()