# generative-ai

This repository contains demo projects related to Google Gemini, Langchain API, Deploment using HuggingFace Hub, usage of vector databases, etc. These examples are taken from the YouTuber [Krish Naik](https://www.youtube.com/@krishnaik06)

Google Gemini Projects:
(Inside gemini/gemini_projects repo and gemini/gemini_llm_app_intro)

|Project | Description|
|--------|------------|
|gemini_llm_intro_app| How to user Gemini API for text and vision applications|
|gemini_projects/chat_multi_pdf_files|User can upload multiple PDFs. The user can then ask questions related to the content of the PDF. The PDF text is converted to vectors using GoogleGenerativeAIEmbeddings and store locally in the FAISS vector database. Once the user asks questions, similarity search is performed on the query and vector documents and top results are returned as response|
|gemini_projects/food_nutrition_info_from_image|It is a vision application where a user can upload image of a food item or dish. The response is all the nutrition information about that image. Google Gemini Pro 1.5 model is used to query|
|gemini_projects/multi_lang_invoice_extractor|It is a vision aplication where a user can upload image of an invoice and various questions related to information on the invoice. Google Gemini Pro 1.5 model is used to query|
|gemini_projects/query_sql_dababase_using_gemini|User inputs a query in text format. The query is converted to a SQL command using a prompt provided with few shot examples. Then the database is queried and results are returned|
|gemini_projects/resume_ats|This is a resume performance applcation wrt to a job description. User provides a JD as an input and his/her resume PDF file. Then the user can see the relevance of the resume to the job description, the missing keywords and how the resume can be improved. Google Gemini Pro 1.5 model is used here|
|gemini_projects/youtube_video_transcribe|User provides a youtube video link. Then a short and long summary of the video is generated and shown to the user using Gemini Pro 1.5 model. This is done in app_summary APP. In another file app_q_a APP, additionally the youtube transcript of the video is conveted to chunks and upserted to a pinecone database. If the user ask any question related to the video, then similar documents to the video are searched using pinecone vector DB similarity search. The response in generated using Gemini Pro 1.5 model|

