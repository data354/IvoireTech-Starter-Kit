import streamlit as st
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import asyncio
import time
import pandas as pd
import plotly.express as px

# Basic configuration
load_dotenv()

# Initialize conversation history and states
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Bonjour ! 👋 Je suis votre assistant IA. Comment puis-je vous aider ?",
        }
    ]
if "stop_generation" not in st.session_state:
    st.session_state.stop_generation = False
if "is_generating" not in st.session_state:
    st.session_state.is_generating = False

# Page configuration
st.set_page_config(
    page_title="Hackathon Starter Kit",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Simplified CSS styling
st.markdown(
    """
    <style>
        .stChatMessage {
            padding: 12px;
            border-radius: 12px;
        }
        .stMarkdown table {
            width: 100% !important;
        }
        .stop-button {
            background-color: #dc3545 !important;
            color: white !important;
            border: none !important;
            padding: 8px 16px !important;
            border-radius: 4px !important;
            cursor: pointer !important;
        }
    </style>
""",
    unsafe_allow_html=True,
)


# Agent initialization with caching
@st.cache_resource
def initialize_agent():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def _initialize():
        # Configure MCP client connection
        client = MultiServerMCPClient(
            {
                "local_mcp": {
                    "url": "https://mcp-server-626474317752.europe-west1.run.app/mcp/",
                    "transport": "streamable_http",
                }
            }
        )
        tools = await client.get_tools()
        return create_react_agent("openai:gpt-4o-mini", tools)

    return loop.run_until_complete(_initialize())


try:
    agent = initialize_agent()
except Exception as e:
    st.error(f"Initialization error: {str(e)}")
    st.stop()

# Simplified sidebar
with st.sidebar:
    st.image(
        "https://data.gouv.ci/api/v1/portals/yCWsyaGpA/assets/logo?draft=false&hash=fit-290f57f7b3.png",
        width=150,
    )
    st.markdown("### IvoireTech Starter Kit")
    st.markdown(
        """
    AI Agent for your hackathon.
    Features:
    - Data search
    - Basic analysis
    - Visualization
    """
    )

    # Conversation reset button
    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Bonjour ! 👋 Je suis votre agent IA. Comment puis-je vous aider ?",
            }
        ]
        st.session_state.stop_generation = False
        st.session_state.is_generating = False
        st.rerun()

# Display message history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input(
    "Ask your question...", disabled=st.session_state.is_generating
):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.stop_generation = False
    st.session_state.is_generating = True
    st.rerun()

# Response generation
if st.session_state.is_generating and not st.session_state.stop_generation:
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        stop_placeholder = st.empty()

        # Stop generation button
        if stop_placeholder.button("⏹️ Stop generation", key="stop_btn"):
            st.session_state.stop_generation = True
            st.session_state.is_generating = False
            st.rerun()

        full_response = ""

        with st.spinner("Thinking..."):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                response = loop.run_until_complete(
                    agent.ainvoke({"messages": st.session_state.messages})
                )

                # Progressive display with stop capability
                words = response["messages"][-1].content.split()
                for i, word in enumerate(words):
                    if st.session_state.stop_generation:
                        full_response += f"\n\n*[Generation stopped by user after {i+1}/{len(words)} words]*"
                        break

                    full_response += word + " "
                    time.sleep(0.05)
                    message_placeholder.markdown(full_response + "▌")

                # Final display
                message_placeholder.markdown(full_response)
                stop_placeholder.empty()

                # Attempt to create visualization from table data
                if not st.session_state.stop_generation and "|" in full_response:
                    try:
                        # Extract table lines
                        lines = [
                            line
                            for line in full_response.split("\n")
                            if "|" in line and "-" not in line
                        ]
                        if len(lines) >= 2:
                            headers = [
                                h.strip() for h in lines[0].strip("|").split("|")
                            ]
                            data = []
                            for line in lines[1:]:
                                data.append(
                                    [d.strip() for d in line.strip("|").split("|")]
                                )

                            if len(headers) >= 2:
                                df = pd.DataFrame(data, columns=headers)
                                # Convert numeric values
                                for col in df.columns[1:]:
                                    try:
                                        df[col] = pd.to_numeric(
                                            df[col]
                                            .str.replace(",", "")
                                            .str.replace(" ", "")
                                        )
                                    except:
                                        pass

                                if pd.api.types.is_numeric_dtype(df[df.columns[1]]):
                                    fig = px.bar(df, x=df.columns[0], y=df.columns[1])
                                    st.plotly_chart(fig, use_container_width=True)
                    except Exception as e:
                        st.error(f"Visualization error: {str(e)}")

            except Exception as e:
                full_response = f"⚠️ Error: {str(e)}"
                message_placeholder.markdown(full_response)
            finally:
                loop.close()
                st.session_state.is_generating = False

        # Add response to history
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )
        st.rerun()

# Clear stop generation flag if set
if st.session_state.stop_generation:
    st.session_state.stop_generation = False
