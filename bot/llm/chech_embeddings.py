from llama_cpp import Llama

llm = Llama(
    model_path="bot/llm/models/model-q4_K.gguf",
    embedding=True,    # ключевой параметр
    n_gpu_layers=-1,   # опционально: сколько слоёв на GPU
    n_ctx=512,
    n_batch=1024
)
embedding = llm.create_embedding("Привет, мир!") 
answer = llm("Привет, мир!")
print(answer['choices'][0]["text"])# список чисел — вектор размерности модели
print(len(embedding))  # например, 4096 для LLaMA-7B
llm.close()  # закрыть модель, когда она больше не нужна