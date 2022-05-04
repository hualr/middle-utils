import yaml


def read_yaml(yaml_file_path):
    with open(yaml_file_path, 'rb') as f:
        cf = yaml.safe_load(f.read())  # yaml.load(f.read())
    return cf

if __name__ == '__main__':
    cf = read_yaml("setting.yaml")
    print(cf)
