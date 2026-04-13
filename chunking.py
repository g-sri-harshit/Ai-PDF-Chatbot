CHUNK_SIZE = 300
CHUNK_OVERLAP = 50

def chunk_text(text, size=CHUNK_SIZE, overlap = CHUNK_OVERLAP):
    words = text.split()
    chunks=[]

    for i in range(0,len(words), size - overlap):
        chunk = " ".join(words[i:i + size])
        chunks.append(chunk)

    return chunks

