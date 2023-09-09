from collections import Counter


def remove_neg_objects(input_dict: dict) -> dict:
    modified_dict = {}
    neg_lines = []
    for key, value in input_dict.items():
        if "--neg" in value:
            parts = value.split("--neg")
            modified_dict[key] = parts[0].strip()

            neg_lines.append(parts[1].strip())
        else:
            modified_dict[key] = value

    neg_line_counts = Counter(neg_lines)
    most_common_neg_line = neg_line_counts.most_common(1)

    if most_common_neg_line and most_common_neg_line[0][1] == len(neg_lines):
        return modified_dict, most_common_neg_line[0][0]
    else:
        return modified_dict, neg_lines
