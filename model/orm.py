#! /usr/bin/env python3
# coding: utf-8
"""Object-relational Mapper (ORM) class."""


class Orm:
    """Translate from ptyhon to sql."""

    def __init__(self, Log):
        self.Log = Log

    def build_params_values(self, values_list):
        nb_params = ",".join("%s" for value in values_list)
        return "VALUES ({})".format(nb_params)

    def multiple_insertion(self, insert_lists):
        """Insert datas to database."""
        for args in insert_lists:
            self.Log.execute(
                " ".join(
                    [
                        "INSERT IGNORE INTO {} ({})".format(*args),
                        self.build_params_values(args[-1]),
                    ]
                ),
                args[-1],
            )

    def simple_request(self, request_lists):
        """Insert datas to database."""
        result_list = []
        for args in request_lists:
            string = args[-1]
            result = self.Log.request(
                "SELECT {} FROM {} WHERE {} = (%s)".format(*args), [string]
            )[0][0]
            result_list.append(result)
        return result_list
