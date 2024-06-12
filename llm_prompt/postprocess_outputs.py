import re

LLM_LABEL_TO_LABEL_ID = {
    "food insecurity indirect": "food-sec",
    "food insecurity direct": "food-sec",
    "food security": "food-sec",
    "aid security": "aid-sec",
    "protection": "protection",
    "education security": "education",
    "health security": "health",
    "irrelevant": "irrelevant",
}
LABEL_ID_TO_LLM_LABEL = {v: k for k, v in LLM_LABEL_TO_LABEL_ID.items()}


def extract_between_tags(tag: str, string: str) -> list[str]:
    ext_list = re.findall(f"<{tag}>(.+?)</{tag}>", string, re.DOTALL)
    final_results = []
    for e in ext_list:
        if "," in e:
            for x in e.split(","):
                final_results.append(x.strip())
        else:
            final_results.append(e.strip())
    return final_results


def decode_pred(x):
    if x.lower() in LLM_LABEL_TO_LABEL_ID:
        decoded_pred = LLM_LABEL_TO_LABEL_ID[x.lower()]
    else:
        print(f"invalid: {x}")
        decoded_pred = "invalid"
    return decoded_pred


def postprocess_output(llm_response: str):
    predicted_category = extract_between_tags("event_category_name", llm_response)
    predicted_explanation = extract_between_tags("explanation", llm_response)

    return decode_pred(predicted_category), predicted_explanation
