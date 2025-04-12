from masint import SupermassiveIntelligence

from datetime import datetime

import logging

logger = logging.getLogger(__name__)


def ls(all):
    logger.debug(f"Listing models")

    try:
        llm = SupermassiveIntelligence()

        models = llm.list_models()
    except Exception as e:
        logger.error(f"Failed to list models")
        logger.error(e)

    if all:
        print_all_model_info(models["models"])
    else:
        print_models(models["models"])


def print_models(models):
    for model in models:
        print(model["name"])


def print_all_model_info(models):
    keys = models[0].keys()

    max_lengths = {key: len(key) for key in keys}

    for model in models:
        for key in keys:
            if 'time' in key:
                model[key] = datetime.fromtimestamp(model[key]).strftime('%Y-%m-%d %H:%M:%S')

    for model in models:
        for key, value in model.items():
            max_lengths[key] = max(max_lengths[key], len(str(value)))

    header = " | ".join(f"{key:<{max_lengths[key]}}" for key in keys)

    print(header)
    print("-" * len(header))
    for model in models:
        row = " | ".join(f"{str(model[key]):<{max_lengths[key]}}" for key in keys)
        print(row)
