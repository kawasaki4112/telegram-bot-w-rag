from llama_cpp import Llama

llm = Llama(
      model_path="bot/llm/models/model-q4_K.gguf", # Path to the model file
      n_gpu_layers=-1,
      n_ctx=512,
      n_batch=1024,
      embedding=True,
)
output = llm(
      "Q: Name the planets in the solar system? A: ", # Prompt
        max_tokens=512,
        temperature=0.7,
        top_p=0.9,
        repeat_penalty=1.1,
        presence_penalty=0.5
) # Generate a completion, can also call create_completion

embeddings = llm.create_embeddings(
      ["What is the capital of France?", "What is the largest mammal?"], # List of texts to embed
      n_threads=-1, # Number of threads to use for embedding
      normalize=True, # Normalize the embeddings
)

print(output['choices'][0]['text']) # Print the generated text
print("--------------------------------------------------")
print(embeddings)
llm.close()