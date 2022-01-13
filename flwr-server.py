import flwr as fl
from flwr.server import Server
from flwr.server.client_manager import SimpleClientManager
from flwr.server.strategy import FedAvg

# Start Flower server for three rounds of federated learning
client_manager = SimpleClientManager()
strategy = FedAvg(on_fit_config_fn=lambda rnd : {"round": rnd})

srv = Server(client_manager=client_manager, strategy=strategy)

fl.server.start_server(server=srv, config={"num_rounds": 10})