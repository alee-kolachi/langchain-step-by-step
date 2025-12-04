from langchain_classic.text_splitter import CharacterTextSplitter

text = ""
with open("docs/abc.txt", 'r') as f:
    text = f.read()
splitter = CharacterTextSplitter(
    chunk_size = 100,
    chunk_overlap = 0,
    separator=''
)

result = splitter.split_text(text)

print(result)
