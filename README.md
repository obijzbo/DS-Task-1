# DS-Task-1

The objective of this project is to get better answers for user queries from gpt-3 on a specific matter. So, there can be some sectors, the data for those are not updated on gpt-3. To handle that, we tried to follow the following steps:

First we'll read the data we want to use in a specific case.
We will divide in to some chunks.
Transform the chunks in to vector using embedding algorithm
Save the vectors to a vector database.
If an user query appears, we'll find some best matches. So, these are the steps we do s preparation of dataset. Then, If a query appeared, we do the following:
We first take the query and find matches with the data we have on vector database, like a semantic serch.
We take those contexts, and generate a prompt appropriate to the use case, including the contexts and the user's original question. We tell gpt-3 to answer based on the context.
Note: The embedding model used here has 384 dimensions.

Tasks:

Load the text from the given docx file and split them in to some chunks. (A splitter is defined, you can use that.)
Add all the splitted chunks to the vector database. (Use addData function)
Create a prompt using the process discussed above.
Get the answer from gpt-3 api.
Get all the things together such that, we can pass a query using the function user_query and get a solid answer.
The embedding model we used here is a basic embedding model, change the model and use openai's embedding model 'text-embedding-ada-002'
Can we improve something in this process? Any suggestion you think of list it down.
Do you think you have a better idea to handle the whole process? Write a summary about the alternative approach.
