
# import libraries
import MetaTrader5 as mt5
import pandas as pd
import os
import pytz

# import classes from libraries
from anytree import Node, RenderTree
from datetime import datetime
from tqdm import tqdm
from typing import Type


class MT5Scraper:
    def __init__(self, login, server, password):
        self.login = login
        self.server = server
        self.password = password
        self.timezone = pytz.timezone('Etc/UTC')

    def __repr__(self):
        return f'MT5Scraper(login={self.login}, server={self.server})'

    def __str__(self):
        return f'MT5Scraper(login={self.login}, server={self.server})'

    @staticmethod
    def _disconnect() -> bool:
        """
        Disconnect from the MetaTrader 5 terminal
        :return: bool: True
        """
        mt5.shutdown()
        return True

    @staticmethod
    def _error(message: str, error: str) -> None:
        """
        Print an error message
        :param message: freely selectable message
        :param error: error message from the MetaTrader 5 terminal
        :return: None: None
        """
        print(message, 'error code:', error)
        return None

    @staticmethod
    def _build_symbol_tree(list_of_path: list) -> dict:
        """
        Build a tree from a list of paths
        :param: list_of_path: list: list of the paths
        :return: dict: dict representing the tree of the paths
        """
        tree = dict()
        for path in list_of_path:
            # split the path into a list
            path_list = path.split('\\')
            # get the last item in the path list
            value = path_list[-1]
            # get the last folder in the path list
            last_folder = path_list[-2]
            # remove the last two item from the path list
            path_list = path_list[:-2]
            # get the current level of the tree
            current_level = tree
            # loop through the path list
            for path_item in path_list:
                # check if the path item exists in the current level
                if path_item not in current_level:
                    # if not, add it to the current level
                    current_level[path_item] = dict()
                # get the next level
                current_level = current_level[path_item]
            # append the value to the current level if it exists otherwise create a new list
            if last_folder in current_level:
                current_level[last_folder].append(value)
            else:
                current_level[last_folder] = [value]
        return tree

    @staticmethod
    def _save(save_path: str, symbol_df: pd.DataFrame, symbol: str) -> None:
        """
        Save the data to a csv file
        :param save_path: str: path to the folder where the data should be saved
        :param symbol_df: pd.DataFrame: dataframe containing the data
        :param symbol: str: symbol name
        :return: None: None
        """
        # if save_path is None, save the data to the current directory
        if save_path is None:
            symbol_df.to_csv(f'{symbol}.csv', index=False)
        else:
            # if save_path doesn't exist, create it
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            symbol_df.to_csv(f'{save_path}/{symbol}.csv', index=False)
        return None

    @staticmethod
    def _tf_translator(tf: str) -> mt5.TIMEFRAME_D1:
        """
        Convert a time frame to a MetaTrader 5 time frame
        :param tf: str: time frame
        :return: mt5.TIMEFRAME_D1: MetaTrader 5 time frame
        """
        translation = {'M1': mt5.TIMEFRAME_M1,
                       'M2': mt5.TIMEFRAME_M2,
                       'M3': mt5.TIMEFRAME_M3,
                       'M4': mt5.TIMEFRAME_M4,
                       'M5': mt5.TIMEFRAME_M5,
                       'M6': mt5.TIMEFRAME_M6,
                       'M10': mt5.TIMEFRAME_M10,
                       'M12': mt5.TIMEFRAME_M12,
                       'M15': mt5.TIMEFRAME_M15,
                       'M20': mt5.TIMEFRAME_M20,
                       'M30': mt5.TIMEFRAME_M30,
                       'H1': mt5.TIMEFRAME_H1,
                       'H2': mt5.TIMEFRAME_H2,
                       'H3': mt5.TIMEFRAME_H3,
                       'H4': mt5.TIMEFRAME_H4,
                       'H6': mt5.TIMEFRAME_H6,
                       'H8': mt5.TIMEFRAME_H8,
                       'H12': mt5.TIMEFRAME_H12,
                       'D1': mt5.TIMEFRAME_D1,
                       'W1': mt5.TIMEFRAME_W1,
                       'MN1': mt5.TIMEFRAME_MN1}
        if tf not in translation:
            raise ValueError(f'{tf} is not a valid time frame. it must be one of the following: {list(translation.keys())}')
        return translation[tf]

    @staticmethod
    def _path_translator(path: str) -> str:
        """
        Convert a path to a MetaTrader 5 path
        :param path: str: path to symbol
        :return: str: MetaTrader 5 symbol path
        """
        # split the path into a list
        path_list = path.split('/')
        # concatenate the path with \\
        path = '\\'.join(path_list)
        return path

    def _connect(self) -> bool:
        """
        Connect to the MetaTrader 5 terminal
        :return: bool: True if connected, False if not
        """
        if not mt5.initialize(login=self.login, server=self.server, password=self.password):
            # if connection failed, print error message
            self._error('initialisation failed,', mt5.last_error())
            return False
        return True

    def _add_node(self, parent: Node, tree: dict) -> None:
        """
        Add nodes to a tree
        :param parent: Node: parent node
        :param tree: dict: dict representing the tree
        :return: None: None
        """
        for key, value in tree.items():
            node = Node(key, parent=parent)
            if isinstance(value, dict):
                self._add_node(node, value)
            else:
                for item in value:
                    Node(item, parent=node)
        return None

    def _datetime_translator(self, datetime_tuple: tuple) -> datetime:
        """
        Convert a datetime tuple to a datetime object
        :param datetime_tuple: tuple: datetime tuple
        :return: datetime: datetime object
        """
        # len datetime_tuple must be between 3 and 6
        if len(datetime_tuple) not in range(3, 7):
            raise ValueError('datetime tuple must be a tuple of min length 3 (Y, M, D) up to 6 (Y, M, D, h, m, s)')
        # copy the datetime tuple and fill the missing values with 0
        datetime_list = list(datetime_tuple)
        for i in range(len(datetime_list), 6):
            datetime_list.append(0)
        # convert the datetime list to a datetime object
        return datetime(*datetime_list, tzinfo=self.timezone)

    def visualize_tree(self, tree: dict) -> Type[Node]:
        """
        Visualize a tree
        :param tree: dict: dict representing the tree
        :return: Node: root node
        """
        # create a root node
        root = Node('root')
        # call the recursive function to add nodes to the tree
        self._add_node(root, tree)
        # print the tree
        for pre, fill, node in RenderTree(root):
            print(f"{pre}{node.name}")
        return Node

    def get_symbols(self, symbol_path: str = 'all', visualize: bool = True) -> list:
        """
        Get the symbols from the MetaTrader 5 terminal
        :param symbol_path: str: path to the folder where the symbols are stored
        :param visualize: bool: if True, visualize the tree
        :return: list: list of the symbols
        """
        self._connect()
        # get all the symbols
        symbols_raw = mt5.symbols_get()
        if symbol_path == 'all':
            symbols = symbols_raw
        else:
            # convert the path to a MetaTrader 5 path if path contains /
            if '/' in symbol_path:
                symbol_path = self._path_translator(symbol_path)
            # filter the symbols
            symbols = [symbol for symbol in symbols_raw if symbol_path in symbol.path]
        self._disconnect()
        path_list = list()
        symbol_list = list()
        for symbol in symbols:
            symbol_path = symbol.path
            symbol_name = symbol.name
            # append the symbol name to the symbol list
            symbol_list.append(symbol_name)
            # append the symbol path to the path list
            path_list.append(symbol_path)
        # build the tree
        tree = self._build_symbol_tree(path_list)
        if visualize:
            self.visualize_tree(tree)
        return symbol_list

    def get_symbol_count(self) -> int:
        """
        Get the number of symbols
        :return: int: number of symbols
        """
        self._connect()
        # number of symbols
        symbol_count = mt5.symbols_total()
        self._disconnect()
        return symbol_count

    def get_historical_data(self, symbol_list: list, timeframe: str, start_date: tuple,
                            end_date: tuple, save: bool = False, save_path: str = None) -> dict:
        """
        Get the historical data from the MetaTrader 5 terminal
        :param symbol_list: list: list of the symbols
        :param timeframe: str: timeframe of the data
        :param start_date: tuple: start datetime of the data
        :param end_date: tuple: end datetime of the data
        :param save: bool: if True, save the data to a csv file
        :param save_path: str: path to the folder where the data should be saved
        :return: dict: dict containing the dataframes
        """
        # connect to the MetaTrader 5 terminal
        self._connect()
        # create a dictionary to store the data
        data_dict = dict()
        # loop through the symbol list
        for symbol in tqdm(symbol_list):
            # get the symbol data
            symbol_data = mt5.copy_rates_range(symbol,
                                               self._tf_translator(timeframe),
                                               self._datetime_translator(start_date),
                                               self._datetime_translator(end_date))
            # append the data to the dictionary
            symbol_df = pd.DataFrame(symbol_data)
            symbol_df['time'] = pd.to_datetime(symbol_df['time'], unit='s')
            if save:
                self._save(save_path, symbol_df, symbol)
            data_dict[symbol] = symbol_df
        # close the connection
        self._disconnect()
        return data_dict
