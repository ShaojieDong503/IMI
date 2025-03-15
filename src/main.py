from src.base_clustering import get_base_clustering
from src.EDA import get_eda
from src.Advance_clustering import get_advanced_clustering
from src.Embedding import get_embedding
from src.Scoring import get_score


def main():
    input_path = "../input/"
    output_path = "../output/"
    interim_path = "../interim/"
    resources_path = "../resources/"
    #get_eda(input_path, interim_path)
    #get_score(input_path, interim_path, resources_path)
    #get_embedding(output_path + "task2/", interim_path)
    get_base_clustering(input_path, output_path + "task1/", interim_path)
    #get_advanced_clustering(input_path, output_path+"task2/", interim_path)


if __name__ == "__main__":
    main()
