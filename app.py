"""
Streamlit Frontend for LangGraph Multi-Agent System
"""
import streamlit as st
import sys
from pathlib import Path
from datetime import datetime
import json

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from utils.config import settings
from workflows.single_agent import create_single_agent_system
from workflows.multi_agent import create_multi_agent_system
from utils.logger import logger


# Page configuration
st.set_page_config(
    page_title="LangGraph Multi-Agent System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5rem 1rem;
    }
    .stButton>button:hover {
        background-color: #1557a0;
    }
    .status-box {
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables."""
    if 'history' not in st.session_state:
        st.session_state.history = []
    if 'current_result' not in st.session_state:
        st.session_state.current_result = None
    if 'agent_logs' not in st.session_state:
        st.session_state.agent_logs = []


def display_header():
    """Display application header."""
    st.markdown('<div class="main-header">🤖 LangGraph Multi-Agent System</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Intelligent Research Automation with AI Agents</div>', unsafe_allow_html=True)

def sidebar_config():
    """Configure sidebar options."""
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # System selection
        system_type = st.radio(
            "Select Agent System:",
            ["Single Agent", "Multi-Agent"],
            help="Single Agent: Fast, simple tasks | Multi-Agent: Complex, comprehensive analysis"
        )
        
        st.divider()
        
        # Task configuration
        st.subheader("📋 Task Settings")
        
        task_preset = st.selectbox(
            "Preset Tasks:",
            [
                "Custom Task",
                "Research trending tech topics",
                "Analyze AI agent developments",
                "Compare LLM providers",
                "Evaluate new frameworks"
            ]
        )
        
        if task_preset == "Custom Task":
            custom_task = st.text_area(
                "Enter your task:",
                placeholder="e.g., Research the latest developments in quantum computing...",
                height=100
            )
            task = custom_task
        else:
            task = task_preset
        
        st.divider()
        
        # Advanced settings
        with st.expander("🔧 Advanced Settings"):
            max_topics = st.slider("Max Topics", 3, 10, 5)
            include_analysis = st.checkbox("Include Sentiment Analysis", value=True)
            verbose_output = st.checkbox("Verbose Logging", value=False)
        
        st.divider()
        
        # System info
        st.subheader("ℹ️ System Info")
        st.info(f"""
        **Model**: {settings.DEFAULT_MODEL}
        **Fast Model**: {settings.FAST_MODEL}
        **Max Retries**: {settings.max_retries}
        **Timeout**: {settings.timeout_seconds}s
        """)
        
        return {
            'system_type': system_type,
            'task': task,
            'max_topics': max_topics,
            'include_analysis': include_analysis,
            'verbose_output': verbose_output
        }

def run_single_agent(config):
    """Execute single agent workflow."""
    logger.info("Running single agent workflow")
    
    try:
        with st.spinner("🔄 Single agent processing..."):
            system = create_single_agent_system()
            
            result = system.invoke({
                "task": config['task'],
                "messages": []
            })
            
            return {
                'success': True,
                'result': result.get('result', 'No result'),
                'type': 'single'
            }
    
    except Exception as e:
        logger.error(f"Single agent error: {str(e)}")
        return {
            'success': False,
            'error': str(e),
            'type': 'single'
        }

def run_multi_agent(config):
    """Execute multi-agent workflow."""
    logger.info("Running multi-agent workflow")
    
    try:
        # Create progress indicators
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Initialize system
        status_text.text("🔧 Initializing multi-agent system...")
        progress_bar.progress(10)
        system = create_multi_agent_system()
        
        # Execute workflow
        status_text.text("🔬 Research team gathering trends...")
        progress_bar.progress(30)
        
        result = system.invoke({
            "current_task": config['task'],
            "messages": [],
            "research_notes": "",
            "trending_topics": [],
            "articles": [],
            "analysis_results": "",
            "patterns": [],
            "final_report": "",
            "next_agent": "researcher",
            "status": "started"
        })
        
        progress_bar.progress(100)
        status_text.text("✅ Analysis complete!")
        
        return {
            'success': True,
            'result': result.get('final_report', 'No report generated'),
            'research_notes': result.get('research_notes', ''),
            'analysis_results': result.get('analysis_results', ''),
            'trending_topics': result.get('trending_topics', []),
            'articles': result.get('articles', []),
            'type': 'multi'
        }
    
    except Exception as e:
        logger.error(f"Multi-agent error: {str(e)}")
        return {
            'success': False,
            'error': str(e),
            'type': 'multi'
        }

def display_results(result):
    """Display execution results."""
    if not result['success']:
        st.markdown('<div class="status-box error-box">❌ Error occurred</div>', unsafe_allow_html=True)
        st.error(f"**Error Details:** {result['error']}")
        return
    
    # Success indicator
    st.markdown('<div class="status-box success-box">✅ Task completed successfully!</div>', unsafe_allow_html=True)
    
    # Display results based on type
    if result['type'] == 'single':
        st.subheader("📄 Results")
        st.markdown(result['result'])
    
    else:  # Multi-agent
        # Create tabs for different outputs
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Final Report",
            "🔬 Research Notes",
            "📈 Analysis",
            "📚 Sources"
        ])
        
        with tab1:
            st.markdown("### Final Intelligence Report")
            st.markdown(result['result'])
            
            # Download button
            st.download_button(
                label="📥 Download Report",
                data=result['result'],
                file_name=f"research_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown"
            )
        
        with tab2:
            st.markdown("### Research Notes")
            if result.get('research_notes'):
                st.markdown(result['research_notes'])
            else:
                st.info("No research notes available")
        
        with tab3:
            st.markdown("### Analysis Results")
            if result.get('analysis_results'):
                st.markdown(result['analysis_results'])
            else:
                st.info("No analysis available")
            
            # Display trending topics if available
            if result.get('trending_topics'):
                st.markdown("#### 🔥 Trending Topics")
                for i, topic in enumerate(result['trending_topics'], 1):
                    st.markdown(f"{i}. {topic}")
        
        with tab4:
            st.markdown("### Source Articles")
            if result.get('articles'):
                for article in result['articles']:
                    with st.expander(f"📰 {article.get('title', 'Untitled')}"):
                        st.markdown(f"**Source:** {article.get('source', 'Unknown')}")
                        st.markdown(f"**Date:** {article.get('date', 'N/A')}")
                        st.markdown(f"**URL:** {article.get('url', 'N/A')}")
                        st.markdown(f"**Summary:** {article.get('summary', 'No summary available')}")
            else:
                st.info("No source articles available")

def display_history():
    """Display execution history."""
    if st.session_state.history:
        st.subheader("📜 Execution History")
        
        for i, item in enumerate(reversed(st.session_state.history[-5:]), 1):
            with st.expander(f"Run {len(st.session_state.history) - i + 1}: {item['timestamp']}"):
                st.markdown(f"**System:** {item['system_type']}")
                st.markdown(f"**Task:** {item['task']}")
                st.markdown(f"**Status:** {'✅ Success' if item['success'] else '❌ Failed'}")
                
                if item['success'] and item.get('summary'):
                    st.markdown(f"**Summary:** {item['summary'][:200]}...")

def main():
    """Main application entry point."""
    # Initialize
    initialize_session_state()
    
    # Display header
    display_header()
    
    # Get configuration
    config = sidebar_config()
    
    # Main content area
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("🎯 Task Configuration")
        st.info(f"**Selected Task:** {config['task']}")
        st.info(f"**System Type:** {config['system_type']}")
    
    with col2:
        execute_button = st.button("🚀 Execute", use_container_width=True, type="primary")
    
    # Execute on button click
    if execute_button:
        if not config['task'] or config['task'].strip() == "":
            st.warning("⚠️ Please enter a task description")
            return
        
        st.divider()
        st.subheader("⚙️ Execution")
        
        # Run appropriate system
        if config['system_type'] == "Single Agent":
            result = run_single_agent(config)
        else:
            result = run_multi_agent(config)
        
        # Store in session state
        st.session_state.current_result = result
        
        # Add to history
        st.session_state.history.append({
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'system_type': config['system_type'],
            'task': config['task'],
            'success': result['success'],
            'summary': result.get('result', '')[:200] if result['success'] else None
        })
        
        # Display results
        st.divider()
        display_results(result)
    
    # Display current result if available
    elif st.session_state.current_result:
        st.divider()
        st.subheader("📊 Last Execution Results")
        display_results(st.session_state.current_result)
    
    # Display history
    st.divider()
    display_history()
    
    # Footer
    st.divider()
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem;'>
        <p>🤖 LangGraph Multi-Agent System | Built with LangGraph 1.0 & Streamlit</p>
        <p>Powered by Groq (Llama Models) - Free & Fast AI</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

