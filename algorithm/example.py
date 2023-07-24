from handlers import adj_matrix
from workflow_class import DAGGraphHandler

wf = DAGGraphHandler(adj_matrix)
print(wf.handle_incoming_request(0, 1, 0, 0, 1))
