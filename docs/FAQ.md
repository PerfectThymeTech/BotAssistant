# FAQ

### Can I use my own vector database with the assistant API?

Azure Open AI assistant API does not support bring-your-own vector database. You cannot create your own Azure AI Search service and point to it within the payload of the assistant API call. You have to rely on the built-in vector database and the chunking and indexing capabilities of the built-in file search tool.

One option to rely on your own vector database could be to do client-sie orchestration and retrieve relevant information manually from the vector database and adding that information manually to the thread. However, before using such setup you should consider relying on the standard completion API as this supports a similar featureset, but higher flexibility with the downside that the thread state and vector index also needs to be managed on the client side.

### How can I finetune the vector search in the assistant API file search tool?

The file search tool relies on a built-in vector database that is managed server-side. The vector database supports a limited set of file formats as [documented here](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/file-search?tabs=python#supported-file-types). The following options can be finetuned for the built-in vector database:

- Chunkung strategy:
    - Chunk size in tokens (`max_chunk_size_tokens`): The maximum number of tokens in each chunk. The default value is `800`. The minimum value is `100` and the maximum value is
    `4096`.
    - Chunk overlap (`chunk_overlap_tokens`): The number of tokens that overlap between chunks. The default value is `400`. Note that the overlap must not exceed half of `max_chunk_size_tokens`.

More details can be found here: [Link](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/file-search?tabs=python#how-it-works).
