from kedro.pipeline import node, Pipeline
from kedro.io import DataCatalog, MemoryDataSet
from kedro.runner import SequentialRunner

from kedro.framework.session import KedroSession
from kedro.framework.startup import bootstrap_project

from pathlib import Path


SCRIPT_DIR = Path(__file__).parent.resolve()

project_root = (SCRIPT_DIR / ".." / "..").resolve()


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

metadata = bootstrap_project(project_root)

# loads yml files from ./conf/base and ./conf/local
with KedroSession.create(
    metadata.package_name, project_path=project_root
) as session:
    print('load context')
    context = session.load_context()
    print('catalog')
    print(context.catalog.list())  # loaded from catalog.yml
    print('context')
    print(context.params)  # loaded from parameters.yml

    # Run pipeline with MemoryDataSet
    pipeline = Pipeline([greeting_node, greet_person_node])
    mds = MemoryDataSet(data="Tuesday")
    data_catalog = DataCatalog({'day': mds})

    runner = SequentialRunner()
    # print(runner.run(pipeline, data_catalog))
    print(runner.run(pipeline, context.catalog))

    # uncomment the following line to run the pipelines in the session
    # session.run()
