# IvoireTech Starter Kit 🚀
An intelligent AI agent designed for hackathons, enabling data search, analysis and automatic visualization.

## 🌟 Features
- **Conversational AI agent** with intuitive chat interface
- **Data search** via integrated MCP server
- **Automatic analysis** of data
- **Interactive visualization** with automatic graph generation
- **Modern interface** with Streamlit
- **Real-time generation stop**

## 📋 Prerequisites
- Python 3.8 or higher
- Internet access for MCP server queries
- OpenAI API key (if using OpenAI model)

## 🛠️ Installation

### 1. Clone the project
```bash
git clone https://github.com/data354/IvoireTech-Starter-Kit.git
cd IvoireTech-Starter-Kit
```

### 2. Create a virtual environment
```bash
python -m venv .venv
# Activate the environment
# On Windows
.venv\Scripts\activate
# On macOS/Linux
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment variables configuration
Create a `.env` file at the project root:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

## 🚀 Launching the application

### Method 1: Standard launch
```bash
streamlit run client.py
```

### Method 2: With custom configuration
```bash
streamlit run client.py --server.port 8501 --server.address 0.0.0.0
```

The application will be accessible at: `http://localhost:8501`

## 💡 Usage

### Main interface
1. **Chat area**: Ask questions to the AI agent
2. **Sidebar**: Project information and reset button
3. **Automatic visualizations**: Charts display automatically when tabular data is detected

### Example queries
```
"Can you give me data on the Ivorian population?"
"Analyze the economic trends of Côte d'Ivoire"
"Search for information on the agricultural sector"
```

### Advanced features
- **Generation stop**: Click "⏹️ Stop generation" to interrupt a response
- **Automatic charts**: Tables in responses are automatically converted to charts
- **Persistent history**: Your conversations are saved during the session

## 🔧 Configuration

### MCP Server
The client connects to the hosted MCP server:
- URL: `https://mcp-server-626474317752.europe-west1.run.app/mcp/`
- Transport: `streamable_http`

### AI Model
- Model used: `openai:gpt-4o`
- Framework: LangGraph with ReAct agent

## 📊 Visualizations
The application automatically generates charts from tabular data:
- **Automatic detection** of tables in responses
- **Conversion to DataFrame** Pandas
- **Interactive charts** with Plotly
- **Supported types**: Bar charts, line charts, etc.

## 🐛 Troubleshooting

### Common issues
1. **MCP connection error**
   ```
   Check your Internet connection
   The MCP server must be accessible
   ```

2. **OpenAI API error**
   ```
   Check your API key in the .env file
   Make sure you have sufficient credits
   ```

3. **Dependencies issue**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

### Logs and debugging
For more details on errors:
```bash
streamlit run client.py --logger.level debug
```

## 📦 Project structure
```
IvoireTech-Starter-Kit/
├── client.py                 # Main application
├── requirements.txt          # Python dependencies
├── .env                     # Environment variables
├── README.md               # Documentation
└── .venv/                  # Virtual environment
```

---
**IvoireTech Starter Kit** - 🇨🇮