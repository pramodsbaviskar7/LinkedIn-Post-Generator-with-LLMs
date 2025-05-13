from llm_helper import llm
from few_shot import FewShotPosts

few_shot = FewShotPosts()

def get_length_str(length):
    if length == "Short":
        return "1 to 8 lines"
    if length == "Medium":
        return "8 to 13 lines"
    if length == "Long":
        return "13 to 18 lines"


def generate_post(length, language, tag, tone=None, creativity=None, hashtags=None):
    prompt = get_prompt(length, language, tag, tone, hashtags)

    try:
        prompt = prompt.encode("utf-8", errors="replace").decode("utf-8")
    except UnicodeEncodeError as e:
        print(f"Encoding error: {e}")
        return "An error occurred while preparing the prompt."

    # Apply temperature if provided
    if creativity is not None:
        response = llm.invoke(prompt, temperature=creativity)
    else:
        response = llm.invoke(prompt)

    return response.content


def get_prompt(length, language, tag, tone=None, hashtags=None):
    length_str = get_length_str(length)

    prompt = f'''
Generate a LinkedIn post using the below information. No preamble.

1) Topic: {tag}
2) Length: {length_str}
3) Language: {language}
'''

    if tone:
        prompt += f'4) Tone/Intent: {tone}\n'

    prompt += '''
If Language is Hinglish then it means it is a mix of Hindi and English.
The script for the generated post should always be English.
'''

    if hashtags:
        if hashtags == "AUTO":
            prompt += "Also include relevant, trending hashtags at the end of the post.\n"
        else:
            prompt += f"Use the following hashtags at the end: {hashtags}\n"
    else:
        prompt += "Add suitable hashtags based on the topic.\n"

    # Add few-shot examples
    examples = few_shot.get_filtered_posts(length, language, tag)
    if len(examples) > 0:
        prompt += "Use the writing style as per the following examples:\n"

    for i, post in enumerate(examples[:2]):  # Max 2 examples
        post_text = post['text']
        prompt += f'\nExample {i+1}:\n\n{post_text}\n'

    return prompt


if __name__ == "__main__":
    print(generate_post("Medium", "English", "Mental Health", tone="Inspirational", creativity=0.8, hashtags="#MentalHealth #Wellbeing"))
