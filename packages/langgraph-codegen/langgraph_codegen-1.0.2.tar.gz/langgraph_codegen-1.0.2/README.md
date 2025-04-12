# langgraph-codegen
##### Overview

**lgcodegen** allows a langraph specification entirely in terms of class names and function names.  It will generate those if necessary, resulting in a runnable graph.

Here's the graphs from Lance-from-Langchain "Building Effective Agents" video:

```
# Agent
MessagesState -> llm_call
llm_call -> should_continue(environment, END)
environment -> llm_call
```

```
# Evaluator Optimizer
State -> llm_call_generator
llm_call_generator -> llm_call_evaluator
llm_call_evaluator -> route_joke(END, llm_call_generator)
```

```
# Orchestrator Worker
State -> orchestrator
orchestrator -> llm_call(State.sections)
llm_call -> synthesizer
synthesizer -> END
```

```
# Parallelization
State -> call_llm_1, call_llm_2, call_llm_3
call_llm_1, call_llm_2, call_llm_3 -> aggregator
aggregator -> END
```

```
# Prompt Chaining
State -> generate_joke
generate_joke -> check_punchline(improve_joke, END)
improve_joke -> polish_joke
polish_joke -> END
```

These convert into runnable code with:
```
lgcodegen graph_spec.txt --code
```

This command creates a folder "graph_spec" (taken from file name), and writes "graph_spec.py" in the folder.  The py file contains the graph State class, all Node and Condition classes.  

##### Quick Start

To generate a graph from examples:

```bash
# View available example graphs, 'plan_and_execute' is one of the examples
lgcodegen --list

# View contents of a graph file
lgcodegen plan_and_execute

# Generate different components
lgcodegen --graph plan_and_execute    # Generate graph code
lgcodegen --nodes plan_and_execute    # Generate node code
lgcodegen --conditions plan_and_execute    # Generate condition code
lgcodegen --state plan_and_execute    # Generate state code

# complete running graph with mocked nodes, state, conditions
# Runnable code in: plan_and_execute/plan_and_execute.py
lgcodegen plan_and_execute --code
python plan_and_execute/plan_and_execute.py
```

##### Running mock graph

Starting with only this graph:

```bash
(py312) johannesjohannsen@Johanness-MacBook-Pro tests % lgcodegen plan_and_execute
LangGraph CodeGen v0.1.26
# Plan and Execute Agent
START(PlanExecute) => plan_step

plan_step => execute_step

execute_step => replan_step

replan_step
  is_done => END
  => execute_step
```

We generate the graph nodes and conditions, these go into a folder with the same name as the graph.  All the python code (state, nodes, conditions, main) go into a single python file.   Running that file invokes the graph.

```bash
(py312) johannesjohannsen@Johanness-MacBook-Pro langgraph-codegen % lgcodegen plan_and_execute --code --human
LangGraph CodeGen 0.1.44
Graph source: plan_and_execute/plan_and_execute.txt
Python source: plan_and_execute/ (plan_and_execute.py)
File plan_and_execute/plan_and_execute.py exists. Overwrite? (y/n): y
Graph specification file plan_and_execute/plan_and_execute.txt already exists
To run:  python plan_and_execute/plan_and_execute.py

```

When it runs, conditions in the graph get human y/n prompts:
```

(py312) johannesjohannsen@Johanness-MacBook-Pro langgraph-codegen % python plan_and_execute/plan_and_execute.py
NODE: plan_step

    {'plan_step': {'nodes_visited': 'plan_step', 'counter': 1}}

NODE: execute_step

    {'execute_step': {'nodes_visited': 'execute_step', 'counter': 2}}

NODE: replan_step
is_done (y/n): n   <----- THIS IS HUMAN INPUT
CONDITION: is_done. Result: False

    {'replan_step': {'nodes_visited': 'replan_step', 'counter': 3}}

NODE: execute_step

    {'execute_step': {'nodes_visited': 'execute_step', 'counter': 4}}

NODE: replan_step
is_done (y/n): n
CONDITION: is_done. Result: False

    {'replan_step': {'nodes_visited': 'replan_step', 'counter': 5}}

NODE: execute_step

    {'execute_step': {'nodes_visited': 'execute_step', 'counter': 6}}

NODE: replan_step
is_done (y/n): y
CONDITION: is_done. Result: True

    {'replan_step': {'nodes_visited': 'replan_step', 'counter': 7}}

DONE STREAMING, final state:
StateSnapshot(values={'nodes_visited': ['plan_step', 'execute_step', 'replan_step', 'execute_step', 'replan_step', 'execute_step', 'replan_step'], 'counter': 7}, next=(), config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1f007763-8d62-667e-8007-aab71890c408'}}, metadata={'source': 'loop', 'writes': {'replan_step': {'nodes_visited': 'replan_step', 'counter': 7}}, 'thread_id': '1', 'step': 7, 'parents': {}}, created_at='2025-03-22T23:34:38.957902+00:00', parent_config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1f007763-8475-61b0-8006-3e2db0d9da30'}}, tasks=())

```



##### Making it real

Any of the generated node and condition functions can be replaced by placing a '.py' file with a definition of that function in the same directory, then re-generating the code.

For example, starting with this example graph, called 'rag':
```bash
START(AgentState) => get_docs
get_docs => format_docs
format_docs => format_prompt
format_prompt => generate
generate => END
```

We can generate the mock compiled graph and run it:

```bash
lgcodegen rag --code
python rag/rag.y
```

This outputs the following:
```bash
NODE: get_docs

    {'get_docs': {'nodes_visited': 'get_docs', 'counter': 1}}

NODE: format_docs

    {'format_docs': {'nodes_visited': 'format_docs', 'counter': 2}}

NODE: format_prompt

    {'format_prompt': {'nodes_visited': 'format_prompt', 'counter': 3}}

NODE: generate

    {'generate': {'nodes_visited': 'generate', 'counter': 4}}

DONE STREAMING, final state:
StateSnapshot(values={'nodes_visited': ['get_docs', 'format_docs', 'format_prompt', 'generate'], 'counter': 4}, next=(), config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1efa12c5-bc89-6fe6-8004-8f8476ca1b76'}}, metadata={'source': 'loop', 'writes': {'generate': {'nodes_visited': 'generate', 'counter': 4}}, 'thread_id': '1', 'step': 4, 'parents': {}}, created_at='2024-11-12T19:28:56.228241+00:00', parent_config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1efa12c5-bc88-6d76-8003-7f480a1284c6'}}, tasks=())
```

But in this case, I have some node functions that I've written, let's say file is `my_nodes.py`

This file has the graph state and nodes.  If this is in same folder as generated code, the generated code will use these for state and nodes -- the mock implementations will not be generated.

```python
# my_nodes.py 
# - class for Graph State (AgentState below)
# - nodes: get_docs, format_prompt, format_docs, generate
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


embedding_function = OpenAIEmbeddings()

docs = [
    Document(
        page_content="the dog loves to eat pizza", metadata={"source": "animal.txt"}
    ),
    Document(
        page_content="the cat loves to eat lasagna", metadata={"source": "animal.txt"}
    ),
]

db = Chroma.from_documents(docs, embedding_function)
retriever = db.as_retriever(search_kwargs={"k": 2})

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

class AgentState(TypedDict):
    question: str
    raw_docs: list[BaseMessage]
    formatted_docs: list[str]
    formatted_prompt: str
    generation: str

def get_docs(state: AgentState):
    print("get_docs:", state)
    question = state["question"]
    return { "raw_docs": retriever.invoke(question) }

def format_prompt(state: AgentState):
    print("format_prompt:", state)
    return { "formatted_prompt": prompt.invoke({"context": state['formatted_docs'], 'question': state['question'] })}
    
def format_docs(state: AgentState):
    print("format_docs:", state)
    documents = state["raw_docs"]
    return { "formatted_docs": "\n\n".join(doc.page_content for doc in documents) }

def generate(state: AgentState):
    print("generate:", state)
    result = model.invoke(state['formatted_prompt'])
    return { "generation": result.content }
```

When this file is placed in the same folder as the `rag.py` file, we then regenerate the graph code, and run it.



##### Using gen_* functions (gen_graph, gen_nodes, gen_state, gen_conditions)

Generates python code for parts of langgraph

```python
from langgraph_codegen import gen_graph

graph_spec = """
# required: start with StateClass and first_node
START(StateClass) => first_node

first_node
  should_go_to_second => second_node
  => third_node

second_node => third_node

third_node => END
"""

graph_code = gen_graph("my_graph", graph_spec)
print(graph_code)

# executing code gives compiled graph in variable 'my_graph'
exec(graph_code)

print(my_graph)
```

Output is:
```python
# GENERATED code, creates compiled graph: my_graph
my_graph = StateGraph(StateClass)
my_graph.add_node('first_node', first_node)
my_graph.add_node('should_go_to_second', should_go_to_second)
my_graph.add_node('second_node', second_node)
my_graph.add_node('third_node', third_node)
my_graph.add_edge(START, 'first_node')
my_graph.add_edge('should_go_to_second', 'second_node')
my_graph.add_edge('should_go_to_second', 'third_node')
my_graph.add_edge('second_node', 'third_node')
my_graph.add_edge('third_node', END)

my_graph = my_graph.compile()
```

#### Syntax

```START(StateClass) => first_node``` required

```# anything after pound sign is ignored```

```node_1 => node_2``` unconditional edge

```python
node_X
  condition_A => node_Y
  condition_B => node_Z
  => END  # unconditional if all above conditions fail
```

```node_1 => node_2, node_3``` ok to transition to multiple nodes.

##### Why This DSL Was Made

The main thing I want to do is condense larger patterns into the DSL, to make it easier to experiment with and evaluate graph architectures.

The DSL represents both Nodes and Conditional Edges with functions that take the Graph State as a parameter.  

The langgraph GraphBuilder makes the equivalent graph with python code (the DSL is translated into this code).  However, its flexibility also means its more complicated than necessary for some uses.

