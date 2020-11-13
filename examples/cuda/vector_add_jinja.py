"""Minimal example of vector_add using a Jinja2 template"""

from kernel_tuner import tune_kernel
from jinja2 import Environment, FileSystemLoader
import json
import numpy


def generate_code(tuning_parameters):
    template_loader = FileSystemLoader(".")
    template_environment = Environment(loader=template_loader)
    template = template_environment.get_template("vector_add_jinja.cu")
    if tuning_parameters["vector_size"] == 1:
        vector_size = ""
    else:
        vector_size = str(tuning_parameters["vector_size"])
    return template.render(real_type=tuning_parameters["real_type"], vector_size=vector_size)


def tune():
    size = 10000000

    a = numpy.random.randn(size).astype(numpy.float32)
    b = numpy.random.randn(size).astype(numpy.float32)
    c = numpy.zeros_like(b)
    n = numpy.int32(size)

    args = [a, b, c, n]

    tuning_parameters = dict()
    tuning_parameters["real_type"] = ["float"]
    tuning_parameters["block_size_x"] = [32 * i for i in range(1, 33)]
    tuning_parameters["vector_size"] = [1]

    result = tune_kernel("vector_add", generate_code, size, args, tuning_parameters, lang="CUDA")

    with open("vector_add_jinja.json", 'w') as fp:
        json.dump(result, fp)

    return result


if __name__ == "__main__":
    tune()
