from kedro.pipeline import node, Pipeline
from kedro.io import DataCatalog, MemoryDataSet
from kedro.runner import SequentialRunner
from kedro.extras.datasets.text import TextDataSet


# Prepare first node
def greeting():
    return "Hello"


greeting_node = node(func=greeting, inputs=None, outputs="my_greeting")


# Prepare second node


def greet_person(greeting, day):
    return f"{greeting} Kedro! on {day}"


greet_person_node = node(
    greet_person, inputs=["my_greeting", "day"], outputs="my_message"
)


# Run pipeline with MemoryDataSet

pipeline = Pipeline([greeting_node, greet_person_node])

# Use an in memory dataset

mds = MemoryDataSet(data="Tuesday")
data_catalog = DataCatalog({'day': mds})

runner = SequentialRunner()

print(runner.run(pipeline, data_catalog))

# Use a dataset from a text file

tds = TextDataSet(filepath='example-pipeline/day_text.txt')
data_catalog2 = DataCatalog({'day': tds})

print(runner.run(pipeline, data_catalog2))
