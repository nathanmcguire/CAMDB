import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from sqlalchemy_data_model_visualizer import generate_data_model_diagram
from app.models.controls import Control
from app.models.safeguards import Safeguard
from app.models.security_functions import SecurityFunction
from app.models.implementation_groups import ImplementationGroup



if __name__ == "__main__":

    models = [Control, Safeguard, SecurityFunction, ImplementationGroup]
    output_file = "docs/models/diagrams/data_model_diagram.svg"
    add_labels = True
    generate_data_model_diagram(models, output_file=output_file, add_labels=add_labels)

