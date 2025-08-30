import streamlit as st
from core.model import generate_response
from core.memory import init_session, add_message, get_messages, clear_messages, get_api_ready_messages
from core.processors import build_prompt
from core.templates import get_template_categories, get_templates_in_category, get_template_data, fill_template
from utils.word_count import count_words, count_chars
from utils.file_ops import export_chat_as_txt, export_chat_as_md
from core.image_gen import ImageGenerator   # uses Cloudflare
import base64

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="AI Content Assistant",
    page_icon="✨",
    layout="wide",
)

# Load custom CSS
with open("assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# -------------------------------
# Session State Initialization
# -------------------------------
init_session(st.session_state)

# Initialize template session state
if "use_template" not in st.session_state:
    st.session_state.use_template = False
if "selected_template" not in st.session_state:
    st.session_state.selected_template = None
if "template_values" not in st.session_state:
    st.session_state.template_values = {}

# -------------------------------
# Sidebar Controls
# -------------------------------
st.sidebar.title("⚙️ Settings")

# Mode toggle - using select_slider for a cleaner look
mode = st.sidebar.select_slider(
    "Mode",
    options=["Text", "Image"],
    value="Text",
    format_func=lambda x: f"📝 {x}" if x == "Text" else f"🎨 {x}"
)

# Only show text generation options when in Text mode
if mode == "Text":
    st.sidebar.markdown("---")
    st.sidebar.subheader("📝 Text Options")
    
    tone = st.sidebar.selectbox(
        "Tone",
        ["Default", "Formal", "Casual", "Persuasive", "Humorous"]
    )

    style = st.sidebar.selectbox(
        "Style",
        ["Default", "Narrative", "Analytical", "Creative", "Technical", "Academic", "Shakespearean"]
    )

    format_type = st.sidebar.selectbox(
        "Format",
        [
            "Default",
            "Email",
            "LinkedIn Post",
            "Tweet / Thread",
            "Blog Post",
            "Journal / Diary Entry",
            "Story / Fiction",
            "Summary / Report"
        ]
    )
    
    # -------------------------------
    # Prompt Templates Section
    # -------------------------------
    st.sidebar.markdown("---")
    st.sidebar.subheader("🎯 Prompt Templates")
    
    use_template = st.sidebar.checkbox("Use Template", value=st.session_state.use_template)
    st.session_state.use_template = use_template
    
    if use_template:
        # Category selection
        categories = get_template_categories()
        selected_category = st.sidebar.selectbox(
            "Category",
            categories,
            index=0
        )
        
        # Template selection within category
        templates_in_category = get_templates_in_category(selected_category)
        template_names = list(templates_in_category.keys())
        
        if template_names:
            selected_template_name = st.sidebar.selectbox(
                "Template",
                template_names,
                index=0
            )
            
            template_data = get_template_data(selected_category, selected_template_name)
            
            # Show example
            if "example" in template_data:
                st.sidebar.markdown("**Example:**")
                st.sidebar.markdown(f"*{template_data['example']}*")
            
            st.session_state.selected_template = {
                "category": selected_category,
                "name": selected_template_name,
                "data": template_data
            }
            
            # Clear template values when template changes
            current_template_key = f"{selected_category}_{selected_template_name}"
            if st.session_state.get("last_template_key") != current_template_key:
                st.session_state.template_values = {}
                st.session_state.last_template_key = current_template_key
        else:
            st.session_state.selected_template = None
    else:
        st.session_state.selected_template = None
        st.session_state.template_values = {}

else:
    # Set defaults for image mode (not used but prevents errors)
    tone = "Default"
    style = "Default"
    format_type = "Default"
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("🎨 Image Options")
    st.sidebar.info("💡 Tip: Be descriptive in your prompts for better results!")
    st.sidebar.markdown("**Try prompts like:**")
    st.sidebar.markdown("• *A futuristic cityscape at sunset*")
    st.sidebar.markdown("• *A Mona Lisa styled potrait of a cat*")
    st.sidebar.markdown("• *A lion sitting on a tree in a dense forest*")

# -------------------------------
# Sidebar Tools
# -------------------------------
st.sidebar.markdown("---")
st.sidebar.title("🛠️ Tools")

if st.sidebar.button("📊 Word Count"):
    full_text = " ".join(
        [
            msg["content"]
            for msg in st.session_state.messages
            if msg["role"] == "assistant" 
            and not str(msg.get("content", "")).startswith(("IMG::", "IMGB::"))
        ]
    )
    words = count_words(full_text)
    chars = count_chars(full_text)
    st.sidebar.write(f"Words: {words} | Characters: {chars}")

# Export as TXT
txt_data = export_chat_as_txt(st.session_state.messages)
st.sidebar.download_button(
    label="📤 Download as TXT",
    data=txt_data,
    file_name="chat_history.txt",
    mime="text/plain"
)

# Export as MD
md_data = export_chat_as_md(st.session_state.messages)
st.sidebar.download_button(
    label="📤 Download as MD",
    data=md_data,
    file_name="chat_history.md",
    mime="text/markdown"
)

if st.sidebar.button("🗑️ Clear Chat"):
    clear_messages(st.session_state)
    st.rerun()

# -------------------------------
# Template Input Form (Main Area)
# -------------------------------
if mode == "Text" and st.session_state.use_template and st.session_state.selected_template:
    st.markdown("### 🎯 Template Builder")
    
    template_data = st.session_state.selected_template["data"]
    placeholders = template_data.get("placeholders", [])
    
    if placeholders:
        st.markdown(f"**Template:** {st.session_state.selected_template['name']}")
        
        # Create input fields for each placeholder
        if len(placeholders) > 2:
            cols = st.columns(2)
        
        for i, placeholder in enumerate(placeholders):
            # Convert placeholder to readable label
            label = placeholder.replace("_", " ").title()
            
            # Use columns only if we have more than 2 placeholders
            if len(placeholders) > 2:
                col = cols[i % 2]
                with col:
                    # Use appropriate input type
                    if "description" in placeholder.lower() or "content" in placeholder.lower():
                        value = st.text_area(
                            label,
                            value=st.session_state.template_values.get(placeholder, ""),
                            height=100,
                            key=f"template_{placeholder}"
                        )
                    else:
                        value = st.text_input(
                            label,
                            value=st.session_state.template_values.get(placeholder, ""),
                            key=f"template_{placeholder}"
                        )
            else:
                # Use full width for 2 or fewer placeholders
                if "description" in placeholder.lower() or "content" in placeholder.lower():
                    value = st.text_area(
                        label,
                        value=st.session_state.template_values.get(placeholder, ""),
                        height=100,
                        key=f"template_{placeholder}"
                    )
                else:
                    value = st.text_input(
                        label,
                        value=st.session_state.template_values.get(placeholder, ""),
                        key=f"template_{placeholder}"
                    )
            
            st.session_state.template_values[placeholder] = value
        
        # Preview filled template
        if all(st.session_state.template_values.get(p) for p in placeholders):
            filled_template = fill_template(template_data["template"], **st.session_state.template_values)
            
            with st.expander("👀 Preview Template", expanded=False):
                st.markdown(f"```\n{filled_template}\n```")
            
            # Generate button
            if st.button("🚀 Generate from Template", type="primary"):
                add_message(st.session_state, "user", filled_template)
                
                system_msg = build_prompt("", tone=tone, style=style, format_type=format_type)[0]
                clean_history = get_api_ready_messages(st.session_state)
                api_messages = [system_msg] + clean_history
                ai_reply = generate_response(api_messages)
                add_message(st.session_state, "assistant", ai_reply)
                
                # Reset template form
                st.session_state.template_values = {}
                st.rerun()
        else:
            st.info("👆 Fill in all fields above to preview and generate content")

# -------------------------------
# Chat Display
# -------------------------------
st.title("✨ AI Content Creation Assistant")

# Show current mode indicator
mode_emoji = "📝" if mode == "Text" else "🎨"
st.markdown(f"**Current Mode:** {mode_emoji} {mode} Generation")

chat_container = st.container()

with chat_container:
    for idx, msg in enumerate(get_messages(st.session_state)):
        ts = msg.get("timestamp", "")
        role_class = "user-msg" if msg["role"] == "user" else "assistant-msg"

        # --- Cloudflare image (base64) ---
        if msg["role"] == "assistant" and str(msg.get("content", "")).startswith("IMGB::"):
            b64 = str(msg["content"])[6:]
            img_bytes = base64.b64decode(b64)

            st.markdown(
                f"""
                <div class="{role_class}">
                    <div class="msg-meta">[{ts}] Assistant</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.image(img_bytes, caption="Generated Image", use_container_width=True)
            st.download_button("📥 Download Image", img_bytes, file_name=f"generated_{idx}.png", mime="image/png")
            continue

        # --- Regular text ---
        st.markdown(
            f"""
            <div class="{role_class}">
                <div class="msg-meta">[{ts}] {msg['role'].capitalize()}</div>
                <div class="msg-content">{msg['content']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Editing options only for assistant text messages (and only in text mode)
        if msg["role"] == "assistant" and not msg["content"].startswith(("IMG::", "IMGB::")) and mode == "Text":
            col1, col2, col3 = st.columns(3)
            system_msg = build_prompt("", tone=tone, style=style, format_type=format_type)[0]
            clean_history = get_api_ready_messages(st.session_state)

            with col1:
                if st.button("🔄 Regenerate", key=f"regen_{idx}"):
                    prompt = f"Regenerate this response:\n\n{msg['content']}"
                    api_messages = [system_msg] + clean_history + [{"role": "user", "content": prompt}]
                    new_reply = generate_response(api_messages)
                    st.session_state.messages[idx]["content"] = new_reply
                    st.rerun()
            with col2:
                if st.button("➕ Expand", key=f"expand_{idx}"):
                    prompt = f"Expand this response with more detail:\n\n{msg['content']}"
                    api_messages = [system_msg] + clean_history + [{"role": "user", "content": prompt}]
                    new_reply = generate_response(api_messages)
                    st.session_state.messages[idx]["content"] = new_reply
                    st.rerun()
            with col3:
                if st.button("➖ Shorten", key=f"shorten_{idx}"):
                    prompt = f"Shorten this response while keeping meaning clear:\n\n{msg['content']}"
                    api_messages = [system_msg] + clean_history + [{"role": "user", "content": prompt}]
                    new_reply = generate_response(api_messages)
                    st.session_state.messages[idx]["content"] = new_reply
                    st.rerun()

# -------------------------------
# Chat / Image Input
# -------------------------------
# Only show regular chat input if not using templates
if not (mode == "Text" and st.session_state.use_template and st.session_state.selected_template):
    if mode == "Text":
        placeholder_text = "Type your message for text generation..."
    else:
        placeholder_text = "Describe the image you want to generate..."

    user_input = st.chat_input(placeholder_text)

    if user_input:
        add_message(st.session_state, "user", user_input)

        if mode == "Text":
            # ---- TEXT MODE ----
            system_msg = build_prompt("", tone=tone, style=style, format_type=format_type)[0]
            clean_history = get_api_ready_messages(st.session_state)
            api_messages = [system_msg] + clean_history
            ai_reply = generate_response(api_messages)
            add_message(st.session_state, "assistant", ai_reply)

        else:
            # ---- IMAGE MODE ----
            try:
                img_gen = ImageGenerator()
                results = img_gen.generate(user_input)
                if results:
                    for img_bytes in results:
                        img_b64 = base64.b64encode(img_bytes).decode("utf-8")
                        add_message(st.session_state, "assistant", f"IMGB::{img_b64}")
                else:
                    add_message(st.session_state, "assistant", "⚠️ Failed to generate image.")
            except Exception as e:
                add_message(st.session_state, "assistant", f"⚠️ Image gen error: {e}")

        st.rerun()