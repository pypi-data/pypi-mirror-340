import importlib

from openai import OpenAI

from test2va.mutation_predictor.config import gpt_config

SYSTEM_PROMPT = ("You are an expert in Android GUI testing and software automation. "
                 "Answer questions clearly and concisely. Provide detailed explanations if asked. "
                 "Focus on Espresso testing methods when dealing with Android UI tests.")
MODEL = "gpt-4o-2024-08-06"
TOKEN_LIMITATION = 1000

def get_response_from_gpt(user_prompt: str, output_format):

    print(user_prompt)

    importlib.reload(gpt_config)  # Reload the module if needed
    api_key = gpt_config.GPT_API_KEY

    client = OpenAI(
        # This is the default and can be omitted
        api_key=api_key
    )

    try:
        completion = client.beta.chat.completions.parse(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            response_format=output_format,
            max_tokens=TOKEN_LIMITATION
        )

        response = completion.choices[0].message
        if response.parsed:
            print(response.parsed)
        elif response.refusal:
            # handle refusal
            print(response.refusal)

        return response.content  # return the content

    except Exception as e:
        print(e)
        pass
