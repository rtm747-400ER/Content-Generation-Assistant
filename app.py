import streamlit as st
from core.model import generate_response
from core.memory import init_session, add_message, get_messages, clear_messages, get_api_ready_messages
from core.processors import build_prompt
from core.templates import get_template_categories, get_templates_in_category, get_template_data, fill_template
from utils.word_count import count_words, count_chars
from utils.file_ops import export_chat_as_txt, export_chat_as_md
from core.image_gen import ImageGenerator
import base64

# Page Config and Session State
st.set_page_config(page_title="AI Content Assistant", page_icon="✨", layout="wide")
with open("assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
init_session(st.session_state)
if "use_template" not in st.session_state: st.session_state.use_template = False
if "selected_template" not in st.session_state: st.session_state.selected_template = None
if "template_values" not in st.session_state: st.session_state.template_values = {}
if 'use_reference' not in st.session_state: st.session_state.use_reference = False
if 'reference_post' not in st.session_state: st.session_state.reference_post = ""

# Sidebar
with st.sidebar:
    st.title("⚙️ Settings")
    mode = st.radio("Select Mode", ["📝 Text", "🎨 Image"], horizontal=True)
    st.markdown("---")
    if mode == "📝 Text":
        st.subheader("Text Options")
        use_template = st.toggle("Use Prompt Template", value=st.session_state.use_template)
        st.session_state.use_template = use_template
        if not use_template:
            tone = st.selectbox("Tone",["Default", "Formal", "Casual", "Persuasive", "Humorous"])
            style = st.selectbox("Style",["Default", "Narrative", "Analytical", "Creative", "Technical", "Academic", "Shakespearean"])
            format_type = st.selectbox("Format",["Default", "Email", "LinkedIn Post", "Tweet / Thread", "Blog Post", "Journal / Diary Entry", "Story / Fiction", "Summary / Report"])
        else:
            tone, style, format_type = "Default", "Default", "Default"
        if use_template:
            st.markdown("---")
            st.subheader("Prompt Templates")
            categories = get_template_categories()
            selected_category = st.selectbox("Category", categories, index=0)
            templates_in_category = get_templates_in_category(selected_category)
            template_names = list(templates_in_category.keys())
            if template_names:
                selected_template_name = st.selectbox("Template", template_names, index=0)
                template_data = get_template_data(selected_category, selected_template_name)
                st.session_state.selected_template = {"category": selected_category, "name": selected_template_name, "data": template_data}
                current_template_key = f"{selected_category}_{selected_template_name}"
                if st.session_state.get("last_template_key") != current_template_key:
                    st.session_state.template_values = {}
                    st.session_state.last_template_key = current_template_key
            else:
                st.session_state.selected_template = None
        else:
            st.session_state.selected_template = None
            st.session_state.template_values = {}
    elif mode == "🎨 Image":
        st.subheader("Image Generation Mode")
        st.info("💡 Tip: Be descriptive in your prompts for better results!")
        st.markdown("**Examples:**\n- *A futuristic cityscape at sunset*\n- *A Mona Lisa styled potrait of a cat*\n- *A lion sitting on a tree in a dense forest*")
    st.markdown("---")
    st.title("🛠️ Tools")
    if st.button("Word Count"):
        full_text = " ".join([msg["content"] for msg in st.session_state.messages if msg["role"] == "assistant" and not str(msg.get("content", "")).startswith("IMGB::")])
        words, chars = count_words(full_text), count_chars(full_text)
        st.write(f"Words: {words} | Characters: {chars}")
    txt_data = export_chat_as_txt(st.session_state.messages)
    st.download_button("Download as TXT", txt_data, "chat_history.txt", "text/plain")
    md_data = export_chat_as_md(st.session_state.messages)
    st.download_button("Download as MD", md_data, "chat_history.md", "text/markdown")
    if st.button("Clear Chat"):
        clear_messages(st.session_state)
        st.rerun()


# Main App Layout
st.title("✨ AI Content Creation Assistant")

if mode == "📝 Text":
    # Template Builder and Chat Display logic
    if st.session_state.use_template and st.session_state.selected_template:
        st.markdown("### 🎯 Template Builder")
        template_data = st.session_state.selected_template["data"]
        placeholders = template_data.get("placeholders", [])
        if placeholders:
            st.markdown(f"**Template:** {st.session_state.selected_template['name']}")
            if len(placeholders) > 2:
                cols = st.columns(2)
                for i, placeholder in enumerate(placeholders):
                    label = placeholder.replace("_", " ").title()
                    with cols[i % 2]:
                        is_textarea = "description" in placeholder.lower() or "content" in placeholder.lower()
                        value = st.text_area(label, value=st.session_state.template_values.get(placeholder, ""), height=100, key=f"template_{placeholder}") if is_textarea else st.text_input(label, value=st.session_state.template_values.get(placeholder, ""), key=f"template_{placeholder}")
                    st.session_state.template_values[placeholder] = value
            else:
                for placeholder in placeholders:
                    label = placeholder.replace("_", " ").title()
                    is_textarea = "description" in placeholder.lower() or "content" in placeholder.lower()
                    value = st.text_area(label, value=st.session_state.template_values.get(placeholder, ""), height=100, key=f"template_{placeholder}") if is_textarea else st.text_input(label, value=st.session_state.template_values.get(placeholder, ""), key=f"template_{placeholder}")
                    st.session_state.template_values[placeholder] = value
            if all(st.session_state.template_values.get(p) for p in placeholders):
                if st.button("Generate from Template", type="primary"):
                    filled_template = fill_template(template_data["template"], **st.session_state.template_values)
                    system_msg = build_prompt("", tone=tone, style=style, format_type=format_type)[0]
                    clean_history = get_api_ready_messages(st.session_state)
                    template_prompt_msg = {"role": "user", "content": filled_template}
                    api_messages = [system_msg] + clean_history + [template_prompt_msg]
                    ai_reply = generate_response(api_messages)
                    add_message(st.session_state, "assistant", ai_reply, msg_type="text")
                    st.session_state.template_values = {}
                    st.rerun()
            else:
                st.info("👆 Fill in all fields above to generate content from the template.")
    chat_container = st.container()
    with chat_container:
        for idx, msg in enumerate(get_messages(st.session_state)):
            if msg.get("type", "text") != "text": continue
            ts, role_class = msg.get("timestamp", ""), "user-msg" if msg["role"] == "user" else "assistant-msg"
            st.markdown(f'<div class="{role_class}"><div class="msg-meta">[{ts}] {msg["role"].capitalize()}</div><div class="msg-content">{msg["content"]}</div></div>', unsafe_allow_html=True)
            if msg["role"] == "assistant":
                col1, col2, col3 = st.columns(3)
                system_msg = build_prompt("", tone=tone, style=style, format_type=format_type)[0]
                clean_history = get_api_ready_messages(st.session_state)
                with col1:
                    if st.button("🔄 Regenerate", key=f"regen_{idx}"):
                        prompt, api_messages = f"Regenerate: {msg['content']}", [system_msg] + clean_history + [{"role": "user", "content": prompt}]
                        new_reply = generate_response(api_messages)
                        st.session_state.messages[idx]["content"] = new_reply
                        st.rerun()
                with col2:
                    if st.button("➕ Expand", key=f"expand_{idx}"):
                        prompt, api_messages = f"Expand: {msg['content']}", [system_msg] + clean_history + [{"role": "user", "content": prompt}]
                        new_reply = generate_response(api_messages)
                        st.session_state.messages[idx]["content"] = new_reply
                        st.rerun()
                with col3:
                    if st.button("➖ Shorten", key=f"shorten_{idx}"):
                        prompt, api_messages = f"Shorten: {msg['content']}", [system_msg] + clean_history + [{"role": "user", "content": prompt}]
                        new_reply = generate_response(api_messages)
                        st.session_state.messages[idx]["content"] = new_reply
                        st.rerun()

    # Regular Chat Input
    if not (st.session_state.use_template and st.session_state.selected_template):
        st.session_state.use_reference = st.toggle("Add Reference Text", value=st.session_state.use_reference)
        if st.session_state.use_reference:
            st.session_state.reference_post = st.text_area(
                "PASTE REFERENCE TEXT HERE",
                value=st.session_state.reference_post,
                height=150,
                placeholder="Paste the text you want the AI to learn the style from..."
            )
            
            if st.session_state.reference_post:
                st.success("✅ Reference text captured! It will be applied to your next prompt.")
            else:
                st.info("💡 Paste your reference text above. The style will be applied automatically.")
        
        st.markdown("---") 
        
        user_input = st.chat_input("Type your message for text generation...")
        if user_input:
            ref_post = st.session_state.reference_post if st.session_state.use_reference else None
            
            system_msg, user_msg = build_prompt(user_input, tone=tone, style=style, format_type=format_type, reference_post=ref_post)

            add_message(st.session_state, "user", user_input, msg_type="text")
            
            clean_history = get_api_ready_messages(st.session_state)
            
            api_messages = [system_msg] + clean_history[:-1] + [user_msg]
            
            ai_reply = generate_response(api_messages)
            add_message(st.session_state, "assistant", ai_reply, msg_type="text")
            
            # Clear reference post after use for the next turn
            st.session_state.reference_post = ""
            st.session_state.use_reference = False
            st.rerun()

elif mode == "🎨 Image":
    # Image Mode logic
    image_chat_container = st.container()
    with image_chat_container:
        for idx, msg in enumerate(get_messages(st.session_state)):
            if msg.get("type", "text") != "image": continue
            ts, role_class = msg.get("timestamp", ""), "user-msg" if msg["role"] == "user" else "assistant-msg"
            if msg["role"] == "assistant" and str(msg.get("content", "")).startswith("IMGB::"):
                b64 = str(msg["content"])[6:]
                try:
                    img_bytes = base64.b64decode(b64)
                    st.markdown(f'<div class="{role_class}"><div class="msg-meta">[{ts}] Assistant</div></div>', unsafe_allow_html=True)
                    st.image(img_bytes, caption="Generated Image", use_container_width=True)
                    st.download_button("📥 Download Image", img_bytes, file_name=f"generated_{idx}.png", mime="image/png", key=f"download_{idx}")
                except Exception as e:
                    st.error(f"Error displaying image: {e}")
                continue
            st.markdown(f'<div class="{role_class}"><div class="msg-meta">[{ts}] {msg["role"].capitalize()}</div><div class="msg-content">{msg["content"]}</div></div>', unsafe_allow_html=True)

    image_prompt = st.chat_input("Describe the image you want to generate...")
    if image_prompt:
        add_message(st.session_state, "user", image_prompt, msg_type="image")
        try:
            with st.spinner("🎨 Generating your image..."):
                img_gen = ImageGenerator()
                results = img_gen.generate(image_prompt)
            if results:
                for img_bytes in results:
                    img_b64 = base64.b64encode(img_bytes).decode("utf-8")
                    add_message(st.session_state, "assistant", f"IMGB::{img_b64}", msg_type="image")
            else:
                add_message(st.session_state, "assistant", "⚠️ Failed to generate image.", msg_type="image")
        except Exception as e:
            add_message(st.session_state, "assistant", f"⚠️ Image generation error: {e}", msg_type="image")
        st.rerun()