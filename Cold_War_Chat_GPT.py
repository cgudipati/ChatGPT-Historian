import tkinter as tk
from tkinter import messagebox
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI()

# Map simple labels to detailed system prompts
system_prompts = {
    "USA supporter": "You are an expert Cold War historian who strongly supports USA and hates USSR.",
    "Neutral expert": "You are an expert Cold War historian with a neutral view of both sides.",
    "USSR supporter": "You are an expert Cold War historian who strongly supports USSR and hates USA."
}

# Function to interact with OpenAI API
def query_chatgpt():
    user_prompt = user_input.get("1.0", tk.END).strip()
    selected_option = selected_expert.get()  # Get selected radio button value
    
    if len(user_prompt) > 250:
        messagebox.showerror("Input Error", "User input exceeds 250 characters.")
        return

    # Retrieve the full system prompt from the selected option
    system_prompt = system_prompts.get(selected_option, "Neutral expert")  # Default to neutral if not found

    # Add explicit instruction to limit response length
    system_prompt += " Please limit your response to under 100 words."

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        response_text.delete("1.0", tk.END)  # Clear previous response
        response_text.insert(tk.END, completion.choices[0].message.content)
    except Exception as e:
        messagebox.showerror("API Error", f"Error communicating with API: {str(e)}")

# Create main application window
root = tk.Tk()
root.title("Fireside Chat with Cold War Expert")
root.geometry("600x600")

# User input label and text box
tk.Label(root, text="Ask your Question: (Max 250 characters):").pack(pady=5)
user_input = tk.Text(root, height=5, wrap=tk.WORD)
user_input.pack(fill=tk.BOTH, padx=10, pady=5)

# Advanced prompting radio buttons
tk.Label(root, text="Choose your expert:").pack(pady=5)

# Create a variable to track selected option
selected_expert = tk.StringVar(value="Neutral expert")  # Default value

# Add radio buttons for options
for option in system_prompts.keys():
    tk.Radiobutton(root, text=option, variable=selected_expert, value=option).pack(anchor=tk.W, padx=10)

# Query button
query_button = tk.Button(root, text="Query Cold War Expert", command=query_chatgpt)
query_button.pack(pady=10)

# Response output label and text box
tk.Label(root, text="Response:").pack(pady=5)
response_text = tk.Text(root, height=15, wrap=tk.WORD)
response_text.pack(fill=tk.BOTH, padx=10, pady=5)

# Start the Tkinter event loop
root.mainloop()
