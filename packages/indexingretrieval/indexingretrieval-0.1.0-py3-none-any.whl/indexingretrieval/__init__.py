def addition(numbers: list) -> float:
    return sum(numbers)
def show_code():
    code = '''
index = {
1: "This is the first document",
2: "This document is the second document",
3: "And this is the third one",
4: "Is this the first document?",
5:"The last document is here"
}
inverted_index = {}
for doc_id, text in index.items():
    for word in text.split():
        inverted_index.setdefault(word, set()).add(doc_id)
query = input("Enter your query: ")
result_docs = set()
for word in query.split():
    result_docs.update(inverted_index.get(word,[]))
if result_docs:
    print("Relevant documents found:")
    for doc_id in result_docs:
        print(f"Document {doc_id}: {index[doc_id]}")
else:
    print("No relevant documents found.")

    '''
    print(code)