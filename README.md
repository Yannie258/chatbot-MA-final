**Master Thesis Project**  

**Author:** Yen Nguyen

**Contact** thi-ngoc-yen.nguyen@s2022.tu-chemnitz.de

---

## Getting started

This project investigates how Large Language Models (LLMs) can produce structured, user-customized outputs - such as cards, buttons, carousels, and links — to enhance clarity, usability, and task efficiency for international students during their TU Chemnitz onboarding process.

Two chatbot versions were implemented:

- **Version A – Unstructured:** Traditional text-based responses similar to ChatGPT-style paragraphs.

- **Version B – Structured:** LLM-generated responses in JSON following pre-defined schemas that map to GUI elements such as cards, buttons, and links.

Both versions share the same retrieval and knowledge sources but differ in output format and rendering logic.
This allows for a direct comparison between unstructured and structured interactions.

## Features

- **Dual Implementation**: Side-by-side comparison of structured vs. unstructured outputs
- **Interactive Elements**: Cards, buttons, carousels, and contextual links in structured version
- **Docker Containerization**: Easy setup and deployment
- **RESTful API**: Backend service for chatbot functionality
- **Responsive Frontend**: Modern web interfaces for both versions

## Technical Stack

### Frontend
- **Framework:** Next.js (React-based)
- **Styling:** Tailwind CSS for responsive UI
- **Rendering Logic:** Dynamic components for structured outputs (`CardComponent`, `CarouselComponent`, `ButtonList`, `LinkList`)
- **Deployment:** Vercel for cloud hosting and demo access

### Backend
- **Framework:** FastAPI (Python)
- **LLM Integration:** OpenAI API 
- **Retrieval-Augmented Generation (RAG):** Combines document embeddings and context retrieval for accurate answers
- **Data Storage:** FAISS for vector search and metadata handling
- **Prompt Management:** Dedicated templates for structured and unstructured outputs

### Containerization
- **Tooling:** Docker & Docker Compose for reproducible environments
- **Purpose:** Isolates frontend, backend, and database for easy deployment

### Data & Output Formats
- **Structured Output:** JSON schemas defining cards, buttons, carousels, and links
- **Unstructured Output:** Plain text generated via LLM response
- **Evaluation Data:** Collected from user testing and interviews  

## Installation (development)

### Step 1: clone the project

**Option 1**: **Clone the Project from GitLab**

Open a terminal and clone the repository from TU Chemnitz GitLab:
   ```bash
   ## use SSH
   git clone git@gitlab.hrz.tu-chemnitz.de:vsr/edu/advising/ma-yen-nguyen.git
   ## OR use https
   git clone https://gitlab.hrz.tu-chemnitz.de/vsr/edu/advising/ma-yen-nguyen.git
   
   cd ma-yen-nguyen
```

**Option 2**: **Extract from Zip**

- Download zip file from GitLab or extract from provided USB
- Navigate to the project folder

### Step 2: Set Environment Variables

Copy .env.example to .env inside root directories.

Fill in your keys or local settings as required.

### Step 3: Run program in docker

1. Make sure **Docker Desktop** is running.  
2. From the **root directory** of the project, run:
   ```bash
   docker compose build
   docker compose up 
   ```

### Once containers are running:

Frontend for baseline chatbot (only plain text): http://localhost:3000

Frontend for structured outputs chatbot: http://localhost:3001

Backend API: http://localhost:8000

### To stop all services:
```bash
docker compose down
```

## Chat with chatbot

After launching the frontend:

- You will see a mock-up website with a chat icon on the bottom-right corner.

- Click the icon to open the chat widget and start your conversation.

- Version A (plain text) displays traditional messages, while Version B (structured) renders interactive UI components like cards, buttons, links, etc.

## Production Deployment

This project has been deployed temporarly in Vercel. For simple user please follow the link:
- https://chatbot-tuc-plain.vercel.app (for plain text chatbot)
- https://chatbot-tuc-so.vercel.app/ (for structured outputs chatbot)

** Note: The server can be down if the author stop it. Please contact to author if you if you believe the server is not responding.

## License and Support
This project is developed as part of academic research at TU Chemnitz. For technical issues or questions about this research project, please refer to author for usage and distribution.



