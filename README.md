# 🚀 Infection AI Cookbook - Your Ultimate Guide to AI-Powered Applications! 🚀 

## 🌟 Welcome to the **Infection AI Cookbook**

🤖✨ Hey there, AI enthusiast! 🤖✨ Ready to dive into the world of **Inflection AI** and supercharge your projects? This repository is your all-in-one guide, packed with fun, practical, and powerful AI use cases!

Whether you're automating workflows, classifying documents, generating intelligent responses, or building AI-powered applications, we've got you covered!

---

## 📜📌 **What’s Inside?** 📜📌
This cookbook contains a collection of hands-on notebooks showcasing how to use **Inflection AI** to solve real-world problems. Here’s what you’ll find inside:

### 🚦 **Intent Recognition for Service Routing** 🚦
- Uses **Chain-of-Thought (CoT) reasoning** for smarter intent classification.
- Extracts **user intent** & provides structured XML outputs. 
- Optimized for **Inflection 3 Productivity Model** to ensure top-notch accuracy.

### 📂 **Document Classification** 📂 
- Sorts documents into categories like **Statement of Work (SOW) or Other**
- Uses **instruction-based prompting** to ensure consistency & reliability.
- Generates **structured XML outputs** for seamless automation.

### 💻 **Code Generation for Automated Development** 💻
- Generates **Python & SQL** code automatically!   
- Uses **Inflection 3 Pi model** for high-quality, structured output.  
- Ensures best practices in readability, maintainability & efficiency.

### ❤️ **Emotional Intelligence in Social Media Responses** ❤️ 
- Detects **emotional tone** in messages & adjusts response accordingly.
- Improves user engagement & sentiment alignment.
- Generates **empathetic, adaptive replies** to enhance brand communication.

### 🧠 **Few-Shot Learning for Smart Adaptation** 🧠
- Learns from just a few examples for **quick, efficient generalization**.
- Adapts to different tasks with minimal labeled data. 
- Uses **prompt-based fine-tuning** for accurate predictions.

### ⚙️ **Function Calling with Structured API Queries** ⚙️
- Automates **API calls** with structured function execution.
- Ensures consistent, interpretable, and adaptable API interactions.

### 🧐 **Retrieval-Augmented Generation (RAG) for Context-Aware AI Agents**🧐
- Enhances AI reasoning by retrieving **relevant knowledge** before responding.
- Ensures AI-generated responses are **context-rich & accurate**.

### 📜 **Automated Specification Validation** 📜
- Ensures **compliance & correctness** in software development.  
- Extracts key compliance criteria & identifies inconsistencies.   
- Outputs **structured validation reports** for review. 

### 📅 **Meeting Scheduling with JSON Output** 📅
- Extracts meeting details like **date, duration, participants, and topics**.
- Handles relative dates (e.g., "next Friday") dynamically. 
- Outputs structured **JSON format** for seamless scheduling automation. 

### 🏗 **Structured Output Generation with XML Formatting** 🏗
- Converts AI responses into **structured XML format**. 
- Ensures **validity, consistency, and seamless data integration**.  
- Perfect for **automation pipelines & interoperability**. 

### 🧪 **Automated Testing with Inflection AI** 🧪
- **Automates testing** of Inflection LLM outputs.
- Ensures **high coverage and reliability** in software testing.
- Generates structured test reports for easy analysis and debugging.

---

## 🏁 **Getting Started with Inflection AI** 🏁

### Inflection-3 Models

Inflection-3 comprises two models designed for distinct purposes:

- **Pi (3.0)**: The model powering our Pi experience, including a backstory, emotional intelligence, productivity, and safety. It excels in scenarios such as customer support chatbots. Set the config field in the API request JSON to `inflection_3_pi` to use this model.
- **Productivity (3.0)**: The model optimized for following instructions. It is better for tasks requiring JSON output or precise adherence to provided guidelines. Set the config field in the API request JSON to `inflection_3_productivity` to use this model.

### Context Window
Both models currently support an 8k context window.

To run these examples, you’ll need an **Inflection AI Developers Account** and an API key. Follow these steps to get started:

1️⃣ **Sign Up & Get Your API Key** 🔑  
👉 [Sign up here](https://developers.inflection.ai/login) using Google or GitHub.  
👉 Navigate to the **API Keys** section and create a new key.

2️⃣ **Read the API Docs** 📖  
👉 Check out the official [Inflection AI API Docs](https://developers.inflection.ai/docs) to understand usage and best practices.

3️⃣ **Authenticate Your Requests** 🔐  

4️⃣ **Create a .env file and asign your key to INFLECTION_API_KEY**🔏

Include your API key in all requests using the `Authorization` header:
```bash
curl --location 'https://layercake.pubwestus3.inf7ks8.com/external/api/inference' \\
    --header 'Authorization: Bearer <YOUR_API_KEY>' \\
    --header 'Content-Type: application/json' \\
    --data '{
        "context": [
            {
                "text": "Hi",
                "type": "Human"
            }
        ],
        "config": "inflection_3_pi"
    }'
```


---

## 🤝 **Join the Community & Get Support** 🤝

💡 **Questions? Issues? Need help?** Head over to:
- 📚 [Inflection AI Docs](https://developers.inflection.ai/docs) for detailed guides.
- 🏗 [Inflection AI Playground](https://developers.inflection.ai/playground) to test models interactively.
- 🏆 Join our AI community and share your projects!

🚀 **Start Building with Inflection AI Today!** 🚀

✨ Happy Coding! ✨