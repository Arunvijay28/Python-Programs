import requests
import json
import streamlit as st

url = "http://localhost:11434/api/generate"

headers = {
    'Content-Type': 'application/json'
}

history = []

def generate_response(prompt):
    history.append(prompt)
    final_prompt = "\n".join(history)

    data = {
        "model": "isochamp",
        "prompt": final_prompt,
        "stream": True  # Assuming the backend can handle streaming
    }

    response = requests.post(url, headers=headers, data=json.dumps(data), stream=True)

    if response.status_code == 200:
        response_text = ""
        for chunk in response.iter_content(chunk_size=512):
            if chunk:
                decoded_chunk = chunk.decode('utf-8')
                data = json.loads(decoded_chunk)
                response_text += data.get('response', '')
                yield response_text  # Yield the partial response for streaming effect
    else:
        st.error(f"Error: {response.text}")
        return None

st.title("ISO Code-Pilot")

prompt = st.text_area("Enter your prompt", height=150)

if st.button("Generate Response"):
    if prompt:
        response_generator = generate_response(prompt)
        response_text = ""
        response_placeholder = st.empty()  # Create a placeholder

        for partial_response in response_generator:
            response_text = partial_response
            response_placeholder.text_area("Generated Response", value=response_text, height=150)
            st.markdown(
                """
                <script>
                var textarea = document.querySelector('textarea');
                if (textarea) {
                    textarea.scrollTop = textarea.scrollHeight;
                }
                </script>
                """, 
                unsafe_allow_html=True
            )
    else:
        st.warning("Please enter a prompt")
