import openai
import streamlit as st

# Retrieve the GPT API key from secrets
api_key = st.secrets["api_keys"]["openai_api_key"]

# Set the API key for OpenAI's client
openai.api_key = api_key

# Define model parameters with significant adjustments
MODEL_PARAMETERS = {
    "1": {
        "description": "LLM Lev1 Modified Model",
        "temperature": 0.1,
        "frequency_penalty": 0.0,
        "max_tokens": 250,
        "top_p": 0.1,
        "presence_penalty": 0.0,
        "logit_bias": {}
    },
    "2": {
        "description": "LLM Lev2 Modified Random Variation",
        "temperature": 0.5,
        "frequency_penalty": 0.5,
        "max_tokens": 150,
        "top_p": 0.6,
        "presence_penalty": 0.5,
        "logit_bias": {}
    },
    "3": {
        "description": "LLM Lev5 Modified Model",
        "temperature": 1.2,
        "frequency_penalty": 0.9,
        "max_tokens": 100,
        "top_p": 1.0,
        "presence_penalty": 1.0,
        "logit_bias": {}
    },
    "4": {
        "description": "LLM HM - my Zero GPT ",
        "temperature": 0.3,
        "frequency_penalty": 1.2,
        "max_tokens": 150,
        "top_p": 1.0,
        "presence_penalty": 1.0,
        "logit_bias": {}
    },
}

# Function to generate content based on the subject, model choice, and task choice
def generate_content(subject, model_choice, task_choice):
    # Get parameters for the selected model
    params = MODEL_PARAMETERS.get(model_choice, MODEL_PARAMETERS["1"])  # Default to model 1 if invalid choice

    # Create the messages based on task_choice, keeping prompts minimal
    

    # Adjust parameters based on task_choice to encourage appropriate behavior
    if task_choice == "Enter Text to Refine":
        messages = [{"role": "user", "content": "please rewrite this using the parameteres given to you "+subject}]
        # For refining text, set parameters to make output more deterministic and focused
        # You can adjust these values as needed
        params['temperature'] = min(params['temperature'], 0.3)
        params['top_p'] = min(params['top_p'], 0.5)
        params['frequency_penalty'] = 0.0
        params['presence_penalty'] = 0.0
        params['max_tokens'] = min(params['max_tokens'], 150)
    else:
        messages = [{"role": "user", "content": "please either generate or answer the following question using the parameteres given to you "+subject}]
        # For refining text, set parameters to make output more deterministic and focused
        # You can adjust these values as needed
        params['temperature'] = min(params['temperature'], 0.3)
        params['top_p'] = min(params['top_p'], 0.5)
        params['frequency_penalty'] = 0.0
        params['presence_penalty'] = 0.0
        params['max_tokens'] = min(params['max_tokens'], 150)
        # For generating new text, keep parameters as specified
        pass  # No changes
    if model_choice=="4":
        if task_choice == "Enter Text to Refine":
            messages= [{"role": "user", "content": " please rewrite this using the parameteres given to you, but use short sentences and avoid using AI predictable structures and use a high readabilty measure and of course do not reduce the size"+subject}]
        else:
            messages=[{"role": "user", "content": " please generate or answer the following question using the parameters given to you , but use short sentences and avoid using AI predictable structures and use a high readabilty measure"+subject}]
        
    # Generate content with the specified parameters
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",  # Ensure you're using the correct model name
        messages=messages,
        temperature=params["temperature"],
        max_tokens=params["max_tokens"],
        top_p=params["top_p"],
        frequency_penalty=params["frequency_penalty"],
        presence_penalty=params["presence_penalty"],
        logit_bias=params["logit_bias"]
        )
    print("blabla",messages,params["temperature"],params["top_p"])
    

    return response.choices[0].message['content'].strip()

# Streamlit interface
def main():
    st.markdown("""<h2 style='text-align: center; font-size: 20px;'>Interactive AI Text Generation & Refinement Tool</h2>
<p style='text-align: center; font-size: 14px;'>[Beta Version]  by Alphanumeric - Mahsa Kia</p>""", unsafe_allow_html=True)

    # Option to choose between text refinement and text generation
    task_choice = st.selectbox("Choose Task", ("Enter Text to Refine", "Generate New Text"))

    # Text input area based on the task choice
    if task_choice == "Enter Text to Refine":
        subject = st.text_area("Enter the text you want to refine:")
    else:
        subject = st.text_input("Enter the subject you want information on:")

    # Model selection options based on the model parameters defined
    model_descriptions = [f"{key}: {value['description']}" for key, value in MODEL_PARAMETERS.items()]
    model_choice = st.selectbox("Select Model", model_descriptions)

    # Extract the model number from the selected option
    model_choice_number = model_choice.split(":")[0].strip()

    # Button to generate content
    if st.button("Generate Content"):
        if subject:
            with st.spinner("Generating..."):
                output = generate_content(subject, model_choice_number, task_choice)
                st.subheader("Generated Output:")
                st.write(output)
        else:
            st.warning("Please enter a subject or text.")

    # Button to clear input and output
    if st.button("Clear All"):
        st.experimental_rerun()

if __name__ == "__main__":
    main()





#======================================-

#temperature = X

#Role:
#Controls the randomness of the output. A higher temperature makes the response more creative and varied, while a lower temperature makes it more focused and deterministic.
#Min/Max Values:
#Commonly ranges from 0.0 to 1.0 (can go higher for extreme randomness).
#Impact:
#0.0: The model produces very deterministic responses, often repeating the most likely words.
#1.0 or higher: The model becomes more random and creative, potentially incoherent if set too high.
#Example:
#temperature = 0.7 strikes a balance between creativity and coherence.

#======================================-

#frequency_penalty = X

#Role:
#Penalizes the model for using the same words repeatedly, which encourages more varied word choice.
#Min/Max Values:
#Usually ranges from 0.0 to 2.0.
#Impact:
#0.0: No penalty; words can be repeated freely.
#2.0: Strong penalty; the model avoids word repetition, possibly at the cost of natural flow.
#Example:
#frequency_penalty = 0.5 moderately discourages repetition for more varied responses.

#======================================-

#presence_penalty = X

#Role:
#Encourages the model to bring new topics or ideas into the response, avoiding sticking to the same theme or subject.
#Min/Max Values:
#Typically between 0.0 and 2.0.
#Impact:
#0.0: No encouragement for new topics; the model may stay focused on a single idea.
#2.0: Strong encouragement for introducing new content, which might cause off-topic shifts.
#Example:
#presence_penalty = 0.3 slightly pushes for fresh content.

#======================================-

#top_p = X

#Role:
#Implements nucleus sampling, where only the most probable words (cumulative probability ≤ top_p) are considered.
#This affects the diversity of the output.
#Min/Max Values:
#Between 0.0 and 1.0.
#Impact:
#0.1: Limited to very high-probability choices, leading to deterministic responses.
#0.9: Includes a wider set of words for richer and more varied output.
#Example:
#top_p = 0.9 allows for high diverse and creative responses while maintaining a certain focus.
#Adjusting top_p allows you to fine-tune how creative or conservative you want the generated response to be.

#======================================-

#max_tokens = X

#Role:
#Sets the maximum number of tokens (words or word parts) the response can include.
#Min/Max Values:
#From 1 to the maximum context limit of the model (e.g., 2048 or 4096 tokens).
#Impact:
#Low values (e.g., 10-50): Short responses, suitable for concise answers.
#High values (e.g., 500-1000): Longer and more detailed responses.
#Example:
#max_tokens = 50 limits responses to be relatively short.

#======================================-

#stop_sequences = X

#Role:
#Specifies sequences of characters or tokens at which the model stops generating text.
#Common Values: Usually a new line ("\n") or a specific keyword.
#Impact:
#Effectiveness: Ensures the response ends cleanly at a desired point.
#Example: stop_sequences = ["\n"] ends the output when a new line is generated

#======================================-

#logit_bias = X

#Role:
#Adjusts the likelihood of specific tokens being generated by applying positive or negative bias.
#Min/Max Values: Range from -100 to 100.
#Impact:
#Negative bias (e.g., -100): Strongly discourages or blocks certain tokens.
#Positive bias (e.g., +100): Increases the likelihood of specific tokens appearing.
#Example: logit_bias = {"50256": -100} discourages the use of token ID 50256,
    #which is often used for special tokens like <|endoftext|>.

    #Avoid Certain Words:
    #If you don’t want specific words or phrases (e.g., sensitive terms or outdated language) to appear in the response,
    #a negative bias can help prevent that.
    #Emphasize Certain Words:
    #If you're writing a piece that requires a specific tone or vocabulary,
    #a positive bias can make the model use those preferred words more often.

#======================================-

#temperature_decay = X

#Role:
#Reduces the temperature across successive calls, potentially making later responses more focused.
    #This means that each response from the model can become less random and more focused over time.
#Common Values: Typically 1.0 (no decay) or less for gradual reduction.
#Impact:
#1.0: No change in temperature across calls.
#<1.0: Temperature decreases, leading to progressively more deterministic outputs.

#======================================-

#batch_size = X

#Role:
#Specifies the number of responses generated in one call.
#Min/Max Values: Usually starts at 1, can go higher if needed.
#Impact:
#1: One response per request.
#Higher values: Multiple responses for comparison.

#======================================-

#context_window = X

#Role:
#The maximum number of tokens the model can consider as input context, including both the input and the response.
#Common Value:
#Often 2048 or 4096 tokens (model-dependent).
#Impact:
#Larger context window: More text can be used for context, allowing for detailed, coherent outputs.

#======================================-

#ethical_filter = X

#Role:
#Enables or disables a filter for removing potentially harmful or inappropriate content.
#Values: True (enabled) or False (disabled).
#Impact:
#True: Responses are more controlled to avoid unethical or inappropriate content.
#False: Full freedom in responses, with no ethical filtering applied.

#======================================-

    
