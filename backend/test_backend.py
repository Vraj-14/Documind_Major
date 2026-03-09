from intent_router import process_question


question = "What is eps for Titan Company Limited and UltraTech Cement Limited in 2023 ?  "

result = process_question(question)

print("\nIntent:", result["intent"])
print("\nEntities:", result["entities"])
print("\nSQL Query:", result["query"])
print("\nDatabase Result:", result["data"])
print("\nFinal Answer:\n")
print(result["answer"])