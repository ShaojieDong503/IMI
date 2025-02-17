from base_clustering import task_one_script
from EDA import get_general_table
#from scarf import task_two_script


def main():
    data_path = "/Users/george/PycharmProjects/IMIProject/input/"
    output_path = "/Users/george/PycharmProjects/IMIProject/output/"
    wire_file_path = data_path + 'wire.csv'
    emt_file_path = data_path + 'emt.csv'
    eft_file_path = data_path + 'eft.csv'
    cheque_file_path = data_path + 'cheque.csv'
    card_file_path = data_path + 'card.csv'
    abm_file_path = data_path + 'abm.csv'
    #get_general_table(wire_file_path, emt_file_path, eft_file_path, cheque_file_path, card_file_path, abm_file_path,
     #                 output_path)
    task_one_script(output_path + "general_table.csv", output_path)
    #task_two_script(output_path + "general_table.csv", output_path)


if __name__ == "__main__":
    main()
