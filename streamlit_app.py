import openai
import streamlit as st

# Set your OpenAI API key
openai.api_key = "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"

# Initial system message
messages = [{"role": "system", "content": "You are a helpful assistant capable of providing information and assistance."}]

# Definitions for specific terms
definitions = {
    "palindrome number": "A palindrome number is a number that reads the same backward as forward.",
    "fibonacci series": "A Fibonacci series is a series of numbers in which each number is the sum of the two preceding ones.",
    # Add more definitions as needed
}

# Function to check if a number is negative
def is_negative_number(number):
    try:
        return int(number) < 0
    except ValueError:
        return False

# Function to extract a number from the user query
def extract_number_from_query(user_input, default_value=None):
    number = next((word for word in user_input.split() if (word.replace('-', '')).isdigit()), None)
    return int(number) if number else default_value

# Function to check for non-negative number scenarios
def is_non_negative_number_for_special_cases(user_input):
    special_keywords = ["natural numbers", "prime numbers", "triangular numbers", "perfect numbers",
                         "factorial numbers", "perfect square numbers", "happy numbers",
                         "fibonacci numbers", "abundant numbers", "powerful numbers", "cube-free numbers", "palindrome numbers"]

    words = user_input.lower().split()
    for keyword in special_keywords:
        if keyword in words:
            for word in words:
                if word.replace('-', '').isdigit() and int(word) < 0:
                    return True
    return False

# Function to handle negative number scenarios
def handle_negative_number_request(user_input):
    return "Negative numbers can't be taken for this scenario."

# Function to handle palindrome number queries
def handle_palindrome_number_request(user_input):
    number = next((word for word in user_input.split() if (word.replace('-', '')).isdigit()), None)
    if number is not None and is_negative_number(number):
        return handle_negative_number_request(user_input)
    return f"A palindrome number is a number that reads the same backward as forward. {number} is {'' if str(number) == str(number)[::-1] else 'not '}a palindrome number."

# Function to handle happy number queries
def handle_happy_numbers_request(user_input):
    number = next((word for word in user_input.split() if (word.replace('-', '')).isdigit()), None)
    if number is not None and is_negative_number(number):
        return handle_negative_number_request(user_input)
    return f"{number} is {'' if is_happy_number(int(number)) else 'not '}a happy number."

# Function to handle non-negative number requests
def handle_non_negative_number_request(user_input):
    return "Negative numbers won't work for these scenarios."

# Function to check if a digit is present in the input
def is_digit_present(user_input):
    return any(char.isdigit() for char in user_input)

# Main function to interact with the ChatGPT model
def CustomChatGPTs(user_input):
    messages.append({"role": "user", "content": user_input})
    
    if is_digit_present(user_input):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
        except openai.error.OpenAIError as e:
            return f"An error occurred: {e}"

        ChatGPT_reply = response["choices"][0]["message"]["content"]
        messages.append({"role": "assistant", "content": ChatGPT_reply})
        if is_non_negative_number_for_special_cases(ChatGPT_reply):
            return handle_non_negative_number_request(ChatGPT_reply)

        return ChatGPT_reply
    
    if any(keyword in user_input.lower() for keyword in ["what is a", "define", "definition of", "what is", "is"]):
        term = next((word for word in user_input.lower().split() if word in definitions), None)
        if term:
            definition_response = definitions.get(term, "I don't have a definition for that term.")
            messages.append({"role": "assistant", "content": definition_response})
            return definition_response
    
    elif any(keyword in user_input.lower() for keyword in ["numbers", "number", "numeric", "numerical", "series", "give code", "generate code", "write code", "code"]):
        messages.append({"role": "assistant", "content": "Sure! What number should I take?"})
        return "Sure! What number should I take?"
    
    elif "palindrome" in user_input.lower():
        return handle_palindrome_number_request(user_input)

    elif "happy numbers" in user_input.lower():
        return handle_happy_numbers_request(user_input)
    
    elif is_non_negative_number_for_special_cases(user_input):
        return handle_non_negative_number_request(user_input)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
    except openai.error.OpenAIError as e:
        return f"An error occurred: {e}"

    ChatGPT_reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": ChatGPT_reply})
    if is_non_negative_number_for_special_cases(ChatGPT_reply):
        return handle_non_negative_number_request(ChatGPT_reply)

    return ChatGPT_reply

# Streamlit app interface
st.title("Chatbot")
user_input = st.text_input("You:", "")

if st.button("Send"):
    if user_input:
        response = CustomChatGPTs(user_input)
        st.text_area("Bot:", value=response, height=200)

st.write("Welcome to the Streamlit chatbot! Type your message and click 'Send' to interact.")
