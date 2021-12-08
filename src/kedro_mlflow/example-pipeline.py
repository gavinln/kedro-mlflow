from kedro.pipeline import node, Pipeline
from kedro.io import DataCatalog, MemoryDataSet
from kedro.runner import SequentialRunner


# Prepare first node
def return_greeting():
    return "Hello"


return_greeting_node = node(
    func=return_greeting, inputs=None, outputs="my_salutation"
)

# Prepare second node
def join_statements(greeting):
    return f"{greeting} Kedro!"


join_statements_node = node(
    join_statements, inputs="my_salutation", outputs="my_message"
)


pipeline = Pipeline([return_greeting_node, join_statements_node])

data_catalog = DataCatalog({"my_salutation": MemoryDataSet()})

runner = SequentialRunner()

print(runner.run(pipeline, data_catalog))
