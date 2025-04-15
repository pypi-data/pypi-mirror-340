from django.conf import settings


def build_semantic_summary(document_dict, filtered_data):
    embedding_data = {}

    for filter in getattr(settings, "SEMANTIC_SEARCH_ADDITIONAL_FILTERS", []):
        embedding_data[filter.name()] = filter.document_value(document_dict)

    embedding_data.update(filtered_data)

    data_text = ""
    for name, value in embedding_data.items():
        name = name.replace("_", " ")
        if isinstance(value, list):
            for v in value:
                data_text += f"{name} is {v}. "
        elif value:
            data_text += f"{name} is {value}. "

    return data_text
