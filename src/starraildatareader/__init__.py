import os
from .starraildata import StarRailData

path_to_data = os.path.join(os.path.dirname(__file__), "..", "..", "data")
path_to_data = os.path.abspath(path_to_data)


def create_star_rail_data(path_to_starraildata, language="CN"):
    star_rail_data = StarRailData(language)
    star_rail_data.load_data(path_to_starraildata, path_to_data)
    return star_rail_data
