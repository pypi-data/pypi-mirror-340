import yaml


def load_yaml_file(dir):
    try:
        with open(dir, "r", encoding="utf-8") as file:
            # return yaml.load(file, Loader=yaml.FullLoader)
            return yaml.safe_load(file)
    except FileNotFoundError as e:
        print(e)
        return None


def doc_constructor(template_dir: str, data_dir: str):
    # Add a yaml constructor
    def placeholder_constructor(loader, node):
        key = loader.construct_scalar(node)
        return data_dict.get(key, {})

    doc = {}

    # Load data dict
    data_dict = load_yaml_file(data_dir)
    if data_dict is not None:
        yaml.add_constructor("!placeholder", placeholder_constructor)

        # Open template file
        with open(template_dir, "r", encoding="utf-8") as template:
            doc = yaml.load(template, Loader=yaml.FullLoader)
            # doc = yaml.safe_load(template)

    return doc


if __name__ == "__main__":
    d1 = doc_constructor(
        template_dir="../app/api/doc/template.yaml", data_dir="test.yaml"
    )
    print(d1)
