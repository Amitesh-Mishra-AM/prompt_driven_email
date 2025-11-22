import streamlit as st
import json
import os
import time 
from prompt_manager import PromptManager
from llm_service import process_email_with_llm, parse_json_output
st.set_page_config(page_title="Email Productivity Agent", layout="wide")

if "emails" not in st.session_state:
    try:
        with open("mock_inbox.json", "r") as f:
            st.session_state.emails = json.load(f)
    except FileNotFoundError:
        st.session_state.emails = []

if "prompt_manager" not in st.session_state:
    st.session_state.prompt_manager = PromptManager()
# --- Sidebar ---
with st.sidebar:
    st.title("⚙️ Agent Settings")
    if os.getenv("GEMINI_API_KEY"):
        st.success("✅ API Key Loaded")
    else:
        st.error("❌ API Key missing in .env")
    st.divider()
    st.subheader("🧠 Prompt Brain")
    pm = st.session_state.prompt_manager
    cat_prompt = st.text_area("Categorization Prompt", pm.get_prompt("categorization_prompt"), height=100)
    action_prompt = st.text_area("Action Extraction Prompt", pm.get_prompt("action_extraction_prompt"), height=100)
    if st.button("Save Prompts"):
        pm.update_prompt("categorization_prompt", cat_prompt)
        pm.update_prompt("action_extraction_prompt", action_prompt)
        st.toast("Prompts updated!")
# --- Main UI ---
st.title("📧 AI Email Agent")
tab1, tab2, tab3 = st.tabs(["📥 Inbox & Processing", "🤖 Email Agent Chat", "✍️ Draft Generator"])
# --- TAB 1: Inbox ---
with tab1:
    st.subheader("Inbox")
    
    if st.button("Run AI Processing"):
        progress_bar = st.progress(0)
        total_emails = len(st.session_state.emails)
        st.info("⏳1 email every 4s...")
        for index, email in enumerate(st.session_state.emails):
            cat_p = pm.get_prompt("categorization_prompt")
            category = process_email_with_llm(email['body'], cat_p)
            st.session_state.emails[index]['category'] = category
            act_p = pm.get_prompt("action_extraction_prompt")
            raw_action = process_email_with_llm(email['body'], act_p)
            action_data = parse_json_output(raw_action)
            st.session_state.emails[index]['action_items'] = action_data
            # Update Progress
            progress_bar.progress((index + 1) / total_emails)
            time.sleep(4) 
        st.success("Processing Complete!")
    for email in st.session_state.emails:
        with st.expander(f"{email['sender']} - {email['subject']}"):
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.write(f"**Body:** {email['body']}")
            with col_b:
                if 'category' in email:
                    st.info(f"📂 {email['category']}")
                if 'action_items' in email and isinstance(email['action_items'], dict):
                    task = email['action_items'].get('task')
                    deadline = email['action_items'].get('deadline')
                    if task:
                        st.warning(f"⚡ Task: {task}")
                        st.caption(f"📅 By: {deadline}")
# --- TAB 2: Chat Agent ---
with tab2:
    st.subheader("Chat with your Inbox")
    email_titles = [f"{e['id']} - {e['subject']}" for e in st.session_state.emails]
    selected_option = st.selectbox("Select Email context:", email_titles)
    selected_id = selected_option.split(" - ")[0]
    current_email = next((e for e in st.session_state.emails if e['id'] == selected_id), None)
    if current_email:
        st.text_area("Context Email:", current_email['body'], height=100, disabled=True)
        if "messages" not in st.session_state:
            st.session_state.messages = []
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        if prompt := st.chat_input("Ask the agent..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    instruction = f"User Query: {prompt}\nContext: {current_email['body']}"
                    response = process_email_with_llm("", instruction)
                    st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
# --- TAB 3: Draft Generator ---
with tab3:
    st.subheader("Auto-Draft Replies")
    draft_title = st.selectbox("Select Email to Reply:", [f"{e['id']} - {e['subject']}" for e in st.session_state.emails], key="draft_select")
    d_id = draft_title.split(" - ")[0]
    d_email = next((e for e in st.session_state.emails if e['id'] == d_id), None)
    if d_email:
        tone = st.selectbox("Select Tone:", ["Professional", "Casual", "Urgent"])
        custom_instr = st.text_input("Additional Instructions:", placeholder="e.g., I am busy until Tuesday")
        if st.button("Generate Draft"):
            with st.spinner("Writing draft..."):
                prompt = f"{pm.get_prompt('auto_reply_prompt')}\nTONE: {tone}\nEXTRA: {custom_instr}"
                draft_content = process_email_with_llm(d_email['body'], prompt)
                if "drafts" not in st.session_state:
                    st.session_state.drafts = {}
                st.session_state.drafts[d_id] = draft_content
                st.success("Draft Generated!")
        if "drafts" in st.session_state and d_id in st.session_state.drafts:
            st.text_area("Draft Body", st.session_state.drafts[d_id], height=200)
            st.button("Save Draft (Local)", key="save_draft_btn")