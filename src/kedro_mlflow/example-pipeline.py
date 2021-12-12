from kedro.pipeline import node, Pipeline
from kedro.io import DataCatalog, MemoryDataSet
from kedro.runner import SequentialRunner


# Prepare first node
def greeting():
    return "Hello"


greeting_node = node(func=greeting, inputs=None, outputs="my_greeting")

# Run first node
print(greeting_node.run())


# Prepare second node


def greet_person(greeting, day):
    return f"{greeting} Kedro! on {day}"


greet_person_node = node(
    greet_person, inputs=["my_greeting", "day"], outputs="my_message"
)


# Run second node with different inputs
print(greet_person_node.run(dict(my_greeting="Hello", day="Tuesday")))
print(greet_person_node.run(dict(my_greeting="Hi", day="Tuesday")))
