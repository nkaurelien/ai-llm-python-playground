import json


def parse_faq(file_path, json_key, output_file):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    lines = text.strip().split('\n')
    current_question = ""
    current_answer = ""
    faq_list = []

    for line in lines:
        if (line and line[0].isdigit()) or line.endswith("?") or line.startswith("Prérequis") or line.startswith("Est-il")  or line.startswith("Pourquoi") or line.startswith("Quand")  or line.startswith("Combien") or line.startswith("Comment") or line.startswith("Existe-t-il"):
            if current_question and current_answer:
                faq_list.append({"question": current_question,
                                "answer": current_answer.strip()})
            current_question = line
            current_answer = ""
        else:
            if not line.startswith("Powered by Document360") and not line.startswith("Documentation") and not line.startswith("Page:") and not line.startswith("Documentation"):
                current_answer += " " + line

    if current_question and current_answer:
        current_question = current_question.replace("\f", "", 1)
        current_answer = current_answer.replace("\f", "", 1)
        faq_list.append({"question": current_question,
                        "answer": current_answer.strip().replace("\f", "", 1)})

    faq_json = {json_key: faq_list}

    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(faq_json, file, ensure_ascii=False, indent=4)

    return faq_json
